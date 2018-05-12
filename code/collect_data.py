from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

def get_box_office_data():
	movie_data = []
	for year in years:
		print(year)
		url = "http://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=%d&sort=gross&order=ASC&p=.htm" % (year)
		response = get(url)
		text = response.text
		soup = bs(text, 'html.parser')
		table = soup.find_all('font', attrs= {"face":"Verdana", "size":"4"})
		number_pages = table[0].text.encode('ascii', 'ignore').decode('ascii')
		number_pages = len(number_pages.split(' - '))
		for i in range(number_pages):
			url = "http://www.boxofficemojo.com/yearly/chart/?page=%d&view=releasedate&view2=domestic&yr=%d&sort=gross&order=ASC&p=.htm" % (i+1, year)
			response = get(url)
			text = response.text
			soup = bs(response.text, 'html.parser')
			table = soup.find_all('table', attrs= {"cellspacing": "1", "cellpadding": "5", "bgcolor":"#ffffff"})[0]
			data_rows = table.find_all('td')
			data = [row.text.encode('ascii', 'ignore').decode('ascii') for row in data_rows]
			movie_data.extend(data[data.index("Close") + 1:-16])
		time.sleep(0.1)
	return movie_data

def create_pandas_df(movie_data):
	df = pd.DataFrame(columns=['Movie Title','Studio', 'Gross Earnings', 'Total Theatres', 
									'Opening Earnings', 'Opening Theatres', 'Release Date', 'Close Data'])
	movie_dataset = [[movie_data[i*9+1:(i+1)*9]] for i in range(int(len(movie_data)/9))]
	print("yo")
	print(len(movie_dataset))
	for i in range(len(movie_dataset)):
		df.loc[i] = movie_dataset[i][0]
	print("done")
	return df




movie_data = get_box_office_data()
movie_df = create_pandas_df(movie_data)
print(len(movie_df))
movie_df.to_pickle("movie_df.pkl")
