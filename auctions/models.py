from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    FASHION = "FA"
    KIDS = "KI"
    ELECTRONICS = "EL"
    HOME = "HO"
    BOOKS = "BO"
    TOOLS = "TO"
    EDIBLES = "ED"
    CATEGORY_CHOICES = [
        (None, 'Select a Category'),
        (FASHION, 'Fashion'),
        (KIDS, 'Toys'),
        (ELECTRONICS, 'Electronics'),
        (HOME, 'Home'),
        (BOOKS, 'Books'),
        (TOOLS, 'Tools'),
        (EDIBLES, 'Edibles'),
    ]
    category_type = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES, blank=False)

    def __str__(self):
        return self.get_category_type_display()


class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='listing_category')
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    listed_at = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_listing'
    )

    def current_bid(self):
        current_bid = self.bid_set.order_by('-amount').first()
        return current_bid

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.listing}, {self.bidder}, {self.amount}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.text}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watchlist')
    listings = models.ManyToManyField(Listing)

    def get_watchlist(self):
        return self.listings.all()

    def __str__(self):
        return f"Watchlist for {self.user}"
