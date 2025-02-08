from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Đường dẫn đến ChromeDriv
driver_path = r'D:\Code\PBL6_DuAnChuyenNganh\chromedriver-win64\chromedriver.exe' 
chrome_binary_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"# Thay "path/to/chromedriver" bằng đường dẫn thực tế
output_file = "urls.txt"  # File để lưu các URL

def khoitao_gg():
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary_path

    # Khởi tạo ChromeDriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
# Tùy chọn Chrome

# URL bắt đầu
start_url = "https://danlambaovn.blogspot.com/search?updated-max=2013-07-22T08%3A05%3A00%2B07%3A00&max-results=50#PageNo=520"
ton_tai=False
try:
    driver= khoitao_gg()
    driver.get(start_url)
    for _ in range(200):  # Giới hạn duyệt 100 trang
        # Lấy URL hiện tại và thêm vào danh sách
        current_url = driver.current_url
        # Kiểm tra xem URL đã có trong file chưa
        with open(output_file, "r", encoding="utf-8") as file:
            if current_url in file.read():
                print(f"URL đã tồn tại: {current_url}")
                ton_tai=True
            else:
                ton_tai=False
        if ton_tai==False:
            with open(output_file, "a", encoding="utf-8") as file:
                file.write(current_url + "\n")
            print(f"Đã thêm URL: {current_url}")
        
        # Tìm nút '>' để chuyển sang trang tiếp theo
        try:
            next_button = driver.find_element(By.XPATH, "//a[normalize-space(text())='>']")
            next_button.click()
            time.sleep(2.5)  # Đợi trang tải
        except Exception as e:
            print("Không tìm thấy nút '>' hoặc đã hết trang.")
            driver.quit()
            driver= khoitao_gg()
            driver.get(current_url)
            continue
finally:
    # Đóng trình duyệt
    driver.quit()

print(f"Đã hoàn tất lưu URL vào file '{output_file}'.")