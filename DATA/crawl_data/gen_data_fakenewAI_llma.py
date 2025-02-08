import pandas as pd
import os
from groq import Groq  
import random

# Danh sách các API key
api_keys = [
    "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",
    "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",
    "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"
]

# Hàm chọn API key ngẫu nhiên
def get_random_api_key():
    return random.choice(api_keys)

# Sử dụng hàm
api_key = get_random_api_key()

client = Groq(api_key=api_key)

# Đọc dữ liệu từ file news.csv
news_df = pd.read_csv('News.csv')

# Kiểm tra nếu fakenews.csv đã tồn tại
fake_news_file = 'fakenews2.csv'
if os.path.exists(fake_news_file):
    # Đọc dữ liệu từ file fakenews.csv
    fake_news_df_existing = pd.read_csv(fake_news_file)
    existing_sources = set(fake_news_df_existing['Source'].values)  # Lấy danh sách các nguồn đã tồn tại
else:
    # Tạo DataFrame rỗng nếu file chưa tồn tại
    fake_news_df_existing = pd.DataFrame(columns=['Title', 'Content', 'Source', 'Label', 'DateTime'])
    existing_sources = set()

# Danh sách để lưu dữ liệu tin giả mới
fake_news_data = []

# Sinh tin giả cho mỗi bài viết
i = 1
for index, row in news_df.iterrows():
    # Lấy tiêu đề và nội dung gốc
    original_title = str(row['Title'])
    original_content = str(row['Content'])
    article_source = row['Source']
    
    # Kiểm tra xem bài viết đã tồn tại trong fakenews.csv chưa (dựa trên Source)
    if article_source in existing_sources:
        print(f"Tin thứ {i} chạy bị trùng lặp!!!<-> {original_title[:40]} <-> {original_content[:40]}")
        i += 1
        continue  # Bỏ qua nếu bài viết đã tồn tại
    
    # Chuỗi yêu cầu sinh tin giả
    prompt = f"Sinh ra nội dung tin giả câu trả lời phải có số từ bằng nội dung tin thật, phải ở dạng: FakeTitle: abc FakeContent: xyz dựa trên tiêu đề và nội dung sau:\nTiêu đề: {original_title}\n\nNội dung: {original_content}"
    
    # Gọi API của Groq để sinh nội dung tin giả
    k=0
    while k==0:
        try:
            completion = client.chat.completions.create(
                model="llama-3.2-90b-text-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là một con bot sinh tin tức giả từ tin tức thật. \nBạn luôn trả lời bằng tiếng việt. Tin giả sinh ra có số từ phải bằng tin thật"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=2300,
                top_p=1,
                stream=True,
                stop=None
            )

            # Xử lý và lưu nội dung sinh ra
            fake_content = ""
            for chunk in completion:
                fake_content += chunk.choices[0].delta.content or ""
            
            # Tách phần FakeTitle và FakeContent
            title_start = fake_content.find("FakeTitle:") + len("FakeTitle:")
            content_start = fake_content.find("FakeContent:") + len("FakeContent:")
            fake_title = fake_content[title_start:content_start - len("FakeContent:")].strip()
            fake_content = fake_content[content_start:].strip()
            
            print(f"Tin thứ {i} đã chạy <-> {fake_title[:40]}... <-> {fake_content[:40]}...")
            
            # Lưu dữ liệu đã sinh vào danh sách
            fake_news_data.append({
                'Title': fake_title,  # Sử dụng tiêu đề giả
                'Content': fake_content,
                'Source': article_source,
                'Label': 'Fake',
                'DateTime': row['DateTime']
            })
            
            # Chỉ ghi dữ liệu nếu có bài viết mới
            if fake_news_data:
                # Tạo DataFrame mới cho dữ liệu tin giả mới
                fake_news_df_new = pd.DataFrame(fake_news_data)
                
                # Kết hợp dữ liệu cũ và mới (nếu file đã tồn tại)
                fake_news_df_combined = pd.concat([fake_news_df_existing, fake_news_df_new], ignore_index=True)
                
                # Lưu dữ liệu kết hợp vào file fakenews.csv
                fake_news_df_combined.to_csv(fake_news_file, index=False, encoding='utf-8')
            else:
                print("Không có dữ liệu tin giả mới để lưu.")
            k=1
        except Exception as e:
            k=0
            api_key = get_random_api_key()
            client = Groq(api_key=api_key)
            print(f"Lỗi sinh tin giả: tin thứ {i} chạy lại! {e}")
    i += 1