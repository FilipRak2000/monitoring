from requests import get
from pprint import PrettyPrinter
import os
import schedule
import time
from dotenv import load_dotenv



load_dotenv()
printer = PrettyPrinter()

def getcurrency():
    endpoint = os.getenv("API_ENDPOINT")
    data = get(endpoint).json()
    printer.pprint(data)
    data = list(data.items())
    return data[0][1]

data = getcurrency()    

def compare():
    shortcut1 = str(input("sell(shortcut like PLN or EUR): ")).upper()
    shortcut2 = str(input("buy(shortcut like PLN or EUR): ")).upper()
    result = data[shortcut1] / data[shortcut2]
    print(f"price for 1 {shortcut2} = {result}")
    return result, shortcut2

result, shortcut2 = compare()
ask = lambda: float(input("your price is: "))
your_price = ask()
script_run = True
count = 0

def notification():
    global count
    getcurrency()
    if result <= your_price:
        notification =f"display notification \"HEY the price of {shortcut2} is compatible with your preferences!\" with title \"PRICE ALERT\""
        os.system(f'osascript -e \'{notification}\'')
        count += 1
        if count == 3:
            global script_run
            script_run = False
    else:
        return 
    
schedule.every(10).seconds.do(notification)

while script_run:
    schedule.run_pending()
    time.sleep(1)
