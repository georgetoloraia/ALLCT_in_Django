# Generated by Django 5.0.6 on 2024-06-01 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=100)),
                ('secret', models.CharField(max_length=100)),
                ('usdt_balance', models.FloatField(default=10.0)),
            ],
        ),
        migrations.CreateModel(
            name='CoinEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=10)),
                ('rsi', models.FloatField()),
                ('macd', models.FloatField()),
                ('bollinger_lower', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=10)),
                ('buy_price', models.FloatField()),
                ('sell_price', models.FloatField()),
                ('profit', models.FloatField()),
                ('trade_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
