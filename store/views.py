from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Product
from carts.models import Cart,CartItem
from carts.views import _cart_id
from category.models import Category
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def store(request,category_slug=None):
    category = None
    products = None

    if category_slug != None:
        categories =  get_object_or_404(Category,slug = category_slug)
        products = Product.objects.filter(category = categories,is_available = True).order_by('id')
        products_count = products.count()
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_items = paginator.get_page(page)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        products_count = products.count()
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_items = paginator.get_page(page)


    context = {
        'products':paged_items,
        'products_count':products_count
    }
    return render(request,'store/store.html',context)

def productDetail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.filter(category__slug=category_slug,slug=product_slug).first()
        inCart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    except Exception as e:
        raise e
    
    context = {
        'single_product':single_product,
        'inCart'        : inCart
    }

    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        products_count = products.count()

    
    context = {
        'products':products,
        'products_count':products_count
    }

    return render(request,'store/store.html',context)