# 🚨 HỆ THỐNG NHẬN DẠNG TIN GIẢ | ELECTRA-Base 🚨

## 📌 Giới thiệu đề tài
Tin giả (**Fake News**) đang trở thành vấn nạn nghiêm trọng trong thời đại số, đặc biệt trên các nền tảng mạng xã hội. Dự án này tập trung xây dựng hệ thống tự động phân loại tin giả tiếng Việt bằng mô hình **ELECTRA-Base**, kết hợp công nghệ NLP tiên tiến và bộ dữ liệu tin tức về chủ đề chính trị đa dạng.

---
## :tv: Demo
![Demo](demo1.gif)
- Xem DEMO đầy đủ tại đây: https://www.youtube.com/watch?v=HQ2c8JY_TXI&t=25s
---
## 📂 Nguồn dữ liệu
- **📰 Tin thật**: Thu thập từ các báo chính thống như VnExpress, Dân Trí, Thanh Niên (16,258 bài báo).
- **📛 Tin giả**: Lấy từ các trang không chính thống như Viettan, Danlambao (16,086 bài báo).
- **📊 Cấu trúc dữ liệu**: Bao gồm tiêu đề, nội dung, nguồn, nhãn (Real/Fake), thời gian đăng của bài báo.

---

## 🔄 Quá trình thu thập và xử lý dữ liệu
1. **🗂️ Thu thập dữ liệu**:
   - Sử dụng các thư viện như Selenium, BeautifulSoup, Requests,.. để thu thập dữ liệu là các bài báo từ nguồn dữ liệu theo cấu trúc dữ liệu.
   - Tham khảo code ở thư mục [crawl_data](./DATA/crawl_data)
