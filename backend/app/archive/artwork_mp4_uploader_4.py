from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# 웹드라이버 설정
driver = webdriver.Chrome()  # 또는 사용 중인 브라우저 드라이버로 대체

try:
    # Hailuo AI 웹사이트 접속
    driver.get("https://hailuoai.video/")

    # 비디오 생성 페이지로 이동
    driver.get("https://hailuoai.video/create")

    # 프롬프트 입력
    prompt_input = wait.until(EC.presence_of_element_located((By.ID, 'prompt')))
    prompt_input.send_keys("object is moving")

    # URL 이미지를 로컬 파일로 저장
    image_url = 'https://storage.googleapis.com/talkingart-bucket/temp_images/02_House_in_the_field.jpg'
    local_image_path = '/tmp/temp_image.jpg'
    with open(local_image_path, 'wb') as file:
        file.write(requests.get(image_url).content)

    # 이미지 업로드
    upload_button = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    upload_button.send_keys(local_image_path)

    # 모델 선택 (예: video-01-live2d)
    model_dropdown = driver.find_element(By.ID, 'model_select')
    model_dropdown.click()
    model_option = driver.find_element(By.XPATH, '//option[text()="video-01-live2d"]')
    model_option.click()

    # 비디오 생성 버튼 클릭
    generate_button = driver.find_element(By.ID, 'generate_video')
    generate_button.click()

    # 비디오 생성 완료 대기
    result = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'download_link')))
    download_url = result.get_attribute('href')
    print(f"[INFO] 비디오 생성 완료: {download_url}")

finally:
    # 브라우저 종료
    driver.quit()