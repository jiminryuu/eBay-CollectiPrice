# this script was to print out the density curve of the scraped price points to see the distribution
# this is ad-hoc but it seems that 1SD away from the mean should mean extreme data points (will remove)

import re #std lib

from bs4 import BeautifulSoup #3rd party imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from urllib.request import Request, urlopen

import config #local


number_extractor = r'\d+\.\d+'


hiddenFatesLink = "https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=hidden+fates+elite+trainer+box&_sacat=0&rt=nc&_odkw=hidden+fates+etb&_osacat=0&LH_Complete=1&LH_Sold=1"
champPathLink = 'https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=champions+path+elite+trainer+box&_sacat=0&_odkw=hidden+fates+elite+trainer+box+case&_osacat=0&LH_Complete=1&LH_Sold=1'
links = [hiddenFatesLink,champPathLink]



for link in links:
  standardReqHead = {'User-Agent' : 'Mozilla/5.0'}

  req = Request(link, headers=standardReqHead)  # Use 'headers' instead of 'User-Agent'
  webpage = urlopen(req).read()

  with requests.Session() as ses:
      soup = BeautifulSoup(webpage, 'html5lib')
      price_elements = soup.find_all("span", class_= "POSITIVE ITALIC")
      prices = []
      for element in price_elements:
          text = element.get_text(strip=True) # will return in this format -> 'C $111.11'
          price = re.search(number_extractor,text).group() # get the int
          prices.append(float(price))


      mini = min(prices)
      maxi = max(prices)
      range_size = 0
      if maxi > mini: 
         range_size = (maxi-mini)/15
      ranges = [(i, i + range_size - .0001) for i in np.arange(mini, maxi, range_size)]
      print(ranges)

      counts = [(r[0], r[1], ((prices >= r[0]) & (prices <= r[1])).sum()) for r in ranges]

      df = pd.DataFrame(counts, columns=['Start', 'End', 'Frequency'])
      intervals = ranges
      freq = df['Frequency']

      # Display table
      print(df)

      
      plt.plot(intervals,freq)
      plt.show()  
      sd = np.std(prices)
      print("standard deviation", sd)
      print(prices)