from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from Accounts.models import UserProfile
from Carts.models import CartItem
from Products.models import Product
from .models import Order,OrderProduct

import datetime


# Create your views here.
def place_order(request, total=0, qty=0):
    current_user = request.user

    try:
        user_profile = UserProfile.objects.get(user = current_user)
    except UserProfile.DoesNotExist:
        return HttpResponse("User Profile Does Not Exist.")
    
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('home')
    total = 0
    grand_total = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.qty)
        qty += cart_item.qty
        grand_total = float(total) + float(6.90)

    if request.method ==  'Post':
        payment_option = request.post.get('flexRadioDefault', 'cash')
        
        try:
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%D'))
            mt = int(datetime.date.today().strftime('%M'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%M%D")
            order_number = current_date + str(cart_count)

            order = Order.objects.create(
                user = current_user,
                mobile = user_profile.mobile,
                email = current_user.email,
                address_line_1 = user_profile.address_1,
                address_line_2 = user_profile.address_2,
                country = user_profile.country,
                state = user_profile.state,
                city = user_profile.city,
                order_note = request.POST.get('order note', ''),
                order_total = grand_total,
                status = 'New',
                order_number = order_number
            )
            for cart_item in cart_items:
                order_product = OrderProduct.objects.create(
                    order = order,
                    product = cart_item.product,
                    qty = cart_item.qty,
                    product_price = cart_item.product.price,
                    user = user_profile,
                )
                product = Product.objects.get(id = cart_item.product.id)
                if product.stock >= cart_item.qty:
                    product.stock -= cart_item.qty
                    product.save()
                else:
                    return HttpResponse("{} : Not enough stock available for the moment.".format(product.name))
                cart_item.delete()
            
            send_order_confirmation_email(current_user, order)

            if payment_option == 'cash':
                return redirect('order_complete')
            else:
                return redirect('payment')
            
        except Exception as e:
            return redirect('error occured:' +str(e))
        
    context = {
        'user':  current_user,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'total': total
    }
    return render(request, 'orders/checkout.html', context)
          

def send_order_confirmation_email(user, order):
    try:
        user_profile = UserProfile.objects.get(user = user)
    except UserProfile.DoesNotExist:
        return HttpResponse("user Profile does not exist.")
    email_subject = "thanks for your Order."
    email_body = render_to_string('orders/order-success.html'), {
        'user': user_profile
    }

    email = EmailMessage(
        subject= email_subject,
        body= email_body,
        from_email= settings.DEFAULT_FROM_EMAIL,
        to = [user.email],
    )

    email.content_subtype = 'html'
    email.send()
