"""
K3 — Ngày 1: Khám Phá LLM API (9h00–13h00)
AICB-P1: AI Practical Competency Program, Phase 1

Hướng dẫn:
    1. Làm theo LAB_GUIDE.md — mỗi block có các bước chi tiết và checkpoint.
    2. Điền vào tất cả các chỗ đánh dấu TODO.
    3. KHÔNG đổi chữ ký hàm (tên hàm, tham số).
    4. Import OpenAI BÊN TRONG hàm (xem gợi ý) — nếu import ở đầu file,
       các bài test mock sẽ không hoạt động.
    5. Kiểm tra tiến độ:  pytest tests/test_part1.py -v  (từng phần)
       Chấm điểm tổng:    python grade.py
"""

import os
import time
from typing import Any, Callable

from dotenv import load_dotenv

load_dotenv()

PRICING_PER_1K_TOKENS = {
    "gpt-4o": {"input": 0.0025, "output": 0.010},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
}

OPENAI_MODEL = os.getenv("LAB_MODEL", "gpt-4o")
OPENAI_MINI_MODEL = os.getenv("LAB_MINI_MODEL", "gpt-4o-mini")


# ===========================================================================
# PART 1 — API CƠ BẢN (Block 1: 10h00–10h40)
# ===========================================================================

# ---------------------------------------------------------------------------
# Task 1.1 — Gọi GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Gọi OpenAI Chat Completions API, trả về nội dung phản hồi + độ trễ.
    """
    from openai import OpenAI  # Import BÊN TRONG hàm

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    start_time = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.perf_counter() - start_time
    response_text = response.choices[0].message.content
    return response_text, latency


# ---------------------------------------------------------------------------
# Task 1.2 — Gọi GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Gọi API với model gpt-4o-mini — nhanh hơn và rẻ hơn.
    """
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 1.3 — So sánh GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Gọi cả hai model với cùng một prompt và trả về dict so sánh.
    """
    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)

    gpt4o_cost_estimate = (
        (len(gpt4o_response.split()) / 0.75) / 1000
        * PRICING_PER_1K_TOKENS["gpt-4o"]["output"]
    )

    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# ===========================================================================
# PART 2 — SYSTEM PROMPT & TOKEN (Block 2: 10h40–11h20)
# ===========================================================================

# ---------------------------------------------------------------------------
# Task 2.1 — Chat với system prompt (persona)
# ---------------------------------------------------------------------------
def chat_with_system_prompt(
    system_prompt: str,
    user_prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Gọi API với MESSAGES gồm 2 phần: system prompt và user prompt.
    """
    from openai import OpenAI 

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    start_time = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    latency = time.perf_counter() - start_time
    response_text = response.choices[0].message.content
    return response_text, latency


