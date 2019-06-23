import bs4
import xlsxwriter
from urllib.request import urlopen as uReq
#url of the website being scraped
my_url = 'https://in.reuters.com/finance/stocks/financial-highlights/'
key = input("Enter the key value: \n")
#accepting user input for the key value
my_url = my_url + key
#opening connection to the desired url
connection = uReq(my_url)
page_html = uReq(my_url).read()
connection.close()
page_soup = bs4.BeautifulSoup(page_html, "html.parser")
modules = page_soup.findAll("div",{"class":"module"})
#only specific data tables required
check = ["Consensus Estimates Analysis","Valuation Ratios","Growth Rates","Financial Strength","Profitability Ratios"]
headers = []
data = []
aData = ['']
row = 0
col = 0
loop = 0
#to store the data being scraped into an excel file
workbook = xlsxwriter.Workbook('DataFound.xlsx')
for m in modules:
	name = m.find("div",{"class":"moduleHeader"})
	if name is None:
		continue
	else:
		temp = str(name.text.strip())
		for c in check:
			if temp == c:
				print(temp)
				dataTables = m.find("table",{"class":"dataTable"})
				if dataTables is None:
					print("Table does not exist")
					continue
				else:
					head = dataTables.findAll("th")
					for h in head:
						headers.append(h.text)
					rawData = dataTables.findAll("td")
					anomData = dataTables.findAll("td",{"class":"dataTitle"})
					for a in anomData:
						aData.append(a.text)
					for d in rawData:
						data.append(d.text.strip())
					#putting each table in a new sheet
					worksheet = workbook.add_worksheet(temp)
					#recreating the table scraped
					for h in headers:
						worksheet.write(row,col,h)
						col = col + 1
					col = 0
					row = row +1
					for d in data:
						if col < len(headers):
							if d in aData:
								worksheet.write(row,col,d)
								row = row + 1
								col = 0
							else:
								worksheet.write(row,col,d)
								col = col + 1
						else:
							row = row + 1
							col = 0
							if d in aData:
								worksheet.write(row,col,d)
								row = row + 1
								col = 0
							else:
								worksheet.write(row,col,d)
								col = col + 1
					print(headers)
					print(data)
					headers = []
					data = []
					aData = ['']
					row = 0
					col = 0
workbook.close()