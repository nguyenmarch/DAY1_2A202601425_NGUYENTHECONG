# K3 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 9h00–13h00
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay nội dung placeholder bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.5, 1.0 và 1.5 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> *Khi temperature = 0.0, phản hồi mang tính nhất quán cao, tập trung vào các sự thật phổ biến (như diện tích/văn hóa) và gần như lặp lại giống hệt nhau nếu gọi nhiều lần. Khi tăng lên 0.5–1.0, từ ngữ đa dạng hơn, văn phong sinh động hơn. Đến 1.5, phản hồi trở nên sáng tạo quá mức, có dấu hiệu lan man, ngắt kết nối logic hoặc xuất hiện từ ngữ lạ.*

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Nên đặt temperature từ 0.0 đến 0.2. Vì chatbot hỗ trợ khách hàng cần cung cấp thông tin chính xác, nhất quán và đáng tin cậy về chính sách hay sản phẩm; mức nhiệt độ thấp giúp giảm thiểu tối đa hiện tượng ảo giác (hallucination) và câu trả lời bất nhất.*



### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**
> *GPT-4o đắt hơn GPT-4o-mini khoảng 12–15 lần cho tổng chi phí output token (tùy bảng giá API hiện tại). Xứng đáng dùng GPT-4o: xử lý tác vụ phức tạp yêu cầu tư duy logic cao, phân tích hợp đồng pháp lý hoặc lập trình nâng cao. Nên dùng GPT-4o-mini: phân loại văn bản đơn giản, tóm tắt ý chính hoặc chatbot CSKH theo kịch bản.*

---


## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:
- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)
> *Phản hồi cho trẻ 8 tuổi đơn giản, dễ hiểu kèm ví dụ thực tế; phản hồi cho chuyên gia chứa nhiều thuật ngữ kỹ thuật chuyên sâu. System prompt giúp định hình vai trò, văn phong và đối tượng mục tiêu cho model.*

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**
> *Chênh lệch khoảng 30%–50% (tiktoken ra số token cao hơn). Tiếng Việt tốn nhiều token hơn vì thuật toán tokenizer ưu tiên tiếng Anh, khiến các từ ghép và dấu thanh tiếng Việt bị tách thành nhiều sub-token.*

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Streaming: Cần cho giao diện Chatbot UI để hiện chữ ngay (giảm thời gian chờ). Non-streaming: Cần cho tác vụ ngầm (backend), xuất dữ liệu JSON hoặc phân loại dữ liệu.*

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**
> *Exponential backoff giúp dãn cách thời gian retry để server kịp phục hồi. Delay cố định sẽ gây ra hiện tượng "bão yêu cầu" (thundering herd), làm sập server liên tục.*

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**
> *System prompt: "Bạn là trợ lý Python. Trả lời ngắn gọn bằng tiếng Việt, kèm code tối ưu và giải thích dưới 2 câu."Giải thích: Nhãn "ngắn gọn" giúp tiết kiệm token; chỉ định "tiếng Việt" giúp đảm bảo ngôn ngữ phản hồi.*
open
### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**
> *Hạn chế: Giới hạn bộ nhớ context (chỉ nhớ 3 lượt thoại).Cải thiện: Dùng Vector DB (như ChromaDB) để lưu lịch sử và khôi phục ngữ cảnh liên quan khi cần.*

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/` và zip theo hướng dẫn README
