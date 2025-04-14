import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils 
from interface import FrankfurtBoerse



class Bond(FrankfurtBoerse):
        
    def __init__(self, isin):
        super().__init__()
        self.isin = isin
        self.url = f"https://www.boerse-frankfurt.de/bond/{self.isin}"

    def history(self, 
                period: str,
                adjust_prices: bool = True,
                ):
        
        start_date = utils.period_to_date(period)

        try:

            self.webdriver.get(self.url)
            
            time.sleep(4)

            price_history = WebDriverWait(self.webdriver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-wrapper/div/div/div[2]/app-bond/app-data-menue/div/div/div/drag-scroll/div/div/button[4]"))
            )
            price_history.click()

            if adjust_prices:
                checkboxes = WebDriverWait(self.webdriver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']"))
                            )
                for checkbox in checkboxes:
                    try:
                        WebDriverWait(self.webdriver, 7).until(EC.element_to_be_clickable(checkbox)).click()  
                    except:
                        pass

            start_date_box = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-wrapper/div/div/div[2]/app-bond/div[2]/div/app-price-history/div[1]/div[1]/div/div/div[1]/app-datepicker/div/input'))
            )
            utils.clear_input_data_form(start_date_box)
            
            
            start_date_box.send_keys(start_date)

            search_new_dates = WebDriverWait(self.webdriver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search')]"))
            )
            search_new_dates.click()


            last_page = int(WebDriverWait(self.webdriver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "/html/body/app-root/app-wrapper/div/div/div[2]/app-bond/div[2]/div/app-price-history/div[2]/div/div/app-page-bar[1]/div/div[1]/button"))
                )[-3].text)


            data = utils.read_table(self.webdriver, last_page)

        finally:
            self.webdriver.quit() 

        return data
    

if __name__ == "__main__":

    isin = Bond('DE0001102390')
    data = isin.history("1mo")

    print(data)