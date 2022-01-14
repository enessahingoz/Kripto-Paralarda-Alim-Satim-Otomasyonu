import time
import datetime as DT
from datetime import datetime
from binance.client import Client
from binance.enums import *
import pandas as pd
import numpy as np
import talib as ta

api_key = "***"
secret_key = "***"

class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    def connect(self, file):
        key = "***"
        secret = "***"
        self.client = Client(key, secret,tld ="com", testnet=True)

def generateTillsonT3(c_arr, h_arr, l_arr, hacim_faktoru, t3Length):

    ema_first_input = (h_arr + l_arr + 2 * c_arr) / 4

    ema1 = ta.EMA(ema_first_input, t3Length)

    ema2 = ta.EMA(ema1, t3Length)

    ema3 = ta.EMA(ema2, t3Length)

    ema4 = ta.EMA(ema3, t3Length)

    ema5 = ta.EMA(ema4, t3Length)

    ema6 = ta.EMA(ema5, t3Length)

    c1 = -1 * hacim_faktoru * hacim_faktoru * hacim_faktoru

    c2 = 3 * hacim_faktoru * hacim_faktoru + 3 * hacim_faktoru * hacim_faktoru * hacim_faktoru

    c3 = -6 * hacim_faktoru * hacim_faktoru - 3 * hacim_faktoru - 3 * hacim_faktoru * hacim_faktoru * hacim_faktoru

    c4 = 1 + 3 * hacim_faktoru + hacim_faktoru * hacim_faktoru * hacim_faktoru + 3 * hacim_faktoru * hacim_faktoru

    T3 = c1 * ema6 + c2 * ema5 + c3 * ema4 + c4 * ema3

    return T3
def MACD():
    klines2 = client.get_klines(symbol="BTCUSDT", interval='5m', limit='60')
    Value = [float(entry[4]) for entry in klines2]
    Value = pd.DataFrame(Value)
    ema12 = Value.ewm(span=12).mean()
    ema26 = Value.ewm(span=26).mean()
    macd_deger = ema26 - ema12
    signal = macd_deger.ewm(span=9).mean()

    macd_deger = macd_deger.values.tolist()
    signal = signal.values.tolist()
    
    if macd_deger[-1] > signal[-1] and macd_deger[-2] < signal[-2]:
        macd_return = 'BUY'
    elif macd_deger[-1] < signal[-1] and macd_deger[-2] > signal[-2]:
        macd_return = 'SELL'
    else:
        macd_return = 'HOLD'

    return macd_return
def stopLoss():
    tarih = DT.date.today()
    lastweek = tarih - DT.timedelta(days=6)
    lastweek = lastweek.strftime('%d %b, %Y')
    deger = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, str(lastweek))
    enyuksek = [float(entry[2]) for entry in deger]
    endusuk = [float(entry[3]) for entry in deger]
    Value = [float(entry[4]) for entry in deger]
    ortalamadeger = (sum(enyuksek)/len(enyuksek)-sum(endusuk)/len(endusuk))/(sum(Value)/len(Value))
    sonhaftaort = Value[-2]*(1-ortalamadeger)
    return sonhaftaort




client = Client(api_key = api_key, api_secret= secret_key, tld ="com", testnet=True)
print('----------DATE----------||---BALANCE--||----------T3 VALUES-----------||--MACD--||------PRICE------||---STRATEGY---|')
while True:
    # Price & Server Time
    now = datetime.now()
    coitime = now.strftime("%H:%M:%S")
    an = datetime.now()
    tarih = datetime.ctime(an)
    price = client.get_ticker(symbol="BTCUSDT")
    btcHesap = client.get_asset_balance(asset = "BTCUSDT")
 
    klines = client.get_klines(symbol="BTCUSDT", interval='5m', limit='500')
    klines2 = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
    close = [float(entry[4]) for entry in klines]
    c_arr = np.asarray(close)
    close_finished = c_arr[:-1]

    
    if __name__ == '__main__':
        filename = 'credentials.txt'

        connection = BinanceConnection(filename)

        klines = connection.client.get_klines(symbol="BTCUSDT", interval="5m", limit=500)
    
        open_time = [int(entry[0]) for entry in klines]

        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]

        c_arr = np.asarray(close)
        h_arr = np.asarray(high)
        l_arr = np.asarray(low)
        hacimfaktoru = 0.7
        t3length = 8
        tillsont3 = generateTillsonT3(c_arr, h_arr, l_arr, hacim_faktoru=hacimfaktoru, t3Length=t3length)
    
    
        t3_son = tillsont3[-1]
        t3_onceki = tillsont3[-2]
        t3_2_onceki = tillsont3[-3]
        t3_buy=False
        t3_sell=False   

    # grafik kırmızıdan yeşile dönüyor
        if t3_son > t3_onceki and t3_onceki < t3_2_onceki:
            t3_buy=True  

    # grafik yeşilden kırmızıya dönüyor
        elif t3_son < t3_onceki and t3_onceki > t3_2_onceki:
             t3_sell=True   
    
    balance = client.get_asset_balance(asset = "BTC")
    coindeger = format(float(price['askPrice']), '.4f')
    if (t3_sell==True and MACD() == 'SELL'):
        stat = 'sell'
        order = client.create_order(symbol = "BTCUSDT", side = "SELL", type = "MARKET", quantity = 0.05)         
        time.sleep(30)
            
    elif float(coindeger) < stopLoss():
        stat = 'STOPLOSS'
        order = client.create_order(symbol = "BTCUSDT", side = "SELL", type = "MARKET", quantity = 0.05)
        time.sleep(30)  
   
    elif (MACD() == 'BUY' and t3_buy==True):
        stat = 'buy'
        order = client.create_order(symbol = "BTCUSDT", side = "BUY", type = "MARKET", quantity = 0.05)
        time.sleep(30)
           
    else:
        stat = 'hold'  

    # Print the values
    print(tarih+'   ' + balance['free'] + '    ' +'t3_buy: '+str(t3_buy)+' t3_sell: '+str(t3_sell) + '     ' + MACD()
              + '      ' + price['askPrice']  + '       ' + stat)
    time.sleep(60)
   


