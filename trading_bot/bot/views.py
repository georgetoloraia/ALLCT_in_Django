from django.shortcuts import render
from .models import BotConfig, TradeLog, CoinEvaluation

def dashboard(request):
    trades = TradeLog.objects.all()
    evaluations = CoinEvaluation.objects.all()
    return render(request, 'bot/dashboard.html', {'trades': trades, 'evaluations': evaluations})
