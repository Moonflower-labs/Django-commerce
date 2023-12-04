from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import AddListingForm, BidForm, CommentForm

from .models import *


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {'listings': active_listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def add_listing(request):
    if request.method == 'POST':
        form = AddListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.seller = request.user
            new_listing.save()
            messages.success(
                request, f'{new_listing.title} listed successfully!')
            return HttpResponseRedirect(reverse('index'))

    else:
        form = AddListingForm(auto_id=True)

    return render(request, 'auctions/add_listing.html', {'form': form})


def listing_page(request, pk):
    try:
        listing = Listing.objects.get(pk=pk)
        form = BidForm(initial={'listing': listing, 'bidder': request.user})
        price = listing.current_bid().amount if listing.current_bid(
        ) is not None else listing.starting_bid
        comments = Comment.objects.filter(listing=pk)
        comment_form = CommentForm()
        user_watchlist, created = Watchlist.objects.get_or_create(
            user=request.user)
        in_watchlist = listing in user_watchlist.get_watchlist()

    except Listing.DoesNotExist:
        return render(request, 'auctions/not_found.html')

    return render(request, 'auctions/listing_page.html', {'listing': listing, 'price': price, 'form': form, 'in_watchlist': in_watchlist, 'comment_form': comment_form, 'comments': comments})


@login_required(login_url='login')
def handle_bid(request):
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            pk = new_bid.listing_id
            listing = get_object_or_404(Listing, id=pk)
            current_bid = listing.current_bid()
            if current_bid is not None:
                price = current_bid.amount
                if new_bid.amount > price:
                    new_bid.save()
                    messages.success(request, 'Bid submitted successfully!')
                else:
                    form.add_error(
                        'amount', f'Your bid amount must be higher than the current price. (£{price})')
            else:
                price = listing.starting_bid
                if new_bid.amount >= price:
                    new_bid.save()
                    messages.success(request, 'Bid submitted successfully!')
                else:
                    form.add_error(
                        'amount', f'Your bid amount must be at least equal to the starting bid price. (£{price})')
            if form.errors:
                for field, error_list in form.errors.items():
                    for error in error_list:
                        messages.error(request, error)

        return HttpResponseRedirect(reverse('listing_page', args=(pk,)))

    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='login')
def close_bid(request, pk):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=pk, seller=request.user)

        if listing.is_active:
            listing.is_active = False
            listing.save()
            highest_bid = listing.current_bid()
            if highest_bid:
                winner = highest_bid.bidder
                listing.winner = winner
                listing.save()
                messages.success(
                    request, f'Auction closed successfully. {winner.username} is the winner.')
            else:
                messages.error(request, 'No bids were made for this listing.')
        else:
            messages.error(request, 'Auction is already closed.')

        return HttpResponseRedirect(reverse('listing_page', args=(pk,)))


@login_required(login_url='login')
def watchlist(request):
    user = request.user
    try:
        watchlist = Watchlist.objects.get(user=user)
        watchlist_items = watchlist.get_watchlist()
    except Watchlist.DoesNotExist:
        return render(request, 'auctions/watchlist.html', {'watchlist': []})

    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist_items})


@login_required(login_url='login')
def handle_watchlist(request, pk):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=pk)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)

        if listing in watchlist.listings.all():
            watchlist.listings.remove(listing)
            messages.info(request, f'{listing.title} removed from watchlist.')
        else:
            watchlist.listings.add(listing)
            messages.info(request, f'{listing.title} added to watchlist.')

        return HttpResponseRedirect(reverse('listing_page', args=(pk,)))


@login_required(login_url='login')
def handle_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        listing = get_object_or_404(Listing, pk=pk)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing
            new_comment.save()
            messages.success(
                request, 'Comment added successfully!')
            return HttpResponseRedirect(reverse('listing_page', args=(pk,)))
    else:
        return HttpResponseNotAllowed(['POST'])


def categories(request):
    item_categories = Category.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        try:
            filtered_items = Listing.objects.filter(
                category__category_type=selected_category)
        except Category.DoesNotExist:
            raise Http404("Category does not exist")
    else:
        filtered_items = None

    return render(request, 'auctions/categories.html', {'item_categories': item_categories, 'filtered_items': filtered_items, 'selected_category': selected_category})
