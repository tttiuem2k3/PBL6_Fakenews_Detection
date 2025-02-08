# 🚨 HỆ THỐNG NHẬN DẠNG TIN GIẢ SỬ DỤNG ELECTRA-Base 🚨

## 📌 Giới thiệu đề tài
Tin giả (Fake News) đang trở thành vấn nạn nghiêm trọng trong thời đại số, đặc biệt trên các nền tảng mạng xã hội. Dự án này tập trung xây dựng hệ thống tự động phân loại tin giả tiếng Việt bằng mô hình **ELECTRA-Base**, kết hợp công nghệ NLP tiên tiến và cơ sở dữ liệu tin tức đa dạng.

---

## 📂 Nguồn dữ liệu
- **📰 Tin thật**: Thu thập từ các báo chính thống như VnExpress, Dân Trí, Thanh Niên (16,258 bài).
- **📛 Tin giả**: Lấy từ các trang không chính thống như Viettan, Danlambao (16,086 bài).
- **📊 Cấu trúc dữ liệu**: Bao gồm tiêu đề, nội dung, nguồn, nhãn (Real/Fake), thời gian đăng.

---

## 🔄 Quá trình thu thập và xử lý dữ liệu
1. **🧹 Tiền xử lý**:
   - Chuẩn hóa văn bản (chuyển chữ thường, xóa ký tự đặc biệt).
   - Tách từ tiếng Việt bằng thư viện `pyvi`.
   - Loại bỏ stopwords và cân bằng dữ liệu.
2. **📂 Phân chia tập dữ liệu**:
   - **Train**: 60% (19,394 mẫu)
   - **Validation**: 20% (6,464 mẫu)
   - **Test**: 20% (6,468 mẫu)

---

## 📊 Thống kê dữ liệu
| Loại tin | Số lượng | Tỷ lệ |
|----------|----------|-------|
| 📰 Tin thật | 16,258   | 50.3% |
| 📛 Tin giả  | 16,086   | 49.7% |

![Phân bố từ sau tiền xử lý](Hình_5_6.png)

---

## 🛠️ Chức năng chính
- **🔍 Phân loại tin giả**: Nhận đầu vào là văn bản, trả về nhãn "Thật"/"Giả" kèm xác suất.
- **🔗 Gợi ý tin liên quan**: Tìm kiếm bài báo tương tự từ CSDL hoặc trang tin uy tín.
- **📊 Giao diện trực quan**: Biểu đồ pie chart và danh sách liên kết tham khảo.

---

## 🚀 ELECTRA-Base: Giới thiệu và Sức mạnh
### 🌟 Tổng quan
**ELECTRA** (Efficiently Learning an Encoder that Classifies Token Replacements Accurately) là mô hình NLP sử dụng cơ chế **Replaced Token Detection**:
- **Generator**: Tạo token giả thay thế ngẫu nhiên.
- **Discriminator**: Phát hiện token bị thay thế, tối ưu hóa việc học toàn bộ đầu vào.

### 💪 Ưu điểm vượt trội
| Ưu điểm                  | Hiệu quả                                                                 |
|--------------------------|--------------------------------------------------------------------------|
| **💻 Tiết kiệm tài nguyên**     | Chỉ cần 25% tài nguyên so với BERT/RoBERTa                               |
| **📜 Xử lý văn bản dài**        | Áp dụng **Sliding Window** (512 tokens/window) với overlap 128 tokens    |
| **🎯 Độ chính xác cao**         | F1-score đạt **99%** trên tập test                                       |
| **🧠 Tích hợp Attention**       | Thêm Multihead Attention để tập trung vào từ khóa quan trọng            |

### 🔧 Cải tiến trong dự án
1. **📜 Xử lý văn bản dài**:
   - Chia văn bản thành các đoạn 512 tokens, kết hợp kỹ thuật overlap.
   - Dùng voting từ các đoạn để quyết định nhãn cuối cùng.
2. **⚙️ Nâng cấp kiến trúc**:
   - Thêm lớp **MultiheadAttention** và **LayerNorm**.
   - Tích hợp Fully Connected layers để tối ưu biểu diễn đặc trưng.
## 📈 Kết quả
| Model       | Accuracy | F1-score | Recall |
|-------------|----------|----------|--------|
| ELECTRA-Base| **99%**  | **99%**  | **99%**|

![Ma trận nhầm lẫn](Hình_25.png)

---

## 🔮 Hướng phát triển
- **🌍 Mở rộng sang đa ngôn ngữ** (tiếng Anh, Trung).
- **🖼️ Tích hợp phân tích hình ảnh/video** bằng CNN.
- **🌐 Xây dựng extension trình duyệt** để quét tin giả real-time.

---

## 🛠️ Cài đặt
```bash
git clone https://github.com/your-repo/fake-news-detection
cd fake-news-detection
pip install -r requirements.txt
```
### Huấn luyện mô hình:
- Huấn luyện mô hình dựa trên bộ data: [./DATA/DATA.rar]
### Chạy ứng dụng:
python app.py

---

##  📞 Liên hệ
👥 

📧 Email: tttiuem2k3@gmail.com
