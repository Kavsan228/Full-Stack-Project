import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from .models import Product, Order
from .forms import CustomUserCreationForm, CheckoutForm
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Product

# Dictionary to store specific product prices
specific_product_prices = {
    'Bluebird Studio': 9999,
    'Dove Studio - Violinburst': 1500,
    'Epiphone Slash J-45': 1800,
    'Frontier Burst': 2222,
    'J-200 EC Studio Parlor - Vintage Natural': 1999,
    'J-200 EC Studio': 2100,
    '1959 ES-355 - Cherry Red': 1600,
    'B.B. King Lucille - Ebony': 1800,
    'Dave Grohl DG-335 - Pelham Blue': 1450,
    'Emperor Swingster': 1750,
    'ES-335 - Watermelon Red': 2200,
    'ES-345 - Tri-Burst, Exclusive': 2050,
    '1963 Les Paul SG Custom': 2400,
    'Adam Jones 1979 Les Paul': 2600,
    'Dave Mustaine Flying V': 2300,
    'Extura Prophecy': 1950,
    'GhostHorse Explorer': 2100,
    'Jimi Hendrix Love Drops Flying V - Ebony': 2250,
    'Les Paul Standard 50s Plain Top - Goldtop': 2500,
    'Les Paul Standard 60s - Cobra Burst': 2750,
    'Rex Brown Thunderbird': 2650,
    'SG Prophecy': 2800
}

# Fully written product data
product_data = [
    {'id': 1, 'name': 'Bluebird Studio', 'price': 9999, 'image_url': 'images/cataloge/eppiphone_acoustics/Bluebird Studio.png'},
    {'id': 2, 'name': 'Dove Studio - Violinburst', 'price': 1500, 'image_url': 'images/cataloge/eppiphone_acoustics/Dove Studio - Violinburst.png'},
    {'id': 3, 'name': 'Epiphone Slash J-45', 'price': 1800, 'image_url': 'images/cataloge/eppiphone_acoustics/Epiphone Slash J-45.png'},
    {'id': 4, 'name': 'Frontier Burst', 'price': 2222, 'image_url': 'images/cataloge/eppiphone_acoustics/Frontier Burst.png'},
    {'id': 5, 'name': 'J-200 EC Studio Parlor - Vintage Natural', 'price': 1999, 'image_url': 'images/cataloge/eppiphone_acoustics/J-200 EC Studio Parlor - Vintage Natural.png'},
    {'id': 6, 'name': 'J-200 EC Studio', 'price': 2100, 'image_url': 'images/cataloge/eppiphone_acoustics/J-200 EC Studio.png'},
    {'id': 7, 'name': '1959 ES-355 - Cherry Red', 'price': 1600, 'image_url': 'images/cataloge/eppiphone_hollow/1959 ES-355 - Cherry Red.png'},
    {'id': 8, 'name': 'B.B. King Lucille - Ebony', 'price': 1800, 'image_url': 'images/cataloge/eppiphone_hollow/B.B. King Lucille - Ebony.png'},
    {'id': 9, 'name': 'Dave Grohl DG-335 - Pelham Blue', 'price': 1450, 'image_url': 'images/cataloge/eppiphone_hollow/Dave Grohl DG-335 - Pelham Blue.png'},
    {'id': 10, 'name': 'Emperor Swingster', 'price': 1750, 'image_url': 'images/cataloge/eppiphone_hollow/Emperor Swingster.png'},
    {'id': 11, 'name': 'ES-335 - Watermelon Red', 'price': 2200, 'image_url': 'images/cataloge/eppiphone_hollow/ES-335 - Watermelon Red.png'},
    {'id': 12, 'name': 'ES-345 - Tri-Burst, Exclusive', 'price': 2050, 'image_url': 'images/cataloge/eppiphone_hollow/ES-345 - Tri-Burst, Exclusive.png'},
    {'id': 13, 'name': '1963 Les Paul SG Custom', 'price': 2400, 'image_url': 'images/cataloge/eppiphone_solid/1963 Les Paul SG Custom.png'},
    {'id': 14, 'name': 'Adam Jones 1979 Les Paul', 'price': 2600, 'image_url': 'images/cataloge/eppiphone_solid/Adam Jones 1979 Les Paul.png'},
    {'id': 15, 'name': 'Dave Mustaine Flying V', 'price': 2300, 'image_url': 'images/cataloge/eppiphone_solid/Dave Mustaine Flying V.png'},
    {'id': 16, 'name': 'Extura Prophecy', 'price': 1950, 'image_url': 'images/cataloge/eppiphone_solid/Extura Prophecy.png'},
    {'id': 17, 'name': 'GhostHorse Explorer', 'price': 2100, 'image_url': 'images/cataloge/eppiphone_solid/GhostHorse Explorer.png'},
    {'id': 18, 'name': 'Jimi Hendrix Love Drops Flying V - Ebony', 'price': 2250, 'image_url': 'images/cataloge/eppiphone_solid/Jimi Hendrix Love Drops Flying V - Ebony.png'},
    {'id': 19, 'name': 'Les Paul Standard 50s Plain Top - Goldtop', 'price': 2500, 'image_url': 'images/cataloge/eppiphone_solid/Les Paul Standard 50s Plain Top - Goldtop.png'},
    {'id': 20, 'name': 'Les Paul Standard 60s - Cobra Burst', 'price': 2750, 'image_url': 'images/cataloge/eppiphone_solid/Les Paul Standard 60s - Cobra Burst.png'},
    {'id': 21, 'name': 'Rex Brown Thunderbird', 'price': 2650, 'image_url': 'images/cataloge/eppiphone_solid/Rex Brown Thunderbird .png'},
    {'id': 22, 'name': 'SG Prophecy', 'price': 2800, 'image_url': 'images/cataloge/eppiphone_solid/SG Prophecy.png'},
]

