from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<int:pk>", views.listing_page, name="listing_page"),
    path("handle_bid", views.handle_bid, name="handle_bid"),
    path("close_bid/<int:pk>", views.close_bid, name="close_bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("handle_comment/<int:pk>", views.handle_comment, name="handle_comment"),
    path("handle_watchlist/<int:pk>",
         views.handle_watchlist, name="handle_watchlist"),

]
