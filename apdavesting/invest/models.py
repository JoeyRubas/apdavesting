from django.db import models
from yahoo_fin import stock_info
from decimal import Decimal

class ticker(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    share_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.symbol
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.value = stock_info.get_live_price(self.symbol)
        super(ticker, self).save(*args, **kwargs)

class position(models.Model):
    ticker = models.ForeignKey(ticker, on_delete=models.CASCADE)
    shares = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ticker.symbol} - {self.shares} shares"
    
    @property
    def current_value(self):
        self.ticker.value = Decimal(stock_info.get_live_price(self.ticker.symbol))
        self.ticker.save()
        value = self.shares * self.ticker.value
        formatted_value = "{:.2f}".format(value)
        return formatted_value

class buyRequest(models.Model):
    ticker = models.ForeignKey(ticker, on_delete=models.CASCADE)
    shares = models.DecimalField(max_digits=10, decimal_places=2)
    votes = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.pk is None:  # Runs only when creating a new instance
            self.votes = 0
            super(buyRequest, self).save(*args, **kwargs)
            self.ticker.value = stock_info.get_live_price(self.ticker.symbol)
            self.ticker.save()
        else:
            super(buyRequest, self).save(*args, **kwargs)  
            self.ticker.value = stock_info.get_live_price(self.ticker.symbol)
            self.ticker.save()
            if self.votes >= 5:
                portfolio_obj = portfolio.objects.first()
                if not portfolio_obj:
                    return
                
                live_price = Decimal(self.ticker.value)
                portfolio_obj.cash -= self.shares * live_price
                portfolio_obj.save()
                position_obj = position(ticker=self.ticker, shares=self.shares, purchase_price=live_price)
                position_obj.save()
                portfolio_obj.positions.add(position_obj)
                self.delete()

    @property
    def cost(self):
        value = self.shares * self.ticker.value
        formatted_value = "{:.2f}".format(value)
        return formatted_value

class sellRequest(models.Model):
    position = models.ForeignKey(position, on_delete=models.CASCADE)
    shares = models.DecimalField(max_digits=10, decimal_places=2)
    votes = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.votes = 0
            super(sellRequest, self).save(*args, **kwargs)
            self.position.ticker.value = stock_info.get_live_price(self.ticker.symbol)
            self.position.ticker.save()
        else:
            super(sellRequest, self).save(*args, **kwargs)
            self.position.ticker.value = stock_info.get_live_price(self.ticker.symbol)
            self.position.ticker.save()
            if self.votes >= 5:
                portfolio_obj = portfolio.objects.first()
                if not portfolio_obj:
                    return
                portfolio_obj.cash += self.shares * self.position.purchase_price
                portfolio_obj.save()
                self.position.shares -= self.shares
                if self.position.shares == 0:
                    self.position.delete()
                else:
                    self.position.save()
                self.delete()
    @property
    def ticker(self):
        return self.position.ticker
    
    @property
    def cost(self):
        value = self.shares * self.position.purchase_price
        formatted_value = "{:.2f}".format(value)
        return formatted_value


class portfolio(models.Model):
    positions = models.ManyToManyField(position)
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def value(self):
        total_value = 0
        for pos in self.positions.all():
            total_value += pos.shares * pos.ticker.value
        return total_value + self.cash

class portfolioLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)