import pandas as pd
import time
import json
from selenium import webdriver
from linkedin_utils import login_linkedin, get_element, input_text_in_element, press_escape
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os

load_dotenv()


profile = "real"
photos_to_post_path = "/Users/savohra/Desktop/galgadot.jpeg"

with open('linkedin_configs.json') as config_file:
    linkedin_configs = json.load(config_file)

profile_dict = linkedin_configs["profiles"][profile]
username = os.getenv(profile_dict["env_var"] + "_USERNAME")
password = os.getenv(profile_dict["env_var"] + "_PASSWORD")
all_groups = profile_dict["groups"]
linkedin_login_url = linkedin_configs["linkedin_login_url"]
linkedin_feed = linkedin_configs["linkedin_feed"]


x_paths_dict = {
    "post_text_button": '//span[@class="truncate block text-align-left"]',
    "post_writing_division": '//div[@data-placeholder="What do you want to talk about?"]',
    "change_post_visibility_button":'//*[local-name()="svg" and @data-test-icon="caret-medium"]',
    # "groups_selection_button": '//*[local-name()="svg" and @data-test-icon="group-medium"]',
    "groups_selection_button": '//button[@id="CONTAINER"]',
    "group_selection": '//span[text()="{group_name}" and @class="sharing-shared-generic-list__description-single-line"]',
    "save_button": '//span[text()="Save"]',
    "done_button": '//span[text()="Done"]',
    "image_selection_button": '//*[local-name()="svg" and @data-test-icon="image-medium"]',
    "upload_input_button": '//input[@id="media-editor-file-selector__file-input"]',
    "next_button":'//span[text()="Next"]',
    "post_button":'//span[text()="Post"]',
    }


# # all_groups = ["test temp grp", "temt temp grp 2"]
# all_groups = [
#     "BIG DATA: Telecom, Intelligence, Analytics, Security, Science, Machine Learning, AI, IoT, Blockchain", "Python Developers: Machine Learning, Artificial Intelligence, Data Engineering, & Programming", "Business Analyst Professional - BA, Analysis, Data Analyst, Data Scientist, AI", "JavaScript", "Artificial Intelligence, Machine Learning, Data Science, Robotics, Gen AI, Data Scientist & Analyst", "Analytics and Artificial Intelligence (AI) in Marketing and Retail", "Data Science Community (moderated)",
#     "Data Science and AI for Decision Makers, Executives and Entrepreneurs", "Data Science & Gen AI Analytics: Artificial Intelligence, Machine Learning, MLOps, XAI, AutoML, GPT", "Software Engineer, Data Scientist, Business Analyst, Gen AI, Python Developer, ML Engineer, Analysis", "Machine Learning Community (Moderated)", "Big Data 🟥 Data Science | Machine Learning | Deep Learning | Artificial Intelligence", "Artificial Intelligence, Deep Learning, Machine Learning", "Future Technology & Artificial Intelligence: AI, Robotics, Blockchain, No-Code, VR, Web3 | Metaverse", "Artificial Intelligence, Machine Learning, Data Science & Robotics", "Open Source & Artificial Intelligence | Machine Learning - OpenAI, ChatGPT, RAG, Gemini, Python, NLP", "Data Science, Open AI, ML : Data Scientist & Analyst, Python Developer, Power BI, Tableau Engineer,", "RMDS (Research Methods, Data Science and AI)", "Machine Learning, Artificial Intelligence, Deep Learning, Computer Vision, Robotics, DataOps, Gen AI", "AI for Marketing | Artificial Intelligence Industry Startups Scaleups Innovation Investment Tech", "Artificial Intelligence & Machine Learning: Gen AI Developer, ML Engineer, Data Scientist & Analyst", "Data Analytics, Data Science, Gen AI, ML, NLP, Power BI, Tableau, SQL, AWS, Azure, MongoDB, Python", "AI Professionals 🟥 Engineering | ML/DL | NLP | LLMs | Prompt | MLOps | Data Science | DataOps AIOps", "Artificial Intelligence and Business Analytics (AIBA) Group", "MACHINE LEARNING, DATA SCIENCE, RPA, IOT, QUANTUM COMPUTING, BLOCKCHAIN, Cybersecurity & AI  NETWORK", "KDnuggets Data Science & Machine Learning (Moderated)", "Artificial Intelligence Investors Group: Robotics, AI & IoT, Machine Learning, NLP & Computer Vision", "Artificial Intelligence (AI) - Machine Learning, Deep Learning, NLP, Computer Vision & Data Science", "AI/CC :: Artificial Intelligence Creative Community", "Data Science, AI & ML Community : Data Scientist, Business Analyst, Data Engineer & Python Developer",
#     "AI / ML,Gen AI & DATA Analytics, Data Science . SAP BI/ Analytics Cloud /Tableau /Power BI /Birst", "Artificial Intelligence Innovators, AI, ChatGPT, Gemini, Bing, Copilot & Machine Learning Innovation", "Data Science | Machine Learning | Artificial Intelligence | Big Data | Data Scientist | Blockchain", "Technology Investor Group: FinTech, Artificial Intelligence, Machine Learning, ChatGPT, Blockchain", "Data Mining, Statistics, Big Data, Data Visualization, AI, Machine Learning, and Data Science", "Power BI, AI Analytics, Business Intelligence, Data Science, Analysis, Dashboard, Scientist, Analyst", "AI (Artificial Intelligence) VR (Virtual Reality) Metaverse Robotics Blockchain Web3 - iTechScope", "Artificial Intelligence 🟥", "Big Data - Data Warehouse - IoT - Cloud - AI - Machine Learning - Blockchain", "Computer Vision,Generative AI,Edge Computing,Fine-tune Multimodal LLMs,Robotics,IoT,AR/VR,Medical", "Gen AI & Machine Learning: Data Science, Analytics, ML, NLP, GPT, Prompt Engineering, Robotics & IoT", "AI & ML - Deep Learning, Machine Learning, Artificial Intelligence, Data Science, Big Data Analytics", "Python, Data Analysis, Tableau, Power BI, SQL, Data Science, Statistics, Business Analytics, AI & ML", "Python Developers Community (moderated)", "Technology Leadership 🟥 IT, Artificial Intelligence AI, Big Data, Cybersecurity, Web3, Metaverse 5g", "QuantSpeak and Data Science", "AI Africa | African Artificial Intelligence OpenAI ChatGPT Machine Learning Startups Innovation Tech", "Data Analytics, AI, ML, Data Science, Power BI, Python Developer, Data Scientist & Business Analyst", "Data Science and Artificial Intelligence", "R Programming & Data Science (Moderated by Statistics Globe)", "Data Science, Machine Learning & AI", "Data Science and Analytics Resource", "Artificial Intelligence, Deep & Machine Learning, AI, Big Data, Virtual Assistants,Chatbots", "Machine Learning and Data Science", "AI & ML Data Scientist, Data Analyst, Data Engineer, Python Developer, Software Full Stack Developer", "Women in Data Science (WiDS)", "Data Science in Healthcare", "Data Warehouse - Big Data - Business Intelligence - Cloud - Data Science - ETL",
#     "Data Science Central", "Gen AI & Machine Learning, Data Scientist, Data Analyst, Python Software Engineer, ML Data Analytics", "AI, ML, Data Science & Analytics: Data Engineer, Data Scientist, Data Analyst, Python & AI Developer", "Cybersecurity and Artificial Intelligence (AI) Frameworks and Maturity Models", "Hot Science- AI | Tech | Robotics | Data | Health | Economics | Space | Earth | Sports | Eng", "Tech Startup CEOs & Investors: Artificial Intelligence, Machine Learning, FinTech, SaaS, ChatGPT", "Advanced Analytics and Data Science", "Artificial Intelligence | Data Science | Quantum", "Software/Technology: AI, Marketing, Social Media, Startups, Blockchain, Human Resources & Metaverse"
# ]


driver = webdriver.Firefox()
driver.set_page_load_timeout(6000)
driver.get(linkedin_login_url)
driver.maximize_window()
driver.implicitly_wait(5) 

login_linkedin(driver=driver, username=username, password=password)
# if username!="greenarrowscaping@gmail.com":
input("Enter verification if asked and press enter here")
time.sleep(3)

for group_name in all_groups:
    driver.get(linkedin_feed)

    try:
        get_element(driver=driver, element_xpath=x_paths_dict["post_text_button"]).click()
        
        # input_text_in_element(element=post_writing_element, text=text_to_post)
        get_element(driver=driver, element_xpath=x_paths_dict["change_post_visibility_button"]).click()
        
        get_element(driver=driver, element_xpath=x_paths_dict["groups_selection_button"]).click()

        time.sleep(2)
        get_element(driver=driver, element_xpath=x_paths_dict["group_selection"].format(group_name=group_name)).click()
        get_element(driver=driver, element_xpath=x_paths_dict["save_button"]).click()
        get_element(driver=driver, element_xpath=x_paths_dict["done_button"]).click()

        get_element(driver=driver, element_xpath=x_paths_dict["image_selection_button"]).click()
        get_element(driver=driver, element_xpath=x_paths_dict["upload_input_button"]).send_keys(photos_to_post_path)

        get_element(driver=driver, element_xpath=x_paths_dict["next_button"]).click()

        post_writing_element = get_element(driver=driver, element_xpath=x_paths_dict["post_writing_division"])
        post_writing_element.click()
        post_writing_element.send_keys(Keys.COMMAND + 'v')

        get_element(driver=driver, element_xpath=x_paths_dict["post_button"]).click()
    
    except Exception as E:
        print(f"Got Error posting to group - {group_name} - {E}")
    
    time.sleep(5)

input("Press enter to quit")
driver.quit()
