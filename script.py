

import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time

def scrape_coursesss(url, page):
    # Constants
    SLEEP_TIME = 1
    NUM_PAGES_TO_SCRAPE = page
    scraped_data = []

    try:
        # Initialize WebDriver
        driver = uc.Chrome(executable_path=ChromeDriverManager().install(), headless=True)
        print(driver)
        for current_page in range(1, NUM_PAGES_TO_SCRAPE + 1):
            COURSES_URL = f"{url}&page={current_page}"
            driver.get(COURSES_URL)
            time.sleep(SLEEP_TIME)

            # Get the list of all the courses' URLs on the current page
            courses = [
                link.get_attribute("href")
                for link in driver.find_elements(
                    By.XPATH, "//a[contains(@href, '/professional-certificates/') or contains(@href, '/learn/')or contains(@href, '/specializations/')]"
                )
               
            ]
            print(courses)
            unique_elements = list(set(courses))
            print(unique_elements)

            # Get details of each course on the current page
            for course_url in unique_elements:
                driver.get(course_url)
                time.sleep(SLEEP_TIME)
                title = driver.find_element(By.XPATH, "//h1").text
                description = "Description not available"
                description_elements = driver.find_elements(By.XPATH, "//div[@class='css-kd6yq1']/p ")
                for element in description_elements:
                   description_text = element.text.strip()
                   if description_text:
                       description = description_text
                       break  
                instructor = driver.find_element(
                     By.XPATH, "//span[contains(text(), 'Instructor')]"
                 ).text.replace("Instructor:", "")

                # Append course details to the list
                scraped_data.append({
                    "Title": title,
                    "URL": course_url,
                    "Description": description,
                    "Instructor": instructor
                })

                print(f"Scraping {title} on page {current_page}...")

        return scraped_data

    finally:
        # Quit the WebDriver and close resources
        driver.quit()