2. **🧹 Tiền xử lý**:
   - Chuẩn hóa văn bản (chuyển chữ thường, xóa ký tự đặc biệt).
   - Tách từ tiếng Việt (word_segmentation): [`NlpHUST/vi-word-segmentation`](https://huggingface.co/NlpHUST/vi-word-segmentation)
   - Loại bỏ stopwords và cân bằng dữ liệu.
     
   ![Qui trình tiền xử lý dữ liệu](./Images/anh1.jpg)

3. **📊 Thống kê dữ liệu**
   | Loại tin | Số lượng | Tỷ lệ |
   |----------|----------|-------|
   | 📰 Tin thật | 16,258   | 50.3% |
   | 📛 Tin giả  | 16,086   | 49.7% |

   ![Phân bố từ sau tiền xử lý](./Images/anh2.jpg)

   ![Phân bố từ sau tiền xử lý](./Images/img3.jpg)   
4. **📂 Phân chia tập dữ liệu huấn luyện**:
   - **Train**: 60% (19,394 mẫu)
   - **Validation**: 20% (6,464 mẫu)
   - **Test**: 20% (6,468 mẫu)

---

## 🛠️ Chức năng chính
- **🔍 Phân loại tin giả**: Nhận đầu vào là văn bản, trả về nhãn "Thật"/"Giả" kèm xác suất.
- **📊 Giao diện trực quan**: Biểu đồ pie chart.

---

## 🚀 ELECTRA-Base: Giới thiệu và Sức mạnh
### 🌟 Tổng quan
**ELECTRA** (Efficiently Learning an Encoder that Classifies Token Replacements Accurately) là mô hình NLP sử dụng cơ chế **Replaced Token Detection**:
- **Generator**: Tạo token giả thay thế ngẫu nhiên.
- **Discriminator**: Phát hiện token bị thay thế, tối ưu hóa việc học toàn bộ đầu vào.
  
![cơ chế electra](./Images/img4.jpg)
### 💪 Ưu điểm vượt trội
| Ưu điểm                  | Hiệu quả                                                                 |
|--------------------------|--------------------------------------------------------------------------|
| **💻 Tiết kiệm tài nguyên**     | Chỉ cần 25% tài nguyên so với BERT/RoBERTa                               |
| **📜 Xử lý văn bản dài**        | Áp dụng **Sliding Window** (512 tokens/window) với overlap 128 tokens    |
| **🎯 Độ chính xác cao**         | F1-score đạt **99%** trên tập test                                       |
| **🧠 Tích hợp Attention**       | Thêm Multihead Attention để tập trung vào từ khóa quan trọng            |

### 🔧 Cải tiến trong dự án
1. **📜 Xử lý văn bản dài**:
   - Chia văn bản thành các đoạn 512 tokens, kết hợp kỹ thuật overlap - cửa sổ trượt với độ trượt là 128 tokens.
   - Dùng voting từ các đoạn để quyết định nhãn cuối cùng.
2. **⚙️ Nâng cấp kiến trúc**:
   - Thêm lớp **MultiheadAttention** và **LayerNorm**.
   - Tích hợp Fully Connected layers để tối ưu biểu diễn đặc trưng.
     
![cải tiến mô hình electra](./Images/img5.jpg)

### 🚀 Qui trình huấn luyện
1. **🛠️ Cấu hình huấn luyện:**

| Epochs      | BATH_SIZE | OPTIMIZER | DROPOUT |LEARNING_RATE|NUM_CLASSES| 
|-------------|-----------|-----------|---------|-------------|-----------| 
|    **4**    |  **48**   |**AdamW**  | **0.3** | **5e-5 -> 1e-5**|**2**| 

2. **🗃️ Qui trình huấn luyện:**

![qui trình huấn luyện](./Images/img6.jpg)


## 📈 Kết quả
| Model       | Accuracy | F1-score | Recall |
|-------------|----------|----------|--------|
| ELECTRA-Base| **99%**  | **99%**  | **99%**|

![Ma trận nhầm lẫn](./Images/img9.jpg)

---
## ⚖️ So sánh kết quả với Transformer-XL và PhoBERT

Dưới đây là bảng so sánh kết quả giữa **ELECTRA-Base**, **Transformer-XL**, và **PhoBERT** trên tập dữ liệu test:

| Model           | Accuracy | F1-score | Recall | Parameters |
|-----------------|----------|----------|--------|------------|
| **ELECTRA-Base**| **99%**  | **99%**  | **99%**| 109M       |
| Transformer-XL  | 94%      | 94%      | 94%    | 191M       |
| PhoBERT         | 93%      | 93%      | 93%    | 135M       |

### 📊 Biểu đồ so sánh
![Biểu đồ so sánh độ mất mát](./Images/img7.jpg)

![Biểu đồ so sánh độ chính xác](./Images/img8.jpg)

### 📝 Nhận xét
- **ELECTRA-Base** cho kết quả **vượt trội** so với Transformer-XL và PhoBERT, đạt độ chính xác **99%**.
- **Transformer-XL** và **PhoBERT** cũng cho kết quả tốt, nhưng độ chính xác thấp hơn (94% và 93%).
- **ELECTRA-Base** sử dụng ít tham số hơn (109M) so với Transformer-XL (191M) và PhoBERT (135M), giúp tiết kiệm tài nguyên tính toán.

---
## 🔮 Hướng phát triển
- **🌍 Mở rộng sang đa ngôn ngữ** (tiếng Anh, Trung).
- **🖼️ Tích hợp phân tích hình ảnh/video** bằng CNN.
- **🌐 Xây dựng extension trình duyệt** để quét tin giả real-time.

---

## 🛠️ Cài đặt
### Tải code:
```bash
cd fake-news-detection
git clone https://github.com/tttiuem2k3/PBL6_Fakenews_Detection.git
pip install -r requirements.txt
```
### Huấn luyện mô hình:
- Huấn luyện mô hình dựa trên bộ data: [`DATA.rar`](./DATA/DATA.rar)
- Tham khoản code huấn luyện mô hình: [`CODE`](./CODE)
### Chạy ứng dụng:
Run python [`App.py`](./APP/App.py)

---

##  📞 Liên hệ
- 👥 Linkedin: [Thịnh Trần](https://www.linkedin.com/in/thinh-tran-04122k3/)

- 📧 Email: tttiuem2k3@gmail.com
