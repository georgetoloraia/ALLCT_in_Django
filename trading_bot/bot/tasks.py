from celery import shared_task
import ccxt
import pandas as pd
import numpy as np
import talib
import time
from .models import BotConfig, TradeLog, CoinEvaluation

@shared_task
def run_trading_bot():
    bot_config = BotConfig.objects.first()
    
    if not bot_config:
        print("BotConfig is not set. Please configure it in the admin panel.")
        return

    binance = ccxt.binance({
        'apiKey': bot_config.api_key,
        'secret': bot_config.secret,
        'enableRateLimit': True,
    })

    def get_all_tickers():
        tickers = binance.fetch_tickers()
        return [symbol for symbol in tickers.keys() if symbol.endswith('/USDT')]

    def get_rsi(data, period=14):
        return talib.RSI(data['close'], timeperiod=period)

    def get_macd(data, fast_period=12, slow_period=26, signal_period=9):
        macd, signal, _ = talib.MACD(data['close'], fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
        return macd, signal

    def get_bollinger_bands(data, period=20, num_std=2):
        upper_band, middle_band, lower_band = talib.BBANDS(data['close'], timeperiod=period, nbdevup=num_std, nbdevdn=num_std)
        return upper_band, lower_band

    def evaluate_coin(symbol):
        data = binance.fetch_ohlcv(symbol, timeframe='5m', limit=100)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        rsi = get_rsi(df).iloc[-1]
        macd, signal = get_macd(df)
        macd_cross = macd.iloc[-1] - signal.iloc[-1]
        upper_band, lower_band = get_bollinger_bands(df)
        price = df['close'].iloc[-1]

        CoinEvaluation.objects.create(
            coin=symbol,
            rsi=rsi,
            macd=macd_cross,
            bollinger_lower=lower_band.iloc[-1]
        )

        if rsi < 30 and macd_cross > 0 and price < lower_band.iloc[-1]:
            return True  # Potential buy signal
        return False

    def buy_coin(symbol):
        balance = binance.fetch_balance()
        usdt_balance = balance['total']['USDT']
        if usdt_balance > 10:  # Ensure there's enough balance to trade
            amount = usdt_balance / binance.fetch_ticker(symbol)['last']
            order = binance.create_market_buy_order(symbol, amount)
            TradeLog.objects.create(
                coin=symbol,
                buy_price=order['price'],
                sell_price=None,
                profit=None
            )
            return order
        return None

    def sell_coin(symbol, buy_price, target_profit=0.05):
        while True:
            ticker = binance.fetch_ticker(symbol)
            current_price = ticker['last']
            if (current_price - buy_price) / buy_price >= target_profit:
                balance = binance.fetch_balance()
                coin_balance = balance['total'][symbol.split('/')[0]]
                if coin_balance > 0:
                    order = binance.create_market_sell_order(symbol, coin_balance)
                    profit = (order['price'] - buy_price) * coin_balance
                    TradeLog.objects.filter(coin=symbol, buy_price=buy_price).update(
                        sell_price=order['price'],
                        profit=profit
                    )
                    return order
            time.sleep(60)

    def main():
        existing_coins = get_all_tickers()
        while True:
            for coin in existing_coins:
                if evaluate_coin(coin):
                    order = buy_coin(coin)
                    if order:
                        sell_coin(coin, order['price'])

            new_coins = list(set(get_all_tickers()) - set(existing_coins))
            for new_coin in new_coins:
                buy_coin(new_coin)

            existing_coins = get_all_tickers()
            time.sleep(300)  # Check every 5 minutes

    main()
