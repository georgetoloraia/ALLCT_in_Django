from django.contrib import admin
from .models import BotConfig, TradeLog, CoinEvaluation

@admin.register(BotConfig)
class BotConfigAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'secret', 'usdt_balance')
    search_fields = ('api_key', 'secret')

@admin.register(TradeLog)
class TradeLogAdmin(admin.ModelAdmin):
    list_display = ('coin', 'buy_price', 'sell_price', 'profit', 'trade_time')
    list_filter = ('coin', 'trade_time')
    search_fields = ('coin',)

@admin.register(CoinEvaluation)
class CoinEvaluationAdmin(admin.ModelAdmin):
    list_display = ('coin', 'rsi', 'macd', 'bollinger_lower', 'timestamp')
    list_filter = ('coin', 'timestamp')
    search_fields = ('coin',)
