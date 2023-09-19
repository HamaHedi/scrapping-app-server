import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pathlib import Path
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def scrape_udemy_courses(url, page):
    SLEEP_TIME = 3
    course_details = []

    # Initialize WebDriver
    driver = uc.Chrome(executable_path=ChromeDriverManager().install(), headless=True)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"})

    for page in range(1, page + 1):
        COURSES_URL = f"{url}?p={page}"
        driver.get(COURSES_URL)
        time.sleep(SLEEP_TIME)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        print(f"Scraping courses from page {page}...")

        courses = [
            link.get_attribute("href")
            for link in driver.find_elements(By.XPATH, "//h3[contains(@class, 'course-card-title-module--course-title')]/a")
        ]
        print(courses)
        # Get details of each course
        for course_url in courses:
            course = {}
            driver.get(course_url)
            time.sleep(SLEEP_TIME)
            title = driver.find_element(By.XPATH, "//h1[contains(@class, 'title')]").text
            price = driver.find_element(By.XPATH, "//div[contains(@class, 'price-text')]/span[2]").text
            print(price)
            course["title"] = title
            course["price"] = price

            course["url"] = course_url
            # course["price"] = price

            try:
                description = driver.find_element(By.XPATH, "//div[contains(@class, 'lead__headline')]").text
                course["description"] = description
            except Exception as e:
                print(e)
                
            instructor = driver.find_element(By.XPATH, "//a[contains(@class, 'instructor')]/span").text.replace("Instructor:", "")
            course["instructor"] = instructor
            course_details.append(course)

    # Quit the WebDriver
    driver.quit()

    return course_details
