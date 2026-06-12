from django.urls import path
from . import views

app_name ="ecsite"

urlpatterns = [
    path("", views.top, name="top"),
    path("viewShoppingcart/", views.ViewShoppingCart.as_view(), name="view_shopping_cart"),
    path("userLogin/", views.UserLogin.as_view(), name="user_login"),
    path("searchItem/", views.SearchItem.as_view(), name="search_item"),
    path("itemDetail/<int:item_id>", views.ShowItemDetail.as_view(), name="item_detail")
]