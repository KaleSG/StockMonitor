import json

def __main__():
    
    # Open and read the JSON file
    csvOutput = open('stocks.csv', 'w')
    
    with open('data.json', 'r') as file:
        data = json.load(file)
        # for key in list(data[0].keys()):
        #         csvOutput.write(key + ",")
        # csvOutput.write('\n')
        
        for stock in data:
            for key in list(stock.keys()):
                csvOutput.write(str(stock[key])+ ',')
            csvOutput.write('\n')
        


