import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox
import tkinter as tk
# Đường dẫn tới ChromeDriver
chrome_driver_path = r'D:\Code\PBL6_DuAnChuyenNganh\chromedriver-win64\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Đường dẫn tới file CSV
csv_file_path = 'fakenews.csv'

# Hàm kiểm tra nếu file CSV đã tồn tại và chứa bài báo
def article_exists(article_url, csv_path):
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        return article_url in df_existing['Source'].values  # Kiểm tra nếu URL đã có trong cột "Source"
    return False

# Truy cập vào URL trang Thời sự Viettan
k=1 # để hiển thị bài viết thứ bao nhiêu
i=1 # chạy từ page nào đến page nào
while i<=60:
    page=str(i)
    url = 'https://viettan.org/quan-diem/page/'+page +'/'
    driver.get(url)

    # Đợi trang tải đầy đủ (bao gồm JavaScript)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))

    # Lấy tất cả các bài báo từ trang
    articles = driver.find_elements(By.TAG_NAME, 'article')

    # Danh sách để lưu các link bài báo
    article_links = []

    # Duyệt qua từng bài báo để lấy href của thẻ <a>
    for article in articles:
        try:
            # Lấy thẻ <a> trong bài báo
            link_element = article.find_element(By.TAG_NAME, 'a')
            
            # Lấy thuộc tính href
            href = link_element.get_attribute('href')

            # Thêm vào danh sách các đường link
            article_links.append(href)
        except Exception as e:
            print(f"Error extracting href: {e}")

    # Duyệt qua từng link để truy cập và lấy tiêu đề, nội dung, và ngày đăng
    
    for link in article_links:
        if article_exists(link, csv_file_path):
            print(f"Bài báo thứ {k} đã tồn tại => bỏ qua: {link[0:100]}")
            k+=1
            continue
        try:
            # Truy cập vào đường link của từng bài báo
            driver.get(link)

            # Đợi trang tải và tìm tiêu đề bài viết
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

            # Lấy tiêu đề bài viết (giả sử tiêu đề nằm trong thẻ <h1>)
            title = driver.find_element(By.TAG_NAME, 'h1').text

            # Lấy ngày đăng bài viết (từ thẻ span với class cụ thể)
            date_element = driver.find_element(By.CLASS_NAME, 'elementor-icon-list-text.elementor-post-info__item--type-date')
            publication_date = date_element.text

            # Lấy nội dung bài viết (tất cả thẻ <p> nằm trong div có class 'elementor-widget-container')
            content_elements = driver.find_elements(By.CSS_SELECTOR, 'div.elementor-widget-container p')
            content = '\n'.join([p.text for p in content_elements])  # Gộp nội dung từ các thẻ <p>

            # Tạo dataframe với dữ liệu mới
            df_new = pd.DataFrame({
                'Title': [title],
                'Content': [content],
                'Source': [link],  # Lưu trực tiếp link bài viết
                'Label': 'Fake',  # Cột nhãn để thêm "real" hoặc "fake"
                'DateTime': [publication_date]  # Ngày, giờ đăng bài
            })

            # Kiểm tra nếu file đã tồn tại thì append thêm dữ liệu
            if os.path.exists(csv_file_path):
                df_existing = pd.read_csv(csv_file_path)
                # Append dữ liệu mới vào file
                df_new.to_csv(csv_file_path, mode='a', header=False, index=False, encoding='utf-8')
            else:
                # Nếu file chưa tồn tại thì tạo file mới với header
                df_new.to_csv(csv_file_path, mode='w', header=True, index=False, encoding='utf-8')

            print(f"Page {i} đang chạy - Bài báo thứ {k} đã được lưu với ===> Tiêu đề: {title[0:20]} <=> Content: {content[0:25]}")
            k+=1
        except Exception as e:
            print(f"Bài báo thứ {k} - Lỗi tải link: {link[0:100]} <====> {e}")
    i+=1
# Đóng trình duyệt

driver.quit()

