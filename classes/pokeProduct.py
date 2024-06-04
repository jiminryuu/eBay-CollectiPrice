# this class will represent a product

import re #std lib

from bs4 import BeautifulSoup #3rd party imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from urllib.request import Request, urlopen

import config #local

class pokeProduct():
    
    #variables to instatiate with
    _itemname = ''
    _boughtFor = None
    _count = None
    _url = ''

    # variables to calculate
    _prices = None
    _adjusted_prices = None
    _mean_price = None
    _mean_price_adjusted = None
    _SD = None
    _difference = None
    _total_gain = None
    _profit = False

    def __init__(self, itemname:str, boughtFor:float, count:str, url:str):
        self._itemname = itemname
        self._boughtFor = boughtFor
        self._count = count
        self._url = url
        self.scrape_product_info()


    def scrape_product_info(self):
        elements = self.scrape_sold_elements()
        prices = self.extract_prices(elements)
        self.fill_fields(prices)




    def scrape_sold_elements(self) -> list:
        req = Request(self._url, headers=config.STD_HEAD) # return the html
        webpage = urlopen(req).read()
      
        soup = BeautifulSoup(webpage, 'html5lib')
        price_elements = soup.find_all(config.TAG_TYPE, class_= config.CLS_SOLD)
        return price_elements

    def extract_prices(self, price_elements:list) -> list:
        prices = []
        for element in price_elements:
            text = element.get_text(strip=True) # will return in this format -> 'C $111.11'
            price = re.search(config.NUMBER_EXTRACTOR,text).group() # get price only
            prices.append(float(price))
        return prices
    
    def fill_fields(self, prices:list):
        if self._prices is None:
            self._prices = prices
            self._mean_price = np.mean(prices)
            self.SD  = np.std(prices)
            self.calculate_adjusted()
            self.calculate_profits()

    def calculate_adjusted(self):
        
        adjusted_prices = []
        if self._prices is not None:
            for price in self._prices:
                if self._mean_price - self.SD < price < self._mean_price + self.SD:
                    adjusted_prices.append(price)
        self.adjusted_prices = adjusted_prices
        self._mean_price_adjusted = np.mean(self.adjusted_prices)

    def calculate_profits(self):
        self._difference = self._mean_price_adjusted - self._boughtFor
        self._total_gain = self._count * self._difference

        if(self._total_gain > 0):
            self._profit = True

    def get_data(self):

        data = {
            "item_name": self._itemname,
            "boughtFor": self._boughtFor,
            "count": self._count,
            "url": self._url,

            # Variables to calculate
            "prices": self._prices,
            "adjusted_prices": self._adjusted_prices,
            "mean_price": self._mean_price,
            "mean_price_adjusted": self._mean_price_adjusted,
            "standard_deviation": self._SD,
            "price_difference": self._difference,
            "total_gain": self._total_gain,
            "profitable": self._profit
        }
        return data



    

    