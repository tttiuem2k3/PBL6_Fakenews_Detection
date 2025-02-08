import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox

# Hàm để đọc danh sách URL từ tệp urls.txt
def read_main_urls(file_name='urls.txt'):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            main_urls = [line.strip() for line in f if line.strip()]
        return main_urls
    else:
        messagebox.showerror("Lỗi", f"Tệp {file_name} không tồn tại!")
        return []
    
# Hàm để lấy danh sách link bài viết từ trang chính
def get_article_links(main_url):
    response = requests.get(main_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Giả sử các link bài viết nằm trong thẻ <article> và có chứa thẻ <a>
        article_tags = soup.find_all('div',class_='date-outer')  # Sửa lại nếu cấu trúc web khác
        article_links = []
        for article in article_tags:
            a_tag = article.find('a', href=True)  # Tìm thẻ <a> có thuộc tính href
            if a_tag:
                article_links.append(a_tag['href'])  # Thêm link vào danh sách
        return article_links
    else:
        messagebox.showerror("Lỗi", f"Không thể truy cập trang web. Mã trạng thái: {response.status_code}")
        return []

# Hàm xử lý dữ liệu từ từng bài viết
def save_data():
    
     # Tên file CSV
    csv_file = 'Fake_danlambao.csv'
    # Kiểm tra nếu file CSV đã tồn tại
    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file, encoding='utf-8')
    else:
        df_existing = pd.DataFrame(columns=['Title', 'Content', 'Source', 'Label', 'DateTime'])
        
    # Đọc danh sách main_url từ tệp urls.txt
    main_urls = read_main_urls()
    if not main_urls:
        print("Danh sách URL chính trống hoặc không hợp lệ.")
        return
    
    page=1   
    baibaothu_ofpage=1
    for main_url in main_urls:
    
        # Lấy danh sách các link bài viết từ trang chính
        article_links = get_article_links(main_url)
        
        if not article_links:
            print(f"Page {page} :Không tìm thấy bài viết nào!")
            page+=1
            continue
            
        # Duyệt qua từng link bài viết và lấy dữ liệu
        for article_url in article_links:
            # Tạo URL đầy đủ nếu link là tương đối
            if not article_url.startswith('http'):
                article_url = main_url.rstrip('/') + '/' + article_url.lstrip('/')

            # Kiểm tra xem link đã tồn tại trong CSV chưa
            if article_url in df_existing['Source'].values:
                print(f"Page {page}: Bài báo thứ {baibaothu_ofpage} đã tồn tại trong dữ liệu => bỏ qua")
                baibaothu_ofpage+=1
                continue  # Nếu đã tồn tại thì bỏ qua

            # Gửi yêu cầu đến từng bài viết
            response = requests.get(article_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Lấy tiêu đề bài viết
                title_tag = soup.find('h2', class_='post-title entry-title')  # Sửa nếu web khác
                if title_tag:
                    title = title_tag.text.strip() 
                    if title=="":
                        print(f"Page {page}: Bài báo thứ {baibaothu_ofpage} không có tiêu đề! => bỏ qua") 
                        baibaothu_ofpage+=1
                        continue    
                else:
                    print(f"Page {page}: Bài báo thứ {baibaothu_ofpage} không tìm thấy tiêu đề! => bỏ qua") 
                    baibaothu_ofpage+=1
                    continue

                # Lấy nội dung bài viết
                content_tag = soup.find('div', class_="post-body entry-content")  # Sửa nếu web khác
                if content_tag:
                    # paragraphs = content_tag.find_all('div', style_="text-align: justify;")
                    paragraphs = content_tag.find_all('div')
                    content = '\n'.join([para.text.strip() for para in paragraphs if para.text.strip()!=""])
                    if content=="":
                        print(f"Page {page}: Bài báo thứ {baibaothu_ofpage} không có nội dung! => bỏ qua") 
                        baibaothu_ofpage+=1
                        continue
                else:
                    print(f"Page {page}: Bài báo thứ {baibaothu_ofpage} không tìm thấy nội dung! => bỏ qua") 
                    baibaothu_ofpage+=1
                    continue

                # Lấy ngày, giờ đăng bài (sửa theo cấu trúc trang cụ thể)
                date_tag = soup.find('abbr', class_='published')  # Sửa nếu web khác
                if date_tag:
                    published_date = date_tag.text.strip()
                    if published_date=="":
                        print(f"Page {page}: Bài báo thứ {baibaothu_ofpage} không có ngày đăng! => bỏ qua") 
                        baibaothu_ofpage+=1
                        continue
                else:
                    print(f"Page {page}: Bài báo thứ {baibaothu_ofpage} không tìm thấy ngày đăng! => bỏ qua") 
                    baibaothu_ofpage+=1
                    continue
                
                # Tạo DataFrame với dữ liệu mới
                df_new = pd.DataFrame({
                    'Title': [title],
                    'Content': [content],
                    'Source': [article_url],  # Lưu trực tiếp link bài viết
                    'Label': "Fake",  # Cột nhãn để thêm "real" hoặc "fake"
                    'DateTime': [published_date]  # Ngày, giờ đăng bài
                })
                print(f"Page {page} - bài báo thứ {baibaothu_ofpage} đã được crawl: {title[0:40]} --- {content[0:40]}")
                
                # Kết hợp dữ liệu hiện có với dữ liệu mới
                df_existing = pd.concat([df_existing, df_new], ignore_index=True)

            else:
                print(f"Không thể truy cập bài báo thứ {baibaothu_ofpage}. Mã trạng thái: {response.status_code}")
            baibaothu_ofpage+=1
        page+=1
        
        # Lưu dữ liệu vào file CSV với encoding utf-8
        df_existing.to_csv(csv_file, index=False, encoding='utf-8')
        
    print(f"Dữ liệu đã được lưu vào {csv_file}")

save_data()