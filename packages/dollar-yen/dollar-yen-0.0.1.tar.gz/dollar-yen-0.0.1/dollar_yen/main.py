import yfinance as yf


def fx_rates(ticker):
    return yf.Ticker(ticker).history(period="1d").Close.iloc[0]

def now():
    print(fx_rates("USDJPY=X"))
def exchange(num):
    return num * fx_rates("USDJPY=X")

def main():
    dollar = float(input('Please enter the amount you would like to convert into Japanese yen: '))
    print(f"{dollar} USD = {exchange(dollar):.2f} Yen")
    
if __name__ == "__main__":
    main()   