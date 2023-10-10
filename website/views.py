from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from django.db.models import Q
import datetime
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
import time
import json
from collections import OrderedDict
from django.contrib import messages  # Import the messages module
from django.http import JsonResponse
import json
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .models import watchlist as w
from django.views import View



# @login_required(login_url='login')
def index(request):
    products = ProductData.objects.all()
    print(products)
    for i in products:
        print(i.product_category)
    context = {"products":products}
    return render(request,'website/index.html',context)

def about(request):
    return render(request,'website/about-us.html')


def terms(request):
    return render(request,'website/terms.html')

@login_required(login_url='login')
def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email =request.POST.get('email')
        subject =request.POST.get('subject')
        message =request.POST.get('message')
        contact_obj = contact_us.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, 'you query is received. we will reply you soon.')
        contact_obj.save()
    
    return render(request,'website/contact.html')

def warrenty(request):
    return render(request,'website/warrenty.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print("USER",user)
            if user is not None:
                login(request, user)
                print("LOGGED IN")
                # logout(request)
                messages.success(request, 'you are login sucessfully')
                return redirect('index')
            else:
                print('else chala')
                messages.error(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'website/account-login.html', context)

def logoutP(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        users = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.create_user(username=users, email=email, password=password)
        user_obj.first_name = users
        user_obj.is_superuser = False
        user_obj.save()

        # Add a success message
        messages.success(request, 'Registration successful! You are now logged in.')

        return redirect('login')
        # return render(request,'website/login.html', context)


@login_required(login_url='login')
def newsletter_sub(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        newsletter_obj = newsletter.objects.create(email=email)
        messages.success(request, 'you have sucessfully subcribed.')
        newsletter_obj.save()

        return redirect('index')

def partnership_form(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        company = request.POST.get('company')
        staff = request.POST.get('staff')
        website = request.POST.get('website')
        comment = request.POST.get('comment')
        if first_name != None:
            pform_obj = distributor.objects.create(first_name=first_name, lat_name=last_name,
                                                email=email, phone=phone_number, country=country,
                                                company=company,staff=staff, website=website, 
                                                comment=comment)
            messages.success(request, 'Your Distribution Form submitted secessfully.')
            pform_obj.save()

        else:
            return render(request, 'website/partnership.html')

        return redirect('partnership')

    return render(request, 'website/partnership.html')

def SearchDataView(request):
    if request.method == 'POST':
        search_obj = request.POST.get('search')
        products = ProductData.objects.filter(product_title__icontains=search_obj)
        context = {'products':products}
        return render(request, 'website/shop-list.html',context)
    

def product_page_single(request,pk):
    user_name = request.user.first_name
    product_data = ProductData.objects.filter(id=int(pk))
    
    context = {'product_data':product_data}
    print(product_data) 
    return render(request, 'website/product-full.html', context)


@login_required(login_url='login')
def add_to_watchlist(request,pk):

    user_id = request.user.id
    # print(pk)
    cc=ProductData.objects.get(id=pk)
    print("coin",cc)
    data=w.objects.filter(Q(user_id=user_id) & Q(coin_ids__id=pk))
    if not data:
        print("No data")
        obj=w.objects.create(user_id=user_id)
        obj.save()
        obj.coin_ids.add(cc)
        messages.success(request, 'Product is sucessfully added to your wishlist..')
    else:
        print("already")

    return redirect("/watchlist")


@login_required(login_url='login')
def add_to_cart(request,pk):

    user_id = request.user.id
    # print(pk)
    cc=ProductData.objects.get(id=pk)
    print("coin",cc)
    data=addtocart.objects.filter(Q(user_id=user_id) & Q(coin_ids__id=pk))
    if not data:
        print("No data")
        obj=addtocart.objects.create(user_id=user_id)
        obj.save()
        obj.coin_ids.add(cc)
        messages.success(request, 'Product is sucessfully added to your cart..')
    else:
        print("already")

    return redirect("/cart")

@login_required(login_url='login')
def add_order(request):
    ob = addtocart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        confirmation_no = request.POST.get('confirmation_no')
        payment_proof = request.POST.get('image')


    user_id = request.user.id
    print('add order',confirmation_no,payment_proof)


    obj=order.objects.create(user_id=user_id, 
                                 confirmation_no=confirmation_no,
                                 payment_proof=payment_proof,
                                 status='Pending')
    obj.save()

    for o in range(len(ob)):
        print("add order...",ob[0].coin_ids.all())

        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            obj.coin_ids.add(obj1)

    messages.success(request, 'Your payment is under review..')
    # cc=ProductData.objects.get(id=pk)
    # print("coin",cc)
    # data=addtocart.objects.filter(Q(user_id=user_id) & Q(coin_ids__id=pk))
    # if not data:
    #     print("No data")
    #     obj=order.objects.create(user_id=user_id, 
    #                              confirmation_no=confirmation_no,
    #                              payment_proof=payment_proof,
    #                              status='Pending')
    #     # obj.save()
    #     # obj.coin_ids.add(cc)
    #     messages.success(request, 'Your payment is under review..')
    # else:
    #     print("already")

    return redirect("/checkout")

@login_required(login_url='login_view')
def watchlist(request):
    ob = w.objects.filter(user_id=request.user.id)
    print(ob)

    lst=[]
    sign_no = []

    for o in range(len(ob)):
        lst1=[]
        print("ss",ob[0].coin_ids.all())
        sign_no.append(o+1)
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            # print("mustafa",obj1)
            lst1.append(obj1)
            lst.append(lst1)

    all_data = zip(sign_no,lst)
    context = {'all_data':all_data}
    return render(request,'website/wishlist.html', context)

@login_required(login_url='login_view')
def cart(request):
    ob = addtocart.objects.filter(user_id=request.user.id)
    print(ob)

    lst=[]
    sign_no = []
    subtotal = 0

    for o in range(len(ob)):
        lst1=[]
        sign_no.append(o+1)
        print("ss",ob[0].coin_ids.all())
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            print("mustafa",float(obj1.price_per_pack))
            subtotal += float(obj1.price_per_pack)
            lst1.append(obj1)
            lst.append(lst1)

            # for product in obj1:
            #     subtotal += product.price_per_pack

            

    all_data = zip(sign_no,lst)
    context = {'all_data':all_data,'subtotal':subtotal}
    return render(request,'website/cart.html', context)


@login_required(login_url='login_view')
def remove_watchlist(request,pk):
    print('main hoon',pk, request.user.id)
    obj=w.objects.get(coin_ids=pk, user_id=request.user.id)
    obj.delete()
    print("muti",pk)
    print(obj)
    #return render(request,"coin/watchlist.html")
    return redirect("/watchlist")

@login_required(login_url='login_view')
def remove_cart(request,pk):
    print('main hoon',pk, request.user.id)
    obj=addtocart.objects.get(coin_ids=pk, user_id=request.user.id)
    obj.delete()
    print("muti",pk)
    print(obj)
    #return render(request,"coin/watchlist.html")
    return redirect("/cart")

def filter_search(request):
    # context = {'products':products}
    if request.method == 'POST':
        make = request.POST.get('make')
        market = request.POST.get('market')
        model = request.POST.get('model')
        body = request.POST.get('body')
        year = request.POST.get('year')

    data_obj = ProductData.objects.filter(make=make, market=market, model=model, body=body, year=year)
    img_lst = []
    data_lst = []

    for im in data_obj:
        if im.suspension_type == 'Front-Suspension':
            data_lst.append(im)
            img_lst.append(im.search_image_file)

    try:
        context = {'products':data_lst, 
                'make':make,
                'market':market,
                'model':model,
                'body':body,
                'year':year,
                'img_url':img_lst[0],
                }
        
    except:
        context = {'products':data_lst, 
                'make':make,
                'market':market,
                'model':model,
                'body':body,
                'year':year,
                'img_url':'None',
                }
               
    return render(request, 'website/shop-table.html',context)


def sema2018(request):
    return render(request,'website/sema2018.html')

def sema2019(request):
    return render(request,'website/sema2019.html')


def initial_data(request):
    print('working fine...........')


    payload = {'product':['Select Make']}

    make_obj = ProductData.objects.all().distinct()

    for product in make_obj:
        # print(product.make)
        if product.make not in payload['product']:
            payload['product'].append(product.make)

    print(payload)
    return JsonResponse({'status':200,"data":payload})

def market_filter(request):
    print('market filter working fine...........')

    selected_make = request.GET.get('name')
    payload = {'market':['Select Market']}
    make_obj = ProductData.objects.filter(make=selected_make)
    
    for ob in make_obj:
        print(ob.market)
        if ob.market not in payload['market']:
            payload['market'].append(ob.market)

    print(payload)
    return JsonResponse({'status':200,"data":payload})


def model_filter(request):
    print('model filter working fine...........')

    selected_market = request.GET.get('name')
    payload = {'model':['Select Model']}

    make_obj = ProductData.objects.filter(make=selected_market.split(',')[1],market=selected_market.split(',')[0])
    
    for ob in make_obj:
        print(ob.model)
        if ob.model not in payload['model']:
            payload['model'].append(ob.model)

    print(selected_market.split(',')[0],selected_market.split(',')[1])
    return JsonResponse({'status':200,"data":payload})


def body_filter(request):
    print('body filter working fine...........')

    selected_market = request.GET.get('name')
    payload = {'body':['Select Body']}

    make_obj = ProductData.objects.filter(make=selected_market.split(',')[0],market=selected_market.split(',')[1],model=selected_market.split(',')[2])
    
    for ob in make_obj:
        print(ob.body)
        if ob.body not in payload['body']:
            payload['body'].append(ob.body)

    print(selected_market.split(',')[0],selected_market.split(',')[1])
    return JsonResponse({'status':200,"data":payload})


def year_filter(request):
    print('year filter working fine...........')

    selected_market = request.GET.get('name')
    payload = {'year':['Select Year']}

    make_obj = ProductData.objects.filter(make=selected_market.split(',')[0],market=selected_market.split(',')[1],model=selected_market.split(',')[2],body=selected_market.split(',')[3])
    
    for ob in make_obj:
        print(ob.year)
        if ob.year not in payload['year']:
            payload['year'].append(ob.year)

    print(selected_market.split(',')[0],selected_market.split(',')[1])
    return JsonResponse({'status':200,"data":payload})


def suspension_filter(request):
    print('suspension_filter working fine...........')

    if request.method == 'POST':
        make = request.POST.get('make')
        market = request.POST.get('market')
        model = request.POST.get('model')
        body = request.POST.get('body')
        year = request.POST.get('year')
        sustype = request.POST.get('sustype')

        print(make,model,year,sustype)

    make_obj = ProductData.objects.filter(make=make,
                                          market=market,
                                          model=model,
                                          body=body,
                                          year=year,
                                         )
    
    print(make_obj)
    data_lst = []
    img_lst = []
    for ob in make_obj:
        print(ob.suspension_type)

        if sustype == 'front':
            if ob.suspension_type == 'Front-Suspension':
                img_lst.append(ob.search_image_file)
                data_lst.append(ob)

        if sustype == 'rear':
            if ob.suspension_type == 'Rear-Suspension':
                img_lst.append(ob.search_image_file)
                data_lst.append(ob)

    try:
        context = {'products':data_lst, 
                'make':make,
                'market':market,
                'model':model,
                'body':body,
                'year':year,
                'img_url':img_lst[0],
                }
    except:
        context = {'products':data_lst, 
                'make':make,
                'market':market,
                'model':model,
                'body':body,
                'year':year,
                'img_url':'None',
                }
                
    
    return render(request, 'website/shop-table.html',context)


def checkout(request):

    if request.method == 'POST':
        selected_payment_method = request.POST.get('pay')


    if selected_payment_method == 'bank':
        payment_method = 'bank'
        bd_obj = Bank_details.objects.all()
        bd_obj = bd_obj[0]

    elif selected_payment_method == 'zelle':
        payment_method = 'zelle'
        bd_obj = zelle_details.objects.all()
        bd_obj = bd_obj[0]

    ob = addtocart.objects.filter(user_id=request.user.id)
    print(ob)

    lst=[]
    sign_no = []

    for o in range(len(ob)):
        subtotal = 0
        lst1=[]
        sign_no.append(o+1)
        print("ss",ob[0].coin_ids.all())
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            print("mustafa",float(obj1.price_per_pack))
            subtotal += float(obj1.price_per_pack)
            lst1.append(obj1)
            lst.append(lst1)

            # for product in obj1:
            #     subtotal += product.price_per_pack

            

    all_data = zip(sign_no,lst)
    context = {'all_data':all_data,
               'subtotal':subtotal,
               'bank_obj':bd_obj,
               'payment_method':payment_method}

    return render(request, 'website/checkout.html', context)



@login_required(login_url='login_view')
def my_order(request):
    
    ob = order.objects.filter(user_id=request.user.id)
    print('my order',ob)

    lst=[]
    sign_no = []
    subtotal_lst =[]

    for o in range(len(ob)):
        subtotal = 0
        lst1=[]
        sign_no.append(o+1)
        print("ss",ob[0].coin_ids.all(), ob[o].confirmation_no)
        lst.append(ob)
        
        for i in ob[o].coin_ids.all():
            obj1 = ProductData.objects.get(id=i.id)
            print("mustafa",float(obj1.price_per_pack))
            subtotal += float(obj1.price_per_pack)

            # lst1.append(obj1)
            # lst.append(lst1)
        subtotal_lst.append(subtotal)
            # for product in obj1:
            #     subtotal += product.price_per_pack

            
    product = ob
    all_data = zip(sign_no,product,subtotal_lst)
    context = {
                'all_data':all_data,
            #    'subtotal':subtotal,
               }
    return render(request,'website/order_list.html', context)



def order_approval(request,pk):

    obj = order.objects.get(id=pk)
    obj.status = "Approved"
    obj.save()
    messages.success(request, 'The order is approved successfully')
    return redirect("/all_orders") 

def order_disapproval(request,pk):

    obj = order.objects.get(id=pk)
    obj.status = "Pending"
    obj.save()
    messages.success(request, 'The order status is changed to pending')
    return redirect("/all_orders") 


def all_orders(request):
    order_obj = order.objects.all()
    subtotal_lst = []


    for ord in order_obj:
        subtotal = 0
        # print(ord.coin_ids.all())

        for obj in ord.coin_ids.all():
            # print('cycle')
            # print(obj.price_per_pack)
            subtotal += float(obj.price_per_pack)

        subtotal_lst.append(subtotal)

    print(subtotal_lst)
    all_data = zip(order_obj,subtotal_lst)
    context = {
        'all_data':all_data
    }
    return render(request,'website/all_order.html',context)


def order_detail(request,pk):
    obj = order.objects.get(id=pk)
    user_obj = User.objects.get(id=obj.user_id)
    # print(user_obj.username)

    product_lst = []
    subtotal = 0
    for product in obj.coin_ids.all():

        product_lst.append(product)
        subtotal += float(product.price_per_pack)


    context={
        'obj':obj,
        'product_lst':product_lst,
        'subtotal':subtotal,
        'user_obj':user_obj,
    }
    return render(request,'website/order-details.html',context)