def generate_product_data():
    # Fetch all products from the database
    return Product.objects.all()

class CustomLoginView(LoginView):
    template_name = 'login.html'

def home(request):
    products = generate_product_data()
    return render(request, 'index.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_html = render_to_string('cart_items.html', {'cart': cart, 'products': get_cart_products(cart)})
        total_price = get_total_price(cart)
        return JsonResponse({'success': True, 'cart_html': cart_html, 'total_price': total_price})

    return redirect('view_cart')

def remove_product_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_html = render_to_string('cart_items.html', {'cart': cart, 'products': get_cart_products(cart)})
        total_price = get_total_price(cart)
        return JsonResponse({'success': True, 'cart_html': cart_html, 'total_price': total_price})

    return redirect('view_cart')

def empty_cart(request):
    if request.method == "POST":
        # Clear the cart session
        request.session['cart'] = {}
        request.session.modified = True

        # Redirect back to the cart page
        return redirect('view_cart')
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_cart_products(cart):
    product_data = generate_product_data()
    products = [product for product in product_data if str(product.id) in cart]
    for product in products:
        product.total_price = product.price * cart[str(product.id)]
    return products

def get_total_price(cart):
    product_data = generate_product_data()
    return sum(product.price * quantity for product_id, quantity in cart.items() for product in product_data if product.id == int(product_id))

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })
            total_price += product.price * quantity
        except Product.DoesNotExist:
            continue

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def account(request):
    return render(request, 'account.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Retrieve cart from session
            cart = request.session.get('cart', {})
            cart_items = []
            total_price = 0

            # Fetch product details and calculate total price
            for product_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    cart_items.append({
                        'id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'quantity': quantity,
                        'image_url': product.image,
                    })
                    total_price += product.price * quantity
                except Product.DoesNotExist:
                    continue

            # Save the order
            order = Order.objects.create(
                user=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code'],
                country=form.cleaned_data['country'],
                total_price=total_price,
                cart_items=cart_items,
            )

            # Clear the cart
            request.session['cart'] = {}
            request.session.modified = True

            # Redirect to success page
            return redirect('checkout_success')
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})

def checkout_success(request):
    return render(request, 'checkout_success.html')

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def acoustics(request):
    products = Product.objects.filter(image__icontains='eppiphone_acoustics')
    return render(request, 'acoustics.html', {'products': products})

def solid(request):
    products = Product.objects.filter(image__icontains='eppiphone_solid')
    return render(request, 'solid.html', {'products': products})

def hollow(request):
    products = Product.objects.filter(image__icontains='eppiphone_hollow')
    return render(request, 'hollow.html', {'products': products})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@csrf_exempt
def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action')

        # Get the cart from the session
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            if action == 'increase':
                cart[str(product_id)] += 1
            elif action == 'decrease' and cart[str(product_id)] > 1:
                cart[str(product_id)] -= 1

            # Save the updated cart back to the session
            request.session['cart'] = cart

            return JsonResponse({
                'success': True,
                'new_quantity': cart[str(product_id)],
            })

    return JsonResponse({'success': False})
