from django.db import migrations

def create_portfolio_and_tickers(apps, schema_editor):
    Portfolio = apps.get_model('invest', 'portfolio')
    Ticker = apps.get_model('invest', 'ticker')
    
    # Create a portfolio with 10,000 cash
    portfolio = Portfolio.objects.create(cash=10000.00)
    
    # List of common tickers
    tickers = [
        ("Apple Inc.", "AAPL"),
        ("Microsoft Corp.", "MSFT"),
        ("Amazon.com Inc.", "AMZN"),
        ("Alphabet Inc.", "GOOGL"),
        ("Meta Platforms Inc.", "META"),
        ("Tesla Inc.", "TSLA"),
        ("NVIDIA Corp.", "NVDA"),
        ("Berkshire Hathaway Inc.", "BRK.B"),
        ("Johnson & Johnson", "JNJ"),
        ("JPMorgan Chase & Co.", "JPM"),
    ]
    
    # Create ticker objects
    for name, symbol in tickers:
        Ticker.objects.create(name=name, symbol=symbol, value=0.00, share_price=0.00)

class Migration(migrations.Migration):
    
    dependencies = [
        ('invest', '0002_buyrequest_sellrequest_delete_transactionrequest'),
    ]
    
    operations = [
        migrations.RunPython(create_portfolio_and_tickers),
    ]
    atomic = False
