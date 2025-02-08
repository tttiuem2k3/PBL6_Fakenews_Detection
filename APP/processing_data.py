#--------------------Thư viện cần thiết------------------------
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import re
import os

#--------------------Tải mô hình tiền xử lý data ( word_segmentation )------------------------

# Load mô hình segmentation cho văn bản tiếng việt
# tokenizer_seg = AutoTokenizer.from_pretrained("NlpHUST/vi-word-segmentation")
# model_1 = AutoModelForTokenClassification.from_pretrained("NlpHUST/vi-word-segmentation")
# nlp = pipeline("token-classification", model=model_1, tokenizer=tokenizer_seg)
# Lưu lại mô hình
# save_directory = r"D:\Code\AI_project\fakenews_detection\DATA\Processing_model"
# model_1.save_pretrained(save_directory)
# tokenizer_seg.save_pretrained(save_directory)

# Thư mục để lưu model và tokenizer
save_directory = r"D:\Code\AI_project\fakenews_detection\DATA\Processing_model"
# Nạp mô hình và tokenizer từ thư mục lưu trữ
tokenizer_seg = AutoTokenizer.from_pretrained(save_directory)
model_1 = AutoModelForTokenClassification.from_pretrained(save_directory)
nlp = pipeline("token-classification", model=model_1, tokenizer=tokenizer_seg)

#-----------------Hàm nối các từ đã tách(word_segmentation) lại thành câu-----------------------
def word_weg(text):
  ner_results = nlp(text)
  example_tok = ""
  for e in ner_results:
      if "##" in e["word"]:
          example_tok = example_tok + e["word"].replace("##","")
      elif e["entity"] =="I":
          example_tok = example_tok + "_" + e["word"]
      elif ("." in e["word"]) or ("/" in e["word"]) or ("%" in e["word"]) or ("-" in e["word"]):
        example_tok = example_tok + "" + e["word"]
      else:
        example_tok = example_tok + " " + e["word"]
  return example_tok

#-----------------------Hàm cắt câu dài hơn 512 tokens-----------------------------

def split_sentence_into_chunks(sentence, max_length=512):
    """Cắt câu dài thành các đoạn nhỏ hơn hoặc bằng max_length ký tự."""
    chunks = []
    while len(sentence) > max_length:
        # Tìm vị trí dấu cách gần nhất trước giới hạn max_length
        split_pos = sentence[:max_length].rfind(" ")
        if split_pos == -1:  # Nếu không tìm thấy dấu cách
            split_pos = max_length
        chunks.append(sentence[:split_pos].strip())
        sentence = sentence[split_pos:].strip()
    if sentence:  # Thêm phần còn lại của câu
        chunks.append(sentence)
    return chunks

#--------------------Hàm cắt câu dài hơn 512 tokens-----------------------

def split_text_with_long_sentences(text, max_length=512):
    """Cắt văn bản thành nhiều đoạn nhỏ hơn hoặc bằng max_length ký tự, bao gồm cả câu dài."""
    text = text.strip()
    sentences = re.split(r'(?<=[.])', text)  # Tách theo câu, giữ lại dấu chấm
    chunks = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > max_length:
            # Nếu câu vượt quá max_length, cắt thành các đoạn nhỏ
            chunks.extend(split_sentence_into_chunks(sentence, max_length))
        else:
            # Nếu câu không vượt quá max_length, thêm vào danh sách
            chunks.append(sentence)
    return chunks

#-----------------------Hàm tiền xử lý cho text-------------------------------

def preprocessing_text(text):
    # lower text
    text = text.lower()

    # remove special char
    allowed_special_chars = r"%"
    allowed_chars = r"[^a-zA-Z0-9\s" + re.escape(allowed_special_chars) + r"àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]"
    text = re.sub(allowed_chars, '', text)

    # word segmentor
    text = word_weg(text)

    # remove stop word
    with open(r'D:\Code\AI_project\fakenews_detection\DATA\vietnamese.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().strip().split('\n'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    text =' '.join(filtered_words)

    return text

#-----------------------------------Hàm chính------------------------------------

def preprocessing_data(text):

    sentences = split_text_with_long_sentences(text, max_length=512)

    # Loại bỏ các câu rỗng hoặc chỉ chứa khoảng trắng
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # Nối kết quả sau xử lý bằng dấu cách
    text = " ".join(preprocessing_text(sentence) for sentence in sentences)
    return text

#-------------------------------Test-----------------------------------
# text="Tổng bí thư nguyễn Phú trọng đã có chuyến thăm cấp độ nhà nước đến SIngapo vào nhiệm kỳ thứ 2 năm 2024"
# print("Câu gốc: ", text)
# text= preprocessing_data(text)
# print("Câu đã xử lý: ", text)
