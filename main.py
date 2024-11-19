from selenium import webdriver
import locale, re, requests,json

# Initialization Options
options = webdriver.FirefoxOptions()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)
locale.setlocale(locale.LC_ALL, '')
# bypass for python blocking on nasdaq
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'} 



symbolList = [ "NVDA","AVGO", "COST", "AMZN", "JPM", "AXP", "AXON"]
symbolStats = []


for symbol in symbolList:
    stock = {}
    
    #  PortfolioLab  Return Rate Aggregate
    # driver.get("https://portfolioslab.com/symbol/" + symbol)
     
    stock["Symbol"] = symbol.upper()
    # stock["YTD"] = locale.atof(re.sub('%','',driver.find_element("xpath","/html/body/div/div/div[2]/main/section[4]/div[2]/div/div[1]/div/div[1]/p").text))/100
    # stock["1MonthReturn"] = locale.atof(re.sub('%','',driver.find_element("xpath","/html/body/div/div/div[2]/main/section[4]/div[2]/div/div[1]/div/div[2]/p").text))/100   
    # stock["6MonthReturn"] = locale.atof(re.sub('%','',driver.find_element("xpath","/html/body/div/div/div[2]/main/section[4]/div[2]/div/div[1]/div/div[3]/p").text))/100   
    # stock["1YearReturn"] = locale.atof(re.sub('%','',driver.find_element("xpath","/html/body/div/div/div[2]/main/section[4]/div[2]/div/div[1]/div/div[4]/p").text))/100   
    # stock["5YearReturn"] = locale.atof(re.sub('%','',driver.find_element("xpath","/html/body/div/div/div[2]/main/section[4]/div[2]/div/div[1]/div/div[5]/p").text))/100   
    # stock["10YearReturn"] = locale.atof(re.sub('%','',driver.find_element("xpath","/html/body/div/div/div[2]/main/section[4]/div[2]/div/div[1]/div/div[6]/p").text))/100   
           
    # Nasdaq response
    
    #Initialization
    nasdaqURL = "https://api.nasdaq.com/api/company/"+symbol+"/financials"
    jsonResponse = requests.get(nasdaqURL, headers=headers).json()
    balanceData=  jsonResponse['data']['balanceSheetTable']['rows']
    
    #DTE Calculuations and Properties
    stock['Equity'] =  locale.atof(balanceData[32]['value2'].replace("$",''))
    shortTermDebt = locale.atof(balanceData[17]['value2'].replace("$",'').replace("--", '0'))
    longTermDebt = locale.atof(balanceData[20]['value2'].replace("$",'').replace("--", '0'))
    stock['Debt'] = shortTermDebt + longTermDebt
    
    stock['DebtToEquity'] = '%.3f'%(stock['Debt']/stock['Equity'])
    
    # Profit Margin Calculations
    incomeData=  jsonResponse['data']['incomeStatementTable']['rows']
    stock['GrossProfit'] = locale.atof(incomeData[2]['value2'].replace("$",'').replace("--", '0'))
    stock['TotalRevenue'] = locale.atof(incomeData[0]['value2'].replace("$",'').replace("--", '0'))
    stock['ProfitMargin'] = '%.3f'%(stock['GrossProfit']/stock['TotalRevenue'])
    
    
    symbolStats.append(stock)
    

print(symbolStats)    
driver.quit()