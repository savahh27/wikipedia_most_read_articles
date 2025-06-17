import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import pandas as pd
import time
from functions.picking_date_functions import *

class Bot:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")

        self.driver = uc.Chrome(options=options)

    def run(self):
        self.driver.get("https://pageviews.toolforge.org/topviews/")

    def set_language(self, preferredLanguage="English"):
        wait = WebDriverWait(self.driver, 10)
        dropdowns = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-toggle="dropdown"]')))
        dropdowns = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-toggle="dropdown"]')
        for dropdown in dropdowns:
            if not dropdown.find_elements(By.CSS_SELECTOR, 'svg[xmlns="http://www.w3.org/2000/svg"]'):
                dropdowns.remove(dropdown)
        changeLanguageButton = dropdowns[0]
        changeLanguageButton.click()

        dropdownMenus = self.driver.find_elements(By.CLASS_NAME, 'dropdown-menu-right')
        dropdownMenus = [dropdownMenu for dropdownMenu in dropdownMenus if dropdownMenu.find_elements
                         (By.CSS_SELECTOR, "a[href='https://translatewiki.net/w/i.php?title=Special:MessageGroupStats&group=out-pageviews']")]
        dropdownMenu = dropdownMenus[0]
        languages = dropdownMenu.find_elements(By.CLASS_NAME, "lang-link")
        languageButton = [language for language in languages if language.text == preferredLanguage]
        englishButton = [language for language in languages if language.text == "English"]
        if languageButton == []:
            englishButton[0].click()
        else:
            languageButton[0].click()

    def set_to_daily(self):
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "main.processing")))
        select_element = wait.until(EC.element_to_be_clickable((By.ID, "date-type-select")))
        select = Select(select_element)
        select.select_by_value("daily")
    
    def set_dates(self, initialDate="31.5.2021", finalDate="1.6.2021"):
        initialDate = datetime.strptime(initialDate, "%d.%m.%Y")
        finalDate = datetime.strptime(finalDate, "%d.%m.%Y")
        delta = finalDate - initialDate
        dates = [(initialDate + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta.days + 1)]
        dates = [str(date) for date in dates]
        self.dates = dates
    
    def grab_data(self):
        all_data = []

        for j, date in enumerate(self.dates):
            wait = WebDriverWait(self.driver, 15)
            dateInput = wait.until(EC.presence_of_element_located((By.ID, "date-input")))
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "main.processing")))
            dateInput.click()

            date = date.split("-")
            
            if j == 0:
                picking_year(self.driver, date[0])
                picking_month(self.driver, date[1])
                picking_day(self.driver, int(date[-1]))
            
            elif self.dates[j][5:7] == self.dates[j - 1][5:7]:
                picking_day(self.driver, int(date[-1]))

            else:
                next = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "next")))
                next.click()
                picking_day(self.driver, int(date[-1]))

            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "main.processing")))
            wait.until(EC.presence_of_element_located((By.ID, "topview-entry-1")))

            entries = self.driver.find_elements(By.CSS_SELECTOR, "[id^='topview-entry-']")

            for i in range(1, 101):
                entry_id = f"topview-entry-{i}"
                entry = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, entry_id)))

                page = self.driver.find_element(By.ID, entry_id).find_element(
                    By.CLASS_NAME, "topview-entry--label"
                    ).find_element(By.CSS_SELECTOR, "a[dir='ltr']").text.strip()
                
                edit_text = self.driver.find_element(By.ID, entry_id).find_element(
                By.CLASS_NAME, "topview-entry--edits"
                ).find_element(By.CSS_SELECTOR, "a[target='_blank']").text
                edits = int(edit_text.replace(".", "").strip())

                pageview_text = self.driver.find_element(By.ID, entry_id).find_element(
                By.CLASS_NAME, "topview-entry--views"
                ).text
                pageviews = int(pageview_text.replace(".", "").strip())

                all_data.append({
                    'Page Name': page,
                    'Number of edits': int(edits),
                    'Pageviews': int(pageviews)
                })
        df = pd.DataFrame(all_data)
        grouped_df = df.groupby('Page Name', as_index=False).sum()
        grouped_df = grouped_df.sort_values(by='Pageviews', ascending=False)
        grouped_df["Pageviews - Number of Edits Ratio"] = grouped_df["Pageviews"] / grouped_df["Number of edits"]
        grouped_df.to_excel("wikipedia_page_data.xlsx", index=False)

    def closing(self):
        try:
            self.driver.quit()
        except OSError:
            pass