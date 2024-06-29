import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from settings.config import FREELANCER_USER_NAME, FREELANCER_PASSWORD, CHROME_VERSIONS, MAX_ATTEMPTS

def create_database():
    conn = sqlite3.connect('freelancer_jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (title TEXT, description TEXT, proposals INTEGER)''')
    conn.commit()
    conn.close()

def login(driver):
    driver.get("https://www.freelancer.com/login")
    time.sleep(2)
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(FREELANCER_USER_NAME)
    password_input.send_keys(FREELANCER_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)

def scrape_jobs(driver):
    driver.get("https://www.freelancer.com/jobs")
    time.sleep(2)
    jobs = driver.find_elements(By.CLASS_NAME, "JobSearchCard-item")
    job_data = []
    for job in jobs:
        title = job.find_element(By.CLASS_NAME, "JobSearchCard-primary-heading-link").text
        description = job.find_element(By.CLASS_NAME, "JobSearchCard-primary-description").text
        proposals = job.find_element(By.CLASS_NAME, "JobSearchCard-secondary-entry").text
        job_data.append((title, description, proposals))
    return job_data

def save_jobs_to_db(job_data):
    conn = sqlite3.connect('freelancer_jobs.db')
    c = conn.cursor()
    c.executemany('INSERT INTO jobs VALUES (?, ?, ?)', job_data)
    conn.commit()
    conn.close()

def main():
    create_database()
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    try:
        login(driver)
        job_data = scrape_jobs(driver)
        save_jobs_to_db(job_data)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
