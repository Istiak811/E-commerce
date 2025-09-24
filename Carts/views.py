from django.shortcuts import render,get_object_or_404,redirect
from Products import models
from . import models
from django.core.exceptions import  ObjectDoesNotExist

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_slug):
    url = request.META.get('HTTP_REFERER')
    product = models.Product.objects.get(slug = product_slug)
    
    try:
        cart = models.Cart.objects.get(cart_id = _cart_id(request))
    except models.Cart.DoesNotExist:
        cart = models.Cart.objects.create(cart_id = _cart_id(request))
    cart.save()

    try:
        cart_item = models.CartItem.objects.get(product=product,cart=cart)
        cart_item.qty += 1
        cart_item.save()

    except models.CartItem.DoesNotExist:
        cart_item = models.CartItem.objects.create(product=product, cart=cart, user=request.user, qty=1)
        cart_item.save()

    return redirect(url)

def cart(request, total=0, qty=0, cart_item=None):
    try:
        grand_total = 0
        total = 0
        if request.user.is_authenticated:
            cart_items = models.CartItem.objects.filter(user = request.user, is_active = True)
        else:
            cart = models.Cart.objects.get(cart_id=_cart_id(request))
            cart_items = models.CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.discount_price * cart_item.qty)
            qty += cart_item.qty
        grand_total = float(total) + float(6.90)
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'qty': qty,
        'cart_items': cart_items,
        'grand_total': grand_total,
    }
    return render(request, 'carts/cart.html', context)

def remove_cart(request,product_slug):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(models.Product, slug = product_slug)
    try:
        if request.user.is_authenticated:
            cart_item = models.CartItem.objects.get(user = request.user, product=product)
        else:
           cart = models.Cart.objects.get(cart_id=_cart_id(request))
           cart_item = models.CartItem.objects.get(cart = cart, product=product)
        if cart_item.qty > 1:
            cart_item.qty -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect(url)

def remove_cart_item(request,product_slug):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(models.Product, slug = product_slug)

    if request.user.is_authenticated:
            cart_item = models.CartItem.objects.get(user = request.user, product=product)
    else:
        cart = models.Cart.objects.get(cart_id=_cart_id(request))
        cart_item = models.CartItem.objects.get(cart = cart, product=product)
    cart_item.delete()
    return redirect(url)