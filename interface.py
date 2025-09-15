from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os


class FrankfurtBoerse(ABC):

    def __init__(self, headless: bool = True, width: int = 1820, height: int = 880):

        driver_path = os.path.join(os.path.dirname(__file__), "msedgedriver.exe")
        self.service = Service(driver_path)
        options = webdriver.EdgeOptions()


        options.add_argument(f"--window-size={width},{height}")

        if headless:
            options.add_argument("--headless")


        self.webdriver = webdriver.Edge(service=self.service, options=options)


    @abstractmethod
    def history(self, start_date: str, end_date: str, adjust_prices: bool = False):
        """Abstract method for retrieving historical data."""
        pass



