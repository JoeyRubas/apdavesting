# views.py
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import BuyRequestForm, SellRequestForm
from .models import buyRequest, portfolio, sellRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from yahoo_fin import stock_info

def vote_request(request, request_type, request_id):
    if request_type == 1:
        trade_request = get_object_or_404(sellRequest, id=request_id)
    else:
        trade_request = get_object_or_404(buyRequest, id=request_id)

    # Check if the user has already voted in the session
    if 'voted_requests' not in request.session:
        request.session['voted_requests'] = []
    
    if request_id in request.session['voted_requests']:
        messages.error(request, "You have already voted on this request.")
        return redirect("index")

    if request.method == "POST":
        trade_request.votes += 1
        trade_request.save()
        
        # Store the voted request ID in the session
        request.session['voted_requests'].append(request_id)
        request.session.modified = True  # Ensure the session is saved

        messages.success(request, f"Your vote for {trade_request.ticker.symbol} has been counted!")
        return redirect("index")

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


def sell_request(request):
    if request.method == 'POST':
        form = SellRequestForm(request.POST)
        if form.is_valid():
            portfolio_obj = portfolio.objects.first()  
            if not portfolio_obj:
                messages.error(request, "No portfolio available.")
                return redirect('sell_request')
            position_obj = form.cleaned_data['position']
            if not position_obj.pk:
                messages.error(request, "Invalid position selection.")
                return redirect('sell_request')
            shares = form.cleaned_data['shares']
            if position_obj.shares >= shares:
                sell_request_obj = form.save(commit=False)
                sell_request_obj.votes = 0 
                sell_request_obj.save()
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
            shares = Decimal(form.cleaned_data['shares'])
            portfolio_obj = portfolio.objects.first()  

            if not portfolio_obj:
                messages.error(request, "No portfolio available.")
                return redirect('buy_request')
            
            if not ticker_obj.pk:
                messages.error(request, "Invalid ticker selection.")
                return redirect('buy_request')
            ticker_obj.value = Decimal(stock_info.get_live_price(ticker_obj.symbol))
            ticker_obj.save()
            total_cost = shares * ticker_obj.value
            print(f"Shares: {shares}, Share Price: {ticker_obj.value}, Total Cost: {total_cost}")

            if portfolio_obj.cash >= total_cost:
                buyRequest.objects.create(ticker=ticker_obj, shares=shares, votes=0)
                
                messages.success(request, "Buy request submitted successfully.")
                return redirect('index')
            else:
                messages.error(request, "Not enough cash to buy the requested shares.")
    else:
        form = BuyRequestForm()

    return render(request, 'buy_request.html', {'form': form})
