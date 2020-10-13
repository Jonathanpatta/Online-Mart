from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from .forms import NewUserForm
from .models import Item,Profile,Order,UserCart

import random,string

import datetime

import smtplib

import json

# Create your views here.


def homepage(request):
    items=None
    if request.method=="POST":
        query = request.POST.get("nav_search")
        
        items = Item.objects.filter(name__icontains=query)|Item.objects.filter(description__icontains=query)
        if(len(items)==0):
            messages.warning(request,f"No items found related to {query}")
    
    else:
        items = Item.objects.all()
    
    cart_items = request.COOKIES.get("cart")
    if cart_items is not None:
        cart_items = json.loads(cart_items)['items']
        cart_items = [[int(k), int(v)] for k, v in cart_items.items()]
    
    
    response = render(request,"main/home.html",{"items":items,"cart_items":cart_items})
    if request.COOKIES.get("cart") is None:
        mycart = json.dumps({'items':{}})
        response.set_cookie("cart",mycart)
    
    

    return response



def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})




def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            random_otp = ''.join(random.choice(string.ascii_letters) for i in range(6))
            exp_time = datetime.datetime.now() + datetime.timedelta(days=1)
            profile = Profile(user=user,otp=random_otp,otp_expiration_date=exp_time)
            profile.save()
            login(request, user)
            print(profile.otp,profile.otp_expiration_date)

            sender = 'jonathan.patta@gmail.com'
            receivers = [user.email]

            message = f"""From: From Person <from@fromdomain.com>
                        To: To Person <{user.email}>
                        Subject: activation otp

                        This is the otp: {random_otp} and expires on {profile.otp_expiration_date}.
                        """

            #try:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender,'udxfkgullsrkfauu')
            server.sendmail(sender, receivers, message)   
            server.close()      
            print("Successfully sent email")
            messages.info(request,f"Otp sent to {user.email} and expires by {profile.otp_expiration_date}")
            #except smtplib.SMTPException:
            #username = form.cleaned_data.get('username')
            #login(request, user)
            #return redirect("main:homepage")
            return redirect("main:activation")
            #user = form.save()
            #username = form.cleaned_data.get('username')
            #login(request, user)
            #return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


@login_required(login_url='/login/')
def activation(request):
    if request.method=="POST":

        otp = request.POST.get("otp")
        profile = Profile.objects.get(user=request.user)
        print(otp,profile.otp)
        if otp==profile.otp:
            if timezone.now() < profile.otp_expiration_date:
                profile.verified = True
                profile.save()
                return redirect("main:homepage")

    
    return render(request,"main/activation.html",{})




@login_required(login_url='/login/')
def cart(request):
    user_cart = request.COOKIES.get("cart")
    user_cart = json.loads(user_cart)

    cart_items = user_cart["items"]
    items = []
    price = 0
    for item_pk in cart_items:
        item = Item.objects.get(pk=item_pk)
        
        if item is not None:
            price += item.price * cart_items[item_pk]
            items.append([item,cart_items[item_pk],item.price])
            
    
    #items = Item.objects.all()

        
    context={"cart":user_cart,
            "items":items,
            "total_price":price}
    response = render(request,"main/cart.html",context)
    return response



@login_required(login_url='/login/')
def purchase(request):
    cart_json_string = request.COOKIES.get("cart")
    cart = json.loads(cart_json_string)

    if len(cart['items']) is 0:
        return redirect("main:homepage")
    order = Order(user=request.user,Cart_json=cart_json_string)
    order.save()
    
    items = []
    price=0
    for item_pk in cart['items']:
        item = Item.objects.get(pk=item_pk)
        if item is not None:
            price += item.price * cart['items'][item_pk]
            order.items.add(item)
            order.save()
    
    order.Total_price=price
    order.save()
    messages.success(request,"Purchase was successful!! check order history to review your order")
    return redirect("main:homepage")




@login_required(login_url='/login/')
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by("time_of_creation")
    order_with_items = []
    for order in orders:
        item_values=[]
        cart = json.loads(order.Cart_json)
        for item in order.items.all():
            item_values.append([item,cart['items'][f"{item.pk}"]])
        order_with_items.append([order,item_values])
    context = {
        "orders":order_with_items,
    }
    return render(request,"main/Orders.html",context)


@login_required(login_url='/login/')
def get_cart_items(request):
    
    cart = request.COOKIES.get("cart")
    user_cart = UserCart(Cart_json=cart,user=request.user)
    user_cart.save()
    return JsonResponse(cart,safe=False)




def item_view(request,pk):
    item = get_object_or_404(Item,pk=pk)
    context = {"item":item}
    return render(request,"main/item_view.html",context)