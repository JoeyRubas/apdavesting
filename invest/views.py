# views.py
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import BuyRequestForm, SellRequestForm
from .models import buyRequest, portfolio, sellRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

def vote_request(request, request_type, request_id):
    if request_type == 1:
        trade_request = get_object_or_404(sellRequest, id=request_id)
    else:
        trade_request = get_object_or_404(buyRequest, id=request_id)

    if request.method == "POST":
        trade_request.votes += 1
        trade_request.save()
        messages.success(request, f"Your vote for {trade_request.ticker.symbol} has been counted!")
        return redirect("index")  # Redirect to the index page

    return render(request, "vote.html", {"trade_request": trade_request})



def index(request):
    buy_requests = buyRequest.objects.all()
    sell_requests = sellRequest.objects.all()
    
    portfolio_obj = portfolio.objects.first()
    positions = portfolio_obj.positions.all()
    
    context = {
        'buy_requests': buy_requests,
        'sell_requests': sell_requests,
        'portfolio_value': portfolio_obj.value if portfolio_obj else 0.0,
        'cash': portfolio_obj.cash if portfolio_obj else 0.0,
        'positions': positions

    }
    return render(request, 'index.html', context)


def vote(request):
    pass

def sell_request(request):
    if request.method == 'POST':
        form = SellRequestForm(request.POST)
        if form.is_valid():
            portfolio_obj = portfolio.objects.first()  # Assuming one portfolio
            if not portfolio_obj:
                messages.error(request, "No portfolio available.")
                return redirect('sell_request')
            position = form.cleaned_data['position']
            position_obj = portfolio_obj.positions.get(id=position.id)
            shares = form.cleaned_data['shares']
            if shares <= 0:
                messages.error(request, "Invalid number of shares.")
                return redirect('sell_request')
            if position_obj.shares >= shares:
                sellRequest.objects.create(position=position_obj, votes=0, shares=form.cleaned_data['shares'])
                return redirect('index')
            else:
                messages.error(request, "Not enough shares to sell.")
    else:
        form = SellRequestForm()

    return render(request, 'sell_request.html', {'form': form})

def buy_request(request):
    if request.method == 'POST':
        form = BuyRequestForm(request.POST)
        if form.is_valid():
            ticker_obj = form.cleaned_data['ticker']
            shares = form.cleaned_data['shares']
            portfolio_obj = portfolio.objects.first()  # Assuming one portfolio
            if shares <= 0:
                messages.error(request, "Invalid number of shares.")
                return redirect('buy_request')
            if not portfolio_obj:
                messages.error(request, "No portfolio available.")
                return redirect('buy_request')
            
            total_cost = shares * ticker_obj.share_price
            if portfolio_obj.cash >= total_cost:

                # Create buy request with 0 votes initially
                buyRequest.objects.create(ticker=ticker_obj, shares=shares, votes=0)
                
                messages.success(request, "Buy request submitted successfully.")
                return redirect('index')
            else:
                messages.error(request, "Not enough cash to buy the requested shares.")
    else:
        form = BuyRequestForm()

    return render(request, 'buy_request.html', {'form': form})
