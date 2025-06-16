from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

numberMonth = {
         "01":"Jan",
         "02":"Feb",
         "03":"Mar",
         "04":"Apr",
         "05":"May",
         "06":"Jun",
         "07":"Jul",
         "08":"Aug",
         "09":"Sep",
         "10":"Oct",
         "11":"Nov",
         "12":"Dec"
    }


def picking_year(driver, year):
    wait = WebDriverWait(driver, 20)
    if int(year) <= 2025:                
                yearMonthSwitch = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "datepicker-switch")))
                yearMonthSwitch.click()
                if int(year) < 2025:
                    yearSwitch = wait.until(EC.element_to_be_clickable((By.XPATH, '//th[@class="datepicker-switch" and text()="2025"]')))
                    yearSwitch.click()
                    if int(year) >= 2020:
                        year = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="year" and text()="{year}"]')))
                        year.click()
                    elif int(year) < 2020:
                        decadeSwitch = wait.until(EC.element_to_be_clickable((By.XPATH, '//th[@class="datepicker-switch" and text()="2020-2029"]')))
                        decadeSwitch.click()
                        
                        decade10 = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="decade" and text()="2010"]')))
                        decade10.click()

                        year = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="year" and text()="{year}"]')))
                        year.click()

def picking_month(driver, month):
    wait = WebDriverWait(driver, 20)
    try:
        monthbtn = WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="month" and text()="{numberMonth[month]}"]')))
        monthbtn.click()
    except:
        monthbtn = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="month focused" and text()="{numberMonth[month]}"]')))
        monthbtn.click()

def picking_day(driver, day):
    wait = WebDriverWait(driver, 20)
    daybtn = wait.until(EC.element_to_be_clickable((By.XPATH, f'//td[@class="day" and text()="{str(day)}"]')))
    daybtn.click()
