# Đẻ Đất Đẻ Nước · Bộ Sử Thi Luyện Kể Chuyện 5 Cấp Độ

**Sử thi Mường — phiên bản kể cho trẻ 9–10 tuổi**  
**6 Hồi · 28 Chương · 28 Tranh gợi nhớ · 5 Cấp độ luyện kể**

Kho dữ liệu này chuyển *Đẻ đất đẻ nước* — trường ca *mo lêu* của người Mường — thành một bộ học liệu kể chuyện đọc thành tiếng, giữ tinh thần, câu chữ, vần, nhịp điệu và mạch kể của bản gốc, đồng thời làm rõ những chỗ trẻ 9–10 tuổi cần một bàn tay dẫn đường.

> **Trạng thái:** **Level 0–3 đã hoàn tất** (bối cảnh, toàn văn 28 chương, dàn ý chi tiết, dàn ý tóm tắt). **Level 4** hoàn tất phần **đặc tả phong cách + 28 đề bài vẽ + gallery danh mục**; 28 ảnh minh họa chưa được tạo và được để ngỏ (xem cờ `image_generated` trong `locales/vi/story-index.json`).

---

## 1. Văn bản gốc

| | |
|---|---|
| **Tác phẩm** | *Đẻ đất đẻ nước* — sử thi của người Mường |
| **Bản dùng làm gốc** | [`Đẻ đất đẻ nước.md`](Đẻ%20đất%20đẻ%20nước.md), bản hợp nhất 6 Hồi · 28 Chương từ ấn phẩm 1988/2000 (26 *rằng*), lời đọc 1988 và bản đọc 28 chương |
| **Nguồn thư mục** | Đặng Văn Lung, Vương Anh, Hoàng Anh Nhân giới thiệu; *Tổng tập Văn học Việt Nam*, tập 41, NXB Khoa học Xã hội, 2000 |
| **Nguyên tắc** | Không sửa một byte vào văn bản gốc; mọi biên tập nằm trong `locales/vi/` |

---

## 2. Kiến trúc 5 cấp độ

| Cấp độ | Thư mục | Mục đích luyện tập |
| :--- | :--- | :--- |
| **Level 0** | [`locales/vi/level-0-context/`](locales/vi/level-0-context/) | **Bối cảnh & Linh hồn sử thi** — không gian văn hóa Mường, nhịp kể cho tuổi 9–10, cách đọc tên riêng, và 8 tư liệu tham khảo. |
| **Level 1** | [`locales/vi/level-1-full-text/`](locales/vi/level-1-full-text/) | **Toàn văn đọc thành tiếng** — thuần lời mo, giữ nhịp thơ, kèm *Lưu ý giọng kể* từng chương. |
| **Level 2** | [`locales/vi/level-2-detailed-outline/`](locales/vi/level-2-detailed-outline/) | **Dàn ý chi tiết** — nhân vật, hình tượng, diễn biến, điệp khúc và điểm nhấn kể chuyện. |
| **Level 3** | [`locales/vi/level-3-summary-outline/chapter-summaries.md`](locales/vi/level-3-summary-outline/chapter-summaries.md) | **Dàn ý tóm tắt** — một khung xương duy nhất cho cả 28 chương. |
| **Level 4** | [`locales/vi/level-4-visual-prompts/`](locales/vi/level-4-visual-prompts/) | **Tranh gợi nhớ thuần hình ảnh** — đặc tả phong cách, 28 đề bài vẽ và gallery danh mục; ảnh minh họa chưa tạo. |

Chỉ mục máy đọc: [`locales/vi/story-index.json`](locales/vi/story-index.json).

---

## 3. Sáu Hồi · Hai mươi tám Chương

| Hồi | Tên | Chương |
| :--- | :--- | :--- |
| **I** | Khai Thiên Lập Địa Và Khởi Nguồn Giống Nòi | 1–7 |
| **II** | Lập Lang Dựng Mường Và Sáng Tạo Văn Hóa | 8–16 |
| **III** | Lập Gia, Đúc Trống Đồng Và Chia Đất | 17–19 |
| **IV** | Chu Kỳ Cây Chu — Tìm, Chặt, Dựng Và Đốt | 20–23 |
| **V** | Trừ Thú Dữ Và Dẹp Loạn Giặc Ma | 24–27 |
| **VI** | Khải Hoàn Về Đồng Chì Tam Quan Kẻ Chợ | 28 |

Danh mục đầy đủ: [`locales/vi/README.md`](locales/vi/README.md).

---

## 4. Nguyên tắc biên tập cho tuổi 9–10

1. **Thuần lời mo:** thơ, xuống dòng theo hơi thở, điệp ngữ và câu chuyển rằng; không thêm đoạn dẫn văn xuôi.
2. **Không hư cấu thần thoại:** mọi nhân vật, địa danh, tục lệ đều từ văn bản gốc.
3. **Tiết chế cảnh nặng:** bạo lực diễn ra ngoài sân khấu, không miêu tả kéo dài; giữ hậu quả và bài học.
4. **Giữ tiếng cười dân gian** làm nhịp nghỉ cảm xúc cho trẻ.

---

## 5. Kiểm tra dữ liệu

```bash
python3 scripts/validate_corpus.py --draft
```

`--draft` cho phép báo *cảnh báo* với các tệp chưa biên soạn, nhưng vẫn *báo lỗi* với dữ liệu sai cấu trúc, thiếu chương hoặc trùng lặp.

---

## 6. Giấy phép

[MIT](LICENSE) © 2026 xuvivn.
