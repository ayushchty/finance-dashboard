import yfinance as yf
import numpy as np
import time
import json

def live_market():
    portfolio = 1250000
    while True:
        try:
            data = yf.Ticker("^NSEI")
            nifty = data.info.get('currentPrice', None)
            
            if nifty is None:
                info = yf.download("^NSEI", period="1d", progress=False)
                nifty = info['Close'].iloc[-1]
            
            portfolio += np.random.randn() * 10000
            pnl = (portfolio - 1250000) / 1250000 * 100
            
            print(f"Nifty: {nifty:.2f} | Portfolio: {portfolio:,.0f} | PnL: {pnl:.2f}%")
        except Exception as e:
            print(f"Error fetching data: {e}")
        
        time.sleep(30)

if __name__ == "__main__":
    live_market()
