import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager

from pathlib import Path
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# import
import re
import os
import sys
import json


COURSES_URL = "https://www.udemy.com/courses/development/web-development/"
SLEEP_TIME = 1
BASE_PATH = Path(__file__).resolve().absolute().parent

driver = uc.Chrome(executable_path=ChromeDriverManager().install(), headless=True)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"})
driver.get(COURSES_URL)

time.sleep(SLEEP_TIME)

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
print(driver)
courses = [
    link.get_attribute("href")
   
    for link in driver.find_elements(
       By.XPATH, "//h3[contains(@class, 'course-card-title-module')]/a"
    )

]
print(courses)

# Get details of each course
course_details = []
for url in courses:
    course = {}
    driver.get(url)
    time.sleep(SLEEP_TIME)
    title = driver.find_element(By.XPATH, "//h1[contains(@class, 'title')]").text
    course["title"] = title
    course["url"] = url
    try:
        description = driver.find_element(
            By.XPATH, "//div[contains(@class, 'lead__headline')]"
        ).text
        course["description"] = description
    except Exception as e:
        print(e)
        
    instructor = driver.find_element(
        By.XPATH, "//a[contains(@class, 'instructor')]/span"
    ).text.replace("Instructor:", "")
    course["instructor"] = instructor
    course_details.append(course)
    print(f"Scraping {title}...")

with open(os.path.join(BASE_PATH, "data.json"), "w") as f:
    print("\n\nWriting to file...")
    json.dump(course_details, f, indent=4)
