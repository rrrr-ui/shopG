from django.urls import path
from . import views

app_name ="ecsite"

urlpatterns = [
    path("", views.top, name="top"),
    path("userLogin/", views.UserLogin.as_view(), name="user_login"),
    path("searchItem/", views.SearchItem.as_view(), name="search_item"),
    path("itemDetail/<int:item_id>", views.ShowItemDetail.as_view(), name="item_detail"),
    path("userLogout/", views.logout, name="user_logout"),
    path("registUser/", views.RegistUser.as_view(), name="user_regist"),
    path("registUserConfirm/", views.RegistUserConfirm.as_view(), name="user_regist_confirm"),
    path("userInfo/", views.UserInfo.as_view(), name="user_info"),
    path("userUpdate/", views.UserUpdate.as_view(), name="user_update"),
    path("userUpdateConfirm/", views.UserUpdateConfirm.as_view(), name="user_update_confirm"),
    path("userWithdraw/", views.UserWithdraw.as_view(), name="user_withdraw"),
    path("shoppingCart/", views.ShoppingCart.as_view(), name="shopping_cart"),
]