from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        user = request.user
        cart = Cart.objects.filter(user=user)
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        no_of_prods=0
        if cart_product:
            for p in cart_product:
                no_of_prods+=1
        else:
            no_of_prods=0            
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,'no_of_prods':no_of_prods})
        
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_in_cart = False
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(Q(user=request.user) & Q(product=product.id)).exists()       
        return render(request,'app/productdetail.html',{'prod':product,'item_in_cart':item_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

    
@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    shipping_amount = 40.0
    amount=0.0
    total = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
            per_unit_amount = p.product.discounted_price
            temp_amount = per_unit_amount * p.quantity
            amount += temp_amount
        total = amount + shipping_amount
        return render(request,'app/addtocart.html',{'carts':cart,'total':total, 'amount':amount,'shipping_amount':shipping_amount})
    return render(request,'app/emptycart.html')
    
    
@login_required  
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        shipping_amount = 40.0
        amount=0.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            per_unit_amount = p.product.discounted_price
            temp_amount = per_unit_amount * p.quantity
            amount += temp_amount
        total = amount + shipping_amount
            
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total,
            'shipping_amount': shipping_amount,
        }
        return JsonResponse(data)
 
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        shipping_amount = 40.0
        amount=0.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            per_unit_amount = p.product.discounted_price
            temp_amount = per_unit_amount * p.quantity
            amount += temp_amount
        total = amount + shipping_amount
            
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total,
            'shipping_amount': shipping_amount,
        }
        return JsonResponse(data)       

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        shipping_amount = 40.0
        amount=0.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            per_unit_amount = p.product.discounted_price
            temp_amount = per_unit_amount * p.quantity
            amount += temp_amount
        total = amount + shipping_amount
            
        data = {
            'amount': amount,
            'totalamount': total,
        }
        return JsonResponse(data)
    
@login_required
def buy_now(request):
    if request.user.is_authenticated:
        return render(request, 'app/buynow.html')
    else:
        return redirect('login')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

    
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'op':op})

@login_required
def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data=='Samsung' or data=='Apple':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

        
@login_required
def laptop(request,data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data=='HP' or data=='Apple':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    return render(request, 'app/laptops.html',{'laptops':laptops})


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'congratulations, Registerd Successfully!')
        return render(request,'app/customerregistration.html',{'form':form})
    
    
@method_decorator(login_required,name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
        
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!!! Profile updated successfully...')
        return render(request,'app/profile.html',{'active':'btn-primary','form':form})

@login_required    
def checkout(request):
    address = Customer.objects.filter(user = request.user)
    cart_items = Cart.objects.filter(user = request.user)
    shipping_amount = 40.0
    amount = 0.0
    temp_amount = 0.0
    total = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
        per_unit_amount = p.product.discounted_price
        temp_amount = per_unit_amount * p.quantity
        amount += temp_amount
        total = amount + shipping_amount
    data = {
            'address': address,
            'total': total,
            'cart_items': cart_items
        }
    return render(request, 'app/checkout.html', {'data':data})
  
@login_required    
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,product=c.product,customer=customer,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
