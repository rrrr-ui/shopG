from django.shortcuts import render
from django.views.generic import View
from ecsite.forms import ItemSearchForm
from ecsite.models import Item

def top(request):
    return render(request, "ecsite/main.html")

class SearchItem(View):
    def get(self,request, *args, **kwargs):
        form = ItemSearchForm(request.GET)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "ecsite/main.html",context)
        keyword = request.GET.get("keyword")
        category = request.GET.get("category")
        #print(category)
        if category == "すべて":
            search_result = Item.objects.filter(name__icontains=keyword)
        else:
            search_result = Item.objects.filter(name__icontains=keyword, category__name = category)

        context = {
            "keyword": keyword,
            "category": category,
            "search_result": search_result,
        }

        return render(request, "ecsite/searchResult.html",context)

    def post(self,request, *args, **kwargs):
        return render(request, "ecsite/main.html")
    
class ShowItemDetail(View):
    def get(self, request, *args, **kwargs):
        item_id = kwargs["item_id"]
        #print(item_id)
        item = Item.objects.get(item_id=item_id)
        stock_list = []
        for num in range(0, item.stock):
            stock_list.append(num+1)
        context = {
            "item": item,
            "stock": stock_list,
        }
        return render(request, "ecsite/itemDetail.html", context)

    def post(self, request, *args, **kwargs):
        pass

class UserLogin(View):
    def get(self, request):
        return render(request, "ecsite/main.html")

    def post(self, request):
        pass

class ViewShoppingCart(View):
    def get(self, request):
        return render(request, "ecsite/cart.html")

    def post(self, request):
        pass