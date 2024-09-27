import pandas as pd
import time
from selenium import webdriver
from linkedin_utils import login_linkedin, get_all_questions_dataframe, click_tab, click_question, click_start_contribution, write_contribution, get_gpt_response

linkedin_login_url = "https://www.linkedin.com/login"
# username="greenarrowscaping@gmail.com"
# password="Vadodara@1"

username="vohrasahil58@gmail.com"
password="Ahmed1397"

questions_directory = "https://www.linkedin.com/pulse/topics/browse/"
tab_name = "Machine Learning"
# tab_name = "Data Science"
# tab_name = "Artificial Intelligence (AI)"
questions_directory = questions_directory + tab_name[0].lower() + "/"
question_file_name = f"allQuestions_{tab_name}.csv"

driver = webdriver.Firefox()
driver.get(linkedin_login_url)
driver.maximize_window()
driver.implicitly_wait(5) 


login_linkedin(driver=driver, username=username, password=password)
# input("Enter verification if asked and press enter here")


driver.get(questions_directory)
time.sleep(5) 
click_tab(driver=driver, tab_name=tab_name)
all_questions_df = get_all_questions_dataframe(driver=driver)
all_questions_df.to_csv(question_file_name, index=False)

print("==> All questions extracted")

all_questions_df = pd.read_csv(question_file_name)


for question in all_questions_df["questions"].to_list()[3:]:
    try:
        print("...QUESTION...")
        print(question)

        driver.get(questions_directory)
        driver.implicitly_wait(5) 
        click_tab(driver=driver, tab_name=tab_name)    
        click_question(driver=driver, question=question)
        click_start_contribution(driver=driver)
        answer = get_gpt_response(question=question)

        print("...ANSWER...")
        print(answer)
        write_contribution(driver=driver, answer=answer)
    
    except Exception as E:
        print(f"Cannot write contribution for question - {question}. Error - {E}")

driver.quit()
