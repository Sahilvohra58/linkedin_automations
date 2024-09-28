import pandas as pd
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from linkedin_utils import login_linkedin, get_gpt_response_with_context, send_telegram_message
from selenium.webdriver.common.keys import Keys
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_client = OpenAI() 


profile = "real"

with open('linkedin_configs.json') as config_file:
    linkedin_configs = json.load(config_file)

profile_dict = linkedin_configs["profiles"][profile]
username = os.getenv(profile_dict["env_var"] + "_USERNAME")
password = os.getenv(profile_dict["env_var"] + "_PASSWORD")
linkedin_login_url = linkedin_configs["linkedin_login_url"]
notification_url = linkedin_configs["notification_url"]

telegram_api = "7186132763:AAHiIfZLvCEZ0f6XHj5nMuTI7tJrnK9Dfo4"
API_URL = f"https://api.telegram.org/bot{telegram_api}"
telegram_group_id = -4148825294

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(6000)
driver.get(linkedin_login_url)
driver.maximize_window()
driver.implicitly_wait(5) 

login_linkedin(driver=driver, username=username, password=password)
# if username!="greenarrowscaping@gmail.com":
# input("Enter verification if asked and press enter here")

while True:
    posts_to_comment_urls = []
    notification_elements = []

    try:
        driver.find_element(By.XPATH, f"//a[@href='{notification_url}']").click()
    except Exception as e:
        try:
            driver.get(notification_url)
        except Exception as e:
            message = f"Error in Logging or finding notification url - Quiting the code now: {e}"
            print(message)
            send_telegram_message(
                group_id=telegram_group_id, 
                message_text=message, 
                api_url=API_URL)
            break
    time.sleep(2)

    send_telegram_message(group_id=telegram_group_id,
                          message_text="login Successfull.!!!",
                          api_url=API_URL)
    
    for i in range(10):
        xpath = f"//div[@data-finite-scroll-hotkey-item='{i}']"
        notification_elements.append(driver.find_element(By.XPATH, xpath))

    if len(notification_elements) > 0:
        for element in notification_elements:
            try:
                p_element = element.find_element(By.XPATH, ".//p[contains(@class, 'nt-card__time-ago t-12 t-black--light t-normal')]")
                time_no, time_unit = p_element.text[:-1], p_element.text[-1]

                span_element = element.find_element(By.XPATH, ".//span[contains(@class, 'nt-card__text--3-line')]")
                notification_text = span_element.text

                a_element = element.find_element(By.XPATH, ".//a[contains(@class, 'nt-card__headline nt-card__text--word-wrap t-black t-normal text-body-small')]")
                notification_element_url =  a_element.get_attribute('href')
            
                if time_unit in ["m"] and " posted: " in notification_text:
                    if time_unit == "m" and int(time_no) > 15:
                        continue
                    # notification_text_split = notification_text.split(' posted: ')
                    # print(f"Author: {notification_text_split[0].strip()}")
                    # print(f"Text: {notification_text_split[1]}")
                    # print(f"Time: {time_no} {time_unit}")
                    # print("URL:", notification_element_url)
                    # print("\n")

                    posts_to_comment_urls.append(notification_element_url)

            except Exception as e:
                message = f"Error finding p element in div: {e}"
                print(message)
                send_telegram_message(
                    group_id=telegram_group_id, 
                    message_text=message, 
                    api_url=API_URL)


    if len(posts_to_comment_urls) > 0:
        for url in posts_to_comment_urls:
            try:
                driver.get(url)
                time.sleep(2)
                post_div = driver.find_elements(By.CLASS_NAME, "update-components-text.relative.update-components-update-v2__commentary")[0]
                post_text = post_div.text
                # print("Post Text: ", post_text)

                system_prompt = """
                    I have this LinkedIn post. I want to write a comment under it.
                    Don't put any inverted commas around the post.
                    write the comment small, one line only.
                    Don't put generic statements like 'in my experience' or 'from my experience'.
                    Don't put any inverted commas around the post.
                    User will give you the post text. and you will write a comment on it.
                    Don't put any prefix like 'Comment: ' or 'Comment:'. Just give the comment.
                """

                comment_text = get_gpt_response_with_context(system_prompt=system_prompt, user_prompt=post_text)
                comment_div = driver.find_element(By.XPATH, '//div[@data-placeholder="Add a comment…"]')
                comment_div.click()

                for character in comment_text:
                    comment_div.send_keys(character)
                    time.sleep(0.1)
                print("Comment Text: ", comment_text)

                time.sleep(2)
                
                # Locate the submit button and click it
                try:
                    driver.find_element(By.CLASS_NAME, "comments-comment-box__submit-button.mt3.artdeco-button.artdeco-button--1.artdeco-button--primary.ember-view").click()
                except Exception as e:
                    driver.find_element(By.XPATH, '//button[@class="comments-comment-box__submit-button--cr artdeco-button artdeco-button--1 artdeco-button--primary ember-view"]').click()
                time.sleep(2)

                send_telegram_message(
                    group_id=telegram_group_id, 
                    message_text=f"Commented on post: {url} with comment: {comment_text}", 
                    api_url=API_URL)

                try:
                    react_like_button = driver.find_element(By.XPATH, '//button[@aria-label="React Like"]')
                    react_like_button.click()
                except Exception as e:
                    print(f"Error finding react like button: {e}")
                
                time.sleep(2)

            except Exception as e:
                message = f"Error trying to comment on post {url}: {e}"
                print(message)
                send_telegram_message(
                    group_id=telegram_group_id, 
                    message_text=message, 
                    api_url=API_URL)
    
    time.sleep(900)


send_telegram_message(
                    group_id=telegram_group_id, 
                    message_text="Program stopped. Please check!!", 
                    api_url=API_URL)