# ---------------------------------------------------------------------------
# Task 2.2 — Đếm token bằng tiktoken
# ---------------------------------------------------------------------------
def count_tokens(text: str, model: str = OPENAI_MODEL) -> int:
    """
    Đếm số token của một đoạn text bằng thư viện tiktoken.
    """
    try:
        import tiktoken

        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(text))
    except Exception:
        return max(1, len(text) // 4)


# ---------------------------------------------------------------------------
# Task 2.3 — Ước tính chi phí chính xác
# ---------------------------------------------------------------------------
def estimate_cost(prompt: str, response: str, model: str = OPENAI_MODEL) -> dict:
    """
    Tính chi phí một lượt gọi API dựa trên số token THẬT.
    """
    input_tokens = count_tokens(prompt, model=model)
    output_tokens = count_tokens(response, model=model)

    pricing = PRICING_PER_1K_TOKENS.get(
        model, PRICING_PER_1K_TOKENS["gpt-4o"]
    )
    input_cost = input_tokens / 1000 * pricing["input"]
    output_cost = output_tokens / 1000 * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


# ===========================================================================
# PART 3 — STREAMING & ĐỘ BỀN (Block 3: 11h30–12h10)
# ===========================================================================

# ---------------------------------------------------------------------------
# Task 3.1 — Chatbot streaming có lịch sử hội thoại
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Chatbot dòng lệnh tương tác dùng streaming.
    """
    from openai import OpenAI  # Import BÊN TRONG hàm

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history = []

    while True:
        user_input = input("Bạn: ")
        if user_input.strip().lower() in ("quit", "exit"):
            print("Thoát chatbot.")
            break

        history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": "Bạn là trợ lý thân thiện."}] + history

        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            stream=True,
        )

        print("Trợ lý: ", end="", flush=True)
        assistant_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_response += delta
        print()

        history.append({"role": "assistant", "content": assistant_response})
        history = history[-6:]


# ---------------------------------------------------------------------------
# Task 3.2 — Retry với exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Thử lại fn() nếu gặp lỗi với exponential backoff.
    """
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Lỗi: {e}. Thử lại sau {delay:.2f} giây...")
            time.sleep(delay)


# ===========================================================================
# PART 4 — MINI-PROJECT: TRỢ LÝ CLI HOÀN CHỈNH (Block 4: 12h10–12h50)
# ===========================================================================
def run_assistant(
    persona: str,
    get_input: Callable[[], str] = None,
    max_turns: int = None,
) -> dict:
    """
    Trợ lý CLI hoàn chỉnh.
    """
    from openai import OpenAI  

    if get_input is None:
        get_input = input

    history = []
    num_turns = 0
    total_tokens = 0
    total_cost = 0.0

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    while True:
        if max_turns is not None and num_turns >= max_turns:
            break

        # Gọi get_input() không truyền tham số để tương thích với mock test
        user_msg = get_input()
        if user_msg.strip().lower() in ("quit", "exit"):
            break

        messages = [{"role": "system", "content": persona}] + history + [{"role": "user", "content": user_msg}]

        def api_call():
            return client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                stream=True,
            )

        stream = retry_with_backoff(api_call)

        assistant_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_response += delta
        print()

        history.append({"role": "user", "content": user_msg})
        history.append({"role": "assistant", "content": assistant_response})
        history = history[-6:]

        input_tokens = count_tokens(user_msg, model=OPENAI_MODEL)
        output_tokens = count_tokens(assistant_response, model=OPENAI_MODEL)
        cost_info = estimate_cost(user_msg, assistant_response, model=OPENAI_MODEL)

        total_tokens += input_tokens + output_tokens
        total_cost += cost_info["total_cost"]
        num_turns += 1

    return {
        "num_turns": num_turns,
        "total_tokens": total_tokens,
        "total_cost": total_cost,
        "history": history,
    }


# ===========================================================================
# BONUS
# ===========================================================================
def batch_compare(prompts: list[str]) -> list[dict]:
    results = []
    for prompt in prompts:
        comparison = compare_models(prompt)
        comparison["prompt"] = prompt
        results.append(comparison)
    return results


def format_comparison_table(results: list[dict]) -> str:
    lines = []
    header = f"{'Prompt':<40} | {'GPT-4o Response':<40} | {'Mini Response':<40} | {'GPT-4o Latency':<15} | {'Mini Latency':<15}"
    lines.append(header)
    lines.append("-" * len(header))
    for result in results:
        prompt = (result["prompt"][:37] + "...") if len(result["prompt"]) > 40 else result["prompt"]
        gpt4o_resp = (result["gpt4o_response"][:37] + "...") if len(result["gpt4o_response"]) > 40 else result["gpt4o_response"]
        mini_resp = (result["mini_response"][:37] + "...") if len(result["mini_response"]) > 40 else result["mini_response"]
        gpt4o_latency = f"{result['gpt4o_latency']:.2f}s"
        mini_latency = f"{result['mini_latency']:.2f}s"
        line = f"{prompt:<40} | {gpt4o_resp:<40} | {mini_resp:<40} | {gpt4o_latency:<15} | {mini_latency:<15}"
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    print("=== So sánh model ===")
    result = compare_models(
        "Giải thích khác biệt giữa temperature và top_p trong một câu."
    )
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Trợ lý CLI (gõ 'quit' để thoát) ===")
    stats = run_assistant(
        persona="Bạn là trợ giảng thân thiện của khóa AI, "
                "trả lời ngắn gọn bằng tiếng Việt.",
    )
    print("\n--- Thống kê phiên chat ---")
    for key, value in stats.items():
        if key != "history":
            print(f"{key}: {value}")