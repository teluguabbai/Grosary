from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Cart, Address, Order
from .forms import ProductForm, AddressForm

#  User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

#  User Login View (Differentiating Admin and User)
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard' if user.is_staff else 'home')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

#  Home View (Displays Grocery Products)
@login_required
def home(request):
    products = Product.objects.all()
    return render(request, "myapp/home.html", {"products": products})

#  Add to Cart (Ensuring User Association)
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

#  Cart Page View
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    user_has_address = Address.objects.filter(user=request.user).exists()
    return render(request, "myapp/cart.html", {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "user_has_address": user_has_address
    })

#  Remove from Cart
@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart')

#  Payment Page
@login_required
def payment(request):
    return render(request, "myapp/payment.html")

#  Order Success Page (Clears Cart After Purchase)
@login_required
def order_success(request):
    Cart.objects.filter(user=request.user).delete()
    return render(request, "myapp/order_success.html")

#  Admin Dashboard
@staff_member_required
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, "myapp/admin_dashboard.html", {"products": products})

# Add Product View
@staff_member_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form = ProductForm()
    return render(request, "myapp/add_product.html", {"form": form})

# Delete Product
@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect("admin_dashboard")

# Checkout View
@login_required
def checkout(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect("payment")
    else:
        form = AddressForm()
    return render(request, "myapp/checkout.html", {"form": form})

# COD Payment
@login_required
def cod_payment(request):
    if request.method == "POST":
        total_amount = request.POST.get("total_amount")
        Order.objects.create(user=request.user, amount=total_amount, status="Pending", payment_method="COD")
        Cart.objects.filter(user=request.user).delete()
        return render(request, "myapp/order_success.html", {"message": "Order placed successfully! Pay on delivery."})
    return redirect("cart")

#  User Profile View
@login_required
def profile_view(request):
    user_address = Address.objects.filter(user=request.user).first()
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'myapp/profile.html', {
        'user': request.user,
        'user_address': user_address,
        'orders': orders,
    })

# Update Address
@login_required
def update_address(request):
    if request.method == "POST":
        address_id = request.POST.get("address_id")
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.street = request.POST.get("street")
        address.city = request.POST.get("city")
        address.state = request.POST.get("state")
        address.zip_code = request.POST.get("zip_code")
        address.country = request.POST.get("country")
        address.save()
        return redirect("profile")
    return redirect("home")
