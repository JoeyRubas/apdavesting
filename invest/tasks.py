from celery import shared_task
from .models import ticker, portfolio, portfolioLog
from django.db.models import Sum

from yahoo_fin import stock_info
import requests

@shared_task
def update_portfolio_value():
    print("running!")
    # Step 1: Update the price of each ticker from an API (or library)
    for t in ticker.objects.all():
        # Assuming you have an API endpoint that returns the price of the ticker
        # Here, I am just simulating an API call to get the current share price
        # Replace with your actual API code or library
    
            t.value = stock_info.get_live_price(t.symbol)
            t.save()

    # Step 2: Update the total value of the portfolio
    total_value = 0
    for p in portfolio.objects.all():
        portfolio_value = 0
        for pos in p.positions.all():
            # Calculate position value = shares * current share price
            position_value = pos.shares * pos.ticker.value
            portfolio_value += position_value
        total_value += portfolio_value + p.cash  # Add cash to portfolio value

    # Step 3: Create a portfolio log object with timestamp and value
    portfolio_log = portfolioLog(value=total_value)
    portfolio_log.save()

    return total_value
