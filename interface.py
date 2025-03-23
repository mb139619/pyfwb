from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class FrankfurtBoerse(ABC):

    def __init__(self, headless : bool = True):
        self.service = Service(EdgeChromiumDriverManager().install())
        options = webdriver.EdgeOptions()

        if headless:
            options.add_argument("--headless")

        self.webdriver = webdriver.Edge(service=self.service, options=options)


    @abstractmethod
    def history(self, start_date: str, end_date: str, adjust_prices: bool = True):
        """Abstract method for retrieving historical data."""
        pass



