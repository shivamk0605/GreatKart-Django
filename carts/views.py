from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.

def _cart_id(request):    # function starting with underscore are called as private functions
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id 


def addCart(request,product_id):
    product = Product.objects.get(id = product_id)
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            print("key : ",key," value : ", value)

            try:
                variation = Variation.objects.get(product=product,variation_category=key,variation_value=value)
            except Exception as e:
                raise e


    # if request.method=="POST":

    
    

            

            


    # creating the Cart
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
            )
        cart.save()
    
    # creating the cartItems 
    try:
        cart_item = CartItem.objects.get(product = product,cart = cart)
        cart_item.quantity += 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        cart_item.save()
 

    return redirect('cart')

def reduceCart(request,product_id):
    cart_obj = Cart.objects.get(cart_id=_cart_id(request))
    product_obj  = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(cart=cart_obj,product=product_obj)
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart') 

def removeCartItem(request,product_id):
    cart_obj = Cart.objects.get(cart_id=_cart_id(request))
    product_obj  = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(cart=cart_obj,product=product_obj)
    cart_item.delete()
    return redirect('cart')


def cart(request,quantityAllCartItems=0,totalCartAmount=0,cart_items=None):

    try:
        tax = 0
        totalAmountPayable = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active = True)
        for cart_item in cart_items:
            totalCartAmount += ( cart_item.quantity * cart_item.product.price) 
            quantityAllCartItems += cart_item.quantity

        # taxes = 2 %
        tax = (2*totalCartAmount)/100
        totalAmountPayable = totalCartAmount + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items':cart_items,
        'totalCartAmount':totalCartAmount,
        'quantityAllCartItems':quantityAllCartItems,
        'totalAmountPayable':totalAmountPayable,
        'tax':tax
    }
    return render(request,'store/cart.html',context)


