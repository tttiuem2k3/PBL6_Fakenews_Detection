from transformers import ElectraTokenizer
import torch
from collections import Counter
from processing_data import preprocessing_data
from CustomELECTRAModel import CustomELECTRAModel, SlidingWindowPredictor

import warnings
# Tắt FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

#----------------------------------------------------------------------------
# Tải mô hình ELECTRA-Base đã huấn luyện
tokenizer_path = r'D:\Code\AI_project\fakenews_detection\MODEL\tokenizer'
tokenizer = ElectraTokenizer.from_pretrained(tokenizer_path)

# model_name='google/electra-base-discriminator' 
# tokenizer = ElectraTokenizer.from_pretrained(model_name)
# tokenizer.save_pretrained(r"D:\Code\PBL6_DuAnChuyenNganh\train\tokenizer")

model_path = r'D:\Code\AI_project\fakenews_detection\MODEL\fakenews_electra-base_model.pth'
model =torch.load(model_path, map_location=torch.device('cpu'))
model.eval()

#----------------------------------- Tạo đối tượng dự đoán---------------------------------
predictor = SlidingWindowPredictor(model, tokenizer, max_length=512, stride=128, device="cpu")

def predict(article_text):
    # Tiền xử lý cho đoạn văn bản
    process_text=preprocessing_data(article_text)
    # Lấy các dự đoán từ các cửa sổ trượt
    token_windows = predictor.sliding_window_tokenize(process_text)
    predictions = []
    predictor.model.eval()
    with torch.no_grad():
        for window in token_windows:
            inputs = {
                'input_ids': torch.tensor([window]).to(predictor.device),
                'attention_mask': torch.tensor([[1 if token != predictor.tokenizer.pad_token_id else 0 for token in window]]).to(predictor.device)
            }
            logits = predictor.model.forward(inputs['input_ids'], inputs['attention_mask'])
            predictions.append(torch.argmax(logits, dim=1).item())
    
    # Tính tỷ lệ phần trăm
    label_count = Counter(predictions)
    print(label_count)
    total_windows = len(predictions)
    percentage = {label: (count / total_windows) * 100 for label, count in label_count.items()}
    
    # Quyết định nhãn cuối cùng
    if label_count[0] == label_count[1]:
        final_label = 1
    else:
        final_label = label_count.most_common(1)[0][0]
    
    return "Real" if final_label == 0 else "Fake", percentage,process_text

#--------------------------Test------------------------------
# text="Tổng bí thư nguyễn phú trong vừa có chuyến thăm đến singapo trong tháng 9/2024, khi ông quay về đã tuyên bố chiến tranh. Tình hình hai bên trở nên căng thẳng"
# label, percentage,process_text= predict(text)
# print("\nNội dung bài báo: ",text)
# print("\nNội dung bài báo đã xử lý: ",process_text)
# print("\nNhãn dự đoán là: ",label)
# print("\nCác xác xuất là: ",percentage)