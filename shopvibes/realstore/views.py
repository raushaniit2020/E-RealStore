
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import CustomerProfileForm, CustomerRegisterationForm, LoginForm
from django.contrib import messages

from .models import Cart, Customer, OrderPlaced, Product 
# Create your views here.
# def home(request):
#     return render(request, 'realstore/home.html')

class ProductView(View):
    def get(self, request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request, 'realstore/home.html', {'topwears':topwears , 'bottomwears': bottomwears, 'mobiles': mobiles})

def mobile(request, data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif (data=='mi' or data=='samsung' or data=='redmi' or data=='apple'):
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif (data=='below'):
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=30000)
    elif (data=='above'):
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=30000)

    return render(request, 'realstore/mobile.html', {'mobiles':mobiles})

# def profile(request):
#     return render(request, 'realstore/profile.html')

class CustomerProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()    
        return render(request, 'realstore/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            data = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            data.save()
            messages.success(request, 'Profile Updated Succesfully!')
        return render(request, 'realstore/profile.html', {'form': form, 'active': 'btn-primary'})

# def customerregistration(request):
#     return render(request, 'realstore/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form=CustomerRegisterationForm()
        return render(request, 'realstore/customerregistration.html', {'form': form})
    def post(self, request):
        form=CustomerRegisterationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registered Succesfully')
            form.save()
        return render(request, 'realstore/customerregistration.html', {'form': form})


# def login(request):
#     return render(request, 'realstore/login.html')

# class LoginView(View):
#     def get(self, request):
#         form=LoginForm()
#         return render(request, 'realstore/login.html', {'form': form})
        

def addToCart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')
    

def ShowCart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        total_amount=0.0
        amount=0.0
        shipping_amount=50.0
        if cart:
            for p in cart:
                if p.user==user:
                    amount=p.product.discounted_price+amount
                    total_amount=amount+shipping_amount
            return render(request, 'realstore/addtocart.html', {'carts': cart, 'amount': amount, 'total_amount': total_amount, 'shipping_amount': shipping_amount})
        else:
            return render(request, 'realstore/emptycart.html')


def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)

    return render(request, 'realstore/orders.html', {'order_placed':op})

# def productDetail(request):
#     return render(request, 'realstore/productdetail.html')
class productDetailView(View):
    def get(self, request, pk):
        unique_product=Product.objects.get(pk=pk)
        return render(request, 'realstore/productdetail.html', {'unique_product':unique_product})


def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request, 'realstore/address.html', {'address': address, 'active': 'btn-primary'})

def checkout(request):
    user=request.user
    address=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            temp_amount=(p.quantity*p.product.discounted_price)
            amount+=temp_amount
        total_amount=amount+shipping_amount

    return render(request, 'realstore/checkout.html', {'address':address, 'total_amount': total_amount, 'cart_items': cart_items})

def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


def buyNow(request):
    return render(request, 'realstore/buynow.html')
