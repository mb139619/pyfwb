import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from dateutil.relativedelta import relativedelta   
from exceptions import InvalidPeriodError

def clear_input_data_form(web_element):

    web_element.send_keys(Keys.CONTROL + "a")
    web_element.send_keys(Keys.BACKSPACE)

    return

def period_to_date(period:str) -> str:


    period = period.strip().lower()

    now = datetime.now()  
    
    mapper = {
        "1d": now,
        "5d": now - relativedelta(days=5),
        "1mo": now - relativedelta(months=1),
        "3mo": now - relativedelta(months=3),
        "6mo": now - relativedelta(months=6),
        "1y": now - relativedelta(years=1),
        "2y": now - relativedelta(years=2),
        "5y": now - relativedelta(years=5),
        "10y": now - relativedelta(years=10),
        "ytd": datetime(now.year, 1, 1),
        "max" : datetime(1900, 1, 1)
    }
    
    date = mapper.get(period)

    if date:
        return date.strftime("%d/%m/%Y")  
    else:
        raise InvalidPeriodError(period, mapper.keys())


def read_table(driver, last_page):

    colnames = ["Date", "Open", "Close", "High", "Low", "Volume", "Value Nominal"]
    all_data = [] 

    for i in range(last_page):

        rows = driver.find_elements(By.CSS_SELECTOR, "tr.widget-table-row")
        
        page_data = [
            [col.text.strip() for col in row.find_elements(By.CSS_SELECTOR, "td.widget-table-cell")]
            for row in rows
        ]

        all_data.extend(page_data)  

        if i < last_page - 1:
            
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-wrapper/div/div/div[2]/app-bond/div[2]/div/app-price-history/div[2]/div/div/app-page-bar[1]/div/div[1]/button[last()-1]"))
                )

                next_button.click()

            except Exception as e:

                print(f"That's what went wrong: {e}")

                break  

    data = pd.DataFrame(all_data, columns=colnames)
    
    return data


if __name__ == "__main__":

    print(period_to_date("1 mo"))

            