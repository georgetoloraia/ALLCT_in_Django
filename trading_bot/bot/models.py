from django.db import models

class BotConfig(models.Model):
    api_key = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)
    usdt_balance = models.FloatField(default=10.0)

class TradeLog(models.Model):
    coin = models.CharField(max_length=10)
    buy_price = models.FloatField()
    sell_price = models.FloatField()
    profit = models.FloatField()
    trade_time = models.DateTimeField(auto_now_add=True)

class CoinEvaluation(models.Model):
    coin = models.CharField(max_length=10)
    rsi = models.FloatField()
    macd = models.FloatField()
    bollinger_lower = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
