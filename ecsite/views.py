from django.shortcuts import render, redirect
from django.views.generic import View
from ecsite.forms import ItemSearchForm
from ecsite.models import Item, Cart
from . import forms, models

def top(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return render(request, "ecsite/main.html")
    user = models.User.objects.get(user_id=user_id)
    context = {
        "is_login": request.session.get("is_login"),
        "user_name": user.name
    }
    return render(request,'ecsite/main.html',context)


class SearchItem(View):
    def get(self,request, *args, **kwargs):
        form = ItemSearchForm(request.GET)

        keyword = request.GET.get("keyword")
        category = request.GET.get("category")

        if category == "すべて":
            search_result = Item.objects.filter(name__icontains=keyword)
        else:
            search_result = Item.objects.filter(name__icontains=keyword, category__name = category)

        context = {
            "keyword": keyword,
            "category": category,
            "search_result": search_result,
            "is_login": request.session.get("is_login")
        }
        return render(request, "ecsite/searchResult.html",context)

    def post(self,request, *args, **kwargs):
        if request.session.get("is_login"):
            context = {
                "is_login": request.session.get("is_login")
            }
            return render(request, "ecsite/cart.html", context)
        context = {
            "is_login": request.session.get("is_login"),
            "login_form": forms.LoginUserForm(),
        }
        return render(request, "ecsite/login.html",context)
    
class ShowItemDetail(View):
    def get(self, request, *args, **kwargs):
        item_id = kwargs["item_id"]

        item = Item.objects.get(item_id=item_id)
        item.item_id = item_id
        stock_list = []
        for num in range(0, item.stock):
            stock_list.append(num+1)
        context = {
            "item": item,
            "stock": stock_list,
            "is_login": request.session.get("is_login")
        }
        return render(request, "ecsite/itemDetail.html", context)

    def post(self, request, *args, **kwargs):
        pass

class UserLogin(View):
    def get(self, request):
        if request.session.get("is_login"):
            context = {
                "is_login": request.session.get("is_login")
            }
            return render(request,'ecsite/main.html',context)
        context = {
            "is_login": request.session.get("is_login"),
            "login_form": forms.LoginUserForm(),
        }
        return render(request, "ecsite/login.html", context)

    def post(self, request):
        if request.session.get("is_login"):
            context = {
                "is_login": request.session.get("is_login")
            }
            return render(request, 'ecsite/main.html', context)
        login_form = forms.LoginUserForm(request.POST)
        if login_form.is_valid():
            user_id = login_form.cleaned_data.get("id")
            password = login_form.cleaned_data.get("password")
            try:
                user = models.User.objects.get(user_id=user_id)
            except:
                message = "ユーザが存在しません"
                return render(request, "ecsite/login.html",locals())
            if user.password == password:
                request.session["is_login"]=True
                request.session["user_id"]=user.user_id
                context = {
                    "is_login": request.session.get("is_login"),
                    "user_name": user.name
                }
                return render(request,'ecsite/main.html',context)
            else:
                message = "パスワードが正しくありません"
                return render(request, "ecsite/login.html", locals())
        else:
            return render(request, "ecsite/login.html", locals())

class ViewShoppingCart(View):
    def get(self, request):
        context = {
            "is_login": request.session.get("is_login")
        }
        return render(request, "ecsite/cart.html",context)

    def post(self, request):
        pass

def logout(request):
    request.session.flush()
    # print("ログアウトしました")
    context = {
        "login_form": forms.LoginUserForm(),
    }
    return render(request, "ecsite/login.html", context)

class RegistUser(View):
    def get(self, request):
        context = {
            "regist_form": forms.RegistUserForm(),
        }
        return render(request, "ecsite/registerUser.html", context)

    def post(self, request):
        regist_form = forms.RegistUserForm(request.POST)
        if not regist_form.is_valid():
            context = {
                 "regist_form": regist_form
            }
            return render(request, "ecsite/registerUser.html", context)
        context = {
            "registuser_data": regist_form.cleaned_data,
        }
        return render(request, "ecsite/registerUserConfirm.html", context)


class RegistUserConfirm(View):
    def get(self, request):
        pass

    def post(self, request):
        new_user = models.User()

        new_user.user_id = request.POST["id"]
        new_user.password = request.POST["password"]
        new_user.name = request.POST["name"]
        new_user.address = request.POST["address"]

        new_user.save()
        context = {
            "name": new_user.name,
        }
        return render(request, "ecsite/registerUserCommit.html", context)
    
class UserInfo(View):
    def get(self,request):
        user_id = request.session.get("user_id")
        user = models.User.objects.get(user_id=user_id)
        
        context = {
            "user": user,
        }
        return render(request, "ecsite/userInfo.html", context)

    def post(self,request):
        pass
        

class UserUpdate(View):
    def get(self,request):
        user_id = request.session.get("user_id")
        user = models.User.objects.get(user_id=user_id)
        update_form = forms.UpdateUserForm(initial={"id": user.user_id, "name": user.name, "address": user.address,})
        context = {
            "user_id": user_id,
            "update_form": update_form,
        }
        print("a")
        return render(request, "ecsite/updateUser.html",context)

    def post(self, request):
        # update_form = forms.UpdateUserForm(request.POST)
        # if not update_form.is_valid():
        #     context = {
        #          "update_form": update_form
        #     }
        #     return render(request, "ecsite/updateUser.html", context)
        # context = {
        #     "updateuser_data": update_form.cleaned_data,
        # }
        # print("b")
        # return render(request, "ecsite/updateUserConfirm.html", context)
        pass

class UserUpdateConfirm(View):
    def get(self, request):
        user_id = request.session.get("user_id")
        user = models.User.objects.get(user_id=user_id)

        user.password = request.GET["password"]
        user.name = request.GET["name"]
        user.address = request.GET["address"]
        user.save()
        context = {
            "user_id": user_id,
            "user": user,
        }
        print("c")
        return render(request, "ecsite/updateUserCommit.html", context)

    def post(self,request):
        user_id = request.session.get("user_id")
        update_form = forms.UpdateUserForm(request.POST)
        if not update_form.is_valid():
            context = {
                "user_id": user_id,
                 "update_form": update_form,
            }
            return render(request, "ecsite/updateUser.html", context)
        context = {
            "user_id": user_id,
            "updateuser_data": update_form.cleaned_data,
        }
        print("d")
        return render(request, "ecsite/updateUserConfirm.html", context)

    
class UserWithdraw(View):
    def get(self,request):
        user_id = request.session.get("user_id")
        user = models.User.objects.get(user_id = user_id)
        context = {
            "name": user.name,
        }
        return render(request, "ecsite/withdrawConfirm.html", context)
    
    def post(self,request):
        user_id = request.session.get("user_id")
        user = models.User.objects.get(user_id = user_id)
        name =  user.name
        user.delete()
        request.session.flush()
        context = {
            "name": name,
            "login_form": forms.LoginUserForm(),
        }
        return render(request,"ecsite/withdrawCommit.html",context)

class ShoppingCart(View):
    def get(self,request):
        user_id = request.session.get("user_id")
        if not user_id:
            context = {
                "login_form": forms.LoginUserForm(),
            }
            return render(request, "ecsite/main.html",context)
        
        cart_itemlist = Cart.objects.filter(user=user_id)
        total = 0
        for cart in cart_itemlist:
            cart.subtotal = cart.item.price * cart.amount
            total += cart.subtotal
        print(total)
        print(user_id)
        context = {
            "total": total,
            "cart_itemlist": cart_itemlist,
        }
        return render(request, "ecsite/cart.html", context)

    def post(self,request):
        user_id = request.session.get("user_id")
        if not user_id:
            context = {
                "login_form": forms.LoginUserForm(),
            }
            return render(request, "ecsite/login.html",context)
        user_cart = models.Cart()
        user_cart.amount = request.POST.get("amount")
        item_id = request.POST.get("item_id")
        item = models.Item.objects.get(item_id=item_id)
        user_cart.item = item
        user = models.User.objects.get(user_id=user_id)
        user_cart.user = user
        user_cart.save()
        cart_itemlist = Cart.objects.filter(user=user).select_related("item")
        
        total = 0
        for cart in cart_itemlist:
            cart.subtotal = cart.item.price * cart.amount
            total += cart.subtotal

        context = {
            "total": total,
            "cart_itemlist": cart_itemlist,
        }
        return render(request, "ecsite/cart.html",context)
    