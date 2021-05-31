from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import random
from django.db.models import Max

def index(request):
    if "user_id" in request.session :
        return redirect("/order/add")
    return render(request, "login.html")
def register(request):
    errors=User.objects.basic_validator(request.POST)
    if request.method == "GET":
        return redirect('/')
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        messages.success(request, "You have successfully registered!")
        return redirect('/')
def login(request):
    if not User.objects.authenticate(request.POST['email'], request.POST['password2']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    # request.session['user'] = user
    messages.success(request, "You have successfully logged in!")
    return redirect('/home')
def orderadd(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    method=Order.method_choices
    context = {
        'user': user,
        'method':method,

    }
    return render(request, 'orderadd.html', context)

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    last=user.favorites.last()
    context = {
        'user': user,
        'last':last,

    }
    return render(request, 'home.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
def createorder(request):
    if request.method == "GET":
        return redirect('/')
    else:
        costype = [{"name": "VEGETERIAN", "cost":2}, {"name": "PEPPERONI", "cost":4}, {"name": "MARGHERITA", "cost":3},{"name": "BARBEQUE", "cost":2},{"name": "HAWAIIAN", "cost":1},{"name": "BUFFALO", "cost":2},{"name": "SUPREME", "cost":3}]
        
        for key  in costype:
            if key["name"]==request.POST['item']:
                costs=int(key["cost"])
                
        costsize= [{"name": "LARGE", "cost":2}, {"name": "MEDIUM", "cost":1}, {"name": "SMALL", "cost":1}]
        
        for key  in costsize:
            if key["name"]==request.POST['size']:
                costsize=0
                costssize=int(key["cost"])
        
        if request.POST['method']=="Delivery":
            delivery_fee=2
        else :
            delivery_fee=0
                
        qty2=int(request.POST['qty'])
        # print(qty2)
        pizzacosts=(costs+costssize)*qty2
        # print(costssize)
        # print(cost)
        # print(pizzacosts)
        messages.success(request, "You have successfully registered!")
        user = User.objects.get(id=request.session['user_id'])

        order=Order.objects.create(user=user,method=request.POST['method'],qty=qty2,price=pizzacosts,delivery_fee=int(delivery_fee))
        pizza=Pizza.objects.create(types=request.POST['item'],order=order,size=request.POST['size'],crust=request.POST['crust'])
        
        
        
        return redirect('/purchase/'+str(order.id))
def purchase(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    order = Order.objects.get(id=id)
    extrafee= (int(order.price) + int(order.delivery_fee))*0.2
    total= int(order.price) + int(order.delivery_fee) + extrafee
    context = {
        'user': user,
        'order': order,
        'extrafee':extrafee,
        'total':total
    }
    return render(request, 'purchase.html', context)   

def edit(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    ids = []
    for i in user.favorites.all():
        ids.append(i.id)
    orders=Order.objects.filter(user=user)
    nonfavorites = orders.exclude(id__in=ids)
    context = {
        'user': user,
        'nonfavorites':nonfavorites
    }
    return render(request, 'userupdate.html', context)   
    


def update(request):
    user = User.objects.get(id=request.session['user_id'])
    errors = User.objects.updateuser_validator(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/user/edit')
    else:
        user = User.objects.get(id=request.session['user_id'])
        user.first_name=(request.POST['name2'])
        user.last_name=(request.POST['lastname2'])
        user.city=(request.POST['city2'])
        user.state=(request.POST['state2'])
        user.email=(request.POST['email2'])
        user.adress=(request.POST['adress2'])
        user.save()
    return redirect('/user/edit')
def addfavorite(request,id):
    user = User.objects.get(id=request.session['user_id'])
    order=Order.objects.get(id=id)
    user.favorites.add(order)
    return redirect('/user/edit')
def removefavorite(request,id):
    user = User.objects.get(id=request.session['user_id'])
    order=Order.objects.get(id=id)
    user.favorites.remove(order)
    return redirect('/user/edit')
def deletefavorite(request,id):
    user = User.objects.get(id=request.session['user_id'])
    order=Order.objects.get(id=id)
    order.delete()
    return redirect('/user/edit')

def createRandom(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    random_fav_pizza = random.choice(user.orders.all())
    order = Order.objects.create(user=user,method=random_fav_pizza.method,qty=random_fav_pizza.qty, price= random_fav_pizza.price, delivery_fee=int(random_fav_pizza.delivery_fee))
    pizza=Pizza.objects.create(types=random_fav_pizza.pizza.types,order=order,size=random_fav_pizza.pizza.size,crust=random_fav_pizza.pizza.crust)
    return redirect('/purchase/'+str(order.id))


