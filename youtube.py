from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
# Initialize the web driver
# driver = webdriver.Firefox()

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument('--headless')
# URL to fetch
# url = 'https://www.youtube.com/watch?v=5OPShZJkJR8'

class FetchTranscript:
    def __init__(self,url) -> None:
        self.url = url
        self.driver = webdriver.Chrome(options=options)

    def get_text(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(15)
        try:
            # finding the more button
            self.driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]').click()  #clicking to the X.
            # print("success clicked on more button")
        except NoSuchElementException:
            print("Error while clicking 'more' button")
            pass 
        try:
            self.driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/div[2]/ytd-structured-description-content-renderer/div/ytd-video-description-transcript-section-renderer/div[3]/div/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click()
            # print("success clicked on Transcript button")
        except NoSuchElementException:
            print("Error while clicking 'transcript' button")
            pass
        text = None
        try:
            div_elements = self.driver.find_elements(By.CLASS_NAME, 'segment-text.style-scope.ytd-transcript-segment-renderer')
            if div_elements:
                # print(len(div_elements))
                div_texts = [div_element.text for div_element in div_elements]
                # print(div_texts)
                single_line_text = ' '.join(div_texts)
                text = single_line_text
                self.driver.quit()
            pass
        except NoSuchElementException:
            pass

        return text


# temp = FetchTranscript(url= "https://www.youtube.com/watch?v=8UryASGBiR4&t=7s")
# text = temp.get_text()
# print(text)