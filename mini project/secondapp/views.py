from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, get_object_or_404,reverse,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from secondapp.models import Contact_us, Category, User, register_table, add_product, Cart,Order,Wallet
from django.contrib.auth.models import User
from secondapp.forms import add_product_form,UpdateOrderStatusForm


def index(request):
    cats = Category.objects.all()
    items=add_product.objects.all()
    chefs = register_table.objects.filter(user__id=request.user.id)

    return render(request,"first.html",{"category":cats,"item":items})
def user_login(request):
    if request.method=="POST":
        un=request.POST["username"]
        pwd=request.POST["password"]
        user=authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                return HttpResponseRedirect("/cust_dashboard")
            #if user.is_active:
             #   return HttpResponseRedirect("/cust_dashboard")

        #else:
            #return render(request,"home.html",{"status":"Invalid Username or Password"})
    return render(request,"login.html")

@login_required
def cust_dashboard(request):
    context={}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check) > 0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"cust_dashboard.html")
@login_required
def chef_dashboard(request):
    return render(request,"chef_dashboard.html")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def edit_profile(request):
    context={}
    check=register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data=register_table.objects.get(user__id=request.user.id)
        context["data"]=data
    if request.method=="POST":
        print(request.POST)
        fn=request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        con = request.POST["contact"]
        ct = request.POST["city"]
        gen = request.POST["gender"]
        abt = request.POST["about"]

        usr=User.objects.get(id=request.user.id)
        usr.first_name=fn
        usr.last_name=ln
        usr.email=em
        usr.save()

        data.contact_number=con
        data.city=ct
        data.gender=gen
        data.about=abt
        data.save()
        if "image" in request.FILES:
            img=request.FILES["image"]
            data.profile_pic=img
            data.save()


        context["status"]="Changes Saved Successfully"
    return render(request,"edit_profile.html",context)




def home(request):
    recent= Contact_us.objects.all()[:6]

    return render(request,"home.html",{"messages":recent})
def about(request):

    return render(request,"about.html")
def contact(request):
    all_data = Contact_us.objects.all().order_by("-id")

    if request.method=="POST":
        name=request.POST["name"]
        con=request.POST["contact"]
        sub=request.POST["subject"]
        ms=request.POST["msg"]
        data=Contact_us(name=name,contact_no=con,subject=sub,message=ms)
        data.save()
        res="Dear {} Thanks for your Feddback".format(name)
        return render(request,"contact.html",{"status":res,"messages":all_data})
       # return HttpResponse("<h1 style='color:blue;'>Dear {} Data saved Sucessfully</h1>".format(name))
    return render(request,"contact.html",{"messages":all_data})

def register(request):
    if request.method=="POST":
        fname=request.POST["first"]
        lname=request.POST["last"]
        un=request.POST["username"]
        pwd=request.POST["password"]
        em=request.POST["email"]
        con=request.POST["contactno"]
        tp=request.POST["utype"]
        usr=User.objects.create_user(un,em,pwd)
        usr.first_name=fname
        usr.last_name=lname
        if tp=="chef":
            usr.is_staff=True
        usr.save()
        reg=register_table(user=usr,contact_number=con)
        reg.save()
        return render(request,"register.html",{"status":"Mr/Miss. {} your Account Created Successfully".format(fname)})
    return render(request,"register.html")
def check_user(request):
    if request.method=="GET":
        un=request.GET["usern"]
        check=User.objects.filter(username=un)
        if len(check)== 1:
            return HttpResponse("Exits")
        else:
            return HttpResponse("Not Exists")

def change_password(request):
    context={}
    ch=register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data=register_table.objects.get(user__id=request.user.id)
        context["data"]=data
    if request.method=="POST":
        current=request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user=User.objects.get(id=request.user.id)
        un=user.username
        check=user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully"
            context["col"] = "alert-success"
            user=User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"]="Incorrect Current Password"
            context["col"]="alert-danger"

    return render(request,"change_password.html",context)

def add_item_view(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch) > 0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data
    form=add_product_form()
    if request.method=="POST":
        form=add_product_form(request.POST,request.FILES)
        if form.is_valid():
            data=form.save(commit=False)

            login_user=User.objects.get(username=request.user.username)
            data.item_chef=login_user

            data.save()
            context["status"]="{} Added Successfully".format(data.item_name)
    context["form"]=form
    return render(request,"addproduct.html",context)

def my_products(request):
    context={}
    all=add_product.objects.filter(item_chef__id=request.user.id)
    context["products"]=all
    return render(request,"myproducts.html",context)

def viewitem(request):
    context = {}
    all = add_product.objects.filter(item_chef__id=request.user.id,item_name__id=request.item_name)
    context["products"] = all
    return render(request, "viewitem.html",context)

def single_product(request):
    context = {}
    pid=request.GET["pid"]
    obj=add_product.objects.get(id=id)
    context["product"]=obj
    return render(request,"single_product.html",context)

def update_product(request):
    context={}
    cats = Category.objects.all()
    context["category"]=cats

    pid = request.GET["pid"]
    product=add_product.objects.get(id=pid)
    context["product"]=product

    if request.method=="POST":
        un=request.POST["pname"]
        ct_id = request.POST["pcat"]
        pr = request.POST["pp"]
        des= request.POST["des"]

        cat_obj=Category.objects.get(id=ct_id)

        product.item_name=un
        product.item_category=cat_obj
        product.item_price = pr
        product.item_details = des
        if "pimg" in request.FILES:
            img=request.FILES["pimg"]
            product.item_image=img
        product.save()
        context["status"]="Changes saved successfully"
        context["id"]=pid
    return render(request,"update_product.html",context)

def delete_product(request):
    context={}
    if "pid" in request.GET:
        pid=request.GET["pid"]
        prd=get_object_or_404(add_product,id=pid)
        context["product"]=prd

        if "action" in request.GET:
            prd.delete()
            context["status"]=str(prd.item_name)+ "Deleted Successfully!!!"
    return render(request,"deleteproduct.html",context)

def all_products(request):
    context={}
    all_products=add_product.objects.all().order_by("item_name")
    context["products"] =all_products
    if "qry" in request.GET:
        q=request.GET["qry"]
        prd=add_product.objects.filter(item_name__contains=q)
        context["products"]=prd
        context["abcd"]="search"
    if "cat" in request.GET:
        cid=request.GET["cat"]
        prd=add_product.objects.filter(item_category__id=cid)
        context["products"] = prd
        context["abcd"] = "search"
    return render(request,"allproducts.html",context)

from django.db.models import Q

def search_chefs(request):
    location = request.GET.get('location')

    if location:
        chefs = register_table.objects.filter(
            Q(city__icontains=location) & Q(user__is_staff=True)
        )
    else:
        chefs = register_table.objects.filter(user__is_staff=True)

    return render(request, 'search_chefs.html', {'chefs': chefs, 'location': location})

from django.utils import timezone

def add_to_cart(request):
    context = {}
    items = Cart.objects.filter(user__id=request.user.id, status=False)
    context["items"] = items

    if request.user.is_authenticated:
        if request.method == "POST":
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            is_exist = Cart.objects.filter(product__id=pid, user__id=request.user.id, status=False)

            if len(is_exist) > 0:
                context["msz"] = "Item Already Exists in Your Cart"
                context["cls"] = "alert alert-warning"
            else:
                product = get_object_or_404(add_product, id=pid)
                usr = get_object_or_404(User, id=request.user.id)
                c = Cart(user=usr, product=product, quantity=qty)
                c.save()

                # Create and save an Order object
                order = Order(
                    cust_id=request.user,
                    cart_ids=','.join(str(item.id) for item in items),
                    processed_on=timezone.now(),
                    order_status='Pending',
                )
                order.save()

                context["msz"] = "{} Added in Your Cart".format(product.item_name)
                context["cls"] = "alert alert-success"
    else:
        context["status"] = "Please Login First to View Your Cart"
    return render(request, "cart.html", context)


def get_cart_data(request):
    items = Cart.objects.filter(user__id=request.user.id, status=False)
    total,quantity =0,0,
    for i in items:

        total += float(i.product.item_price)*i.quantity
        quantity+= int(i.quantity)

    res = {
        "total":total,"quan":quantity,
    }
    return JsonResponse(res)

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(Cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(Cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)

def view_wallet(request):
    user_wallet = Wallet.objects.get(user=request.user)
    return render(request, "view_wallet.html", {"wallet": user_wallet})

def add_money(request):
    if request.method == "POST":
        amount = float(request.POST["amount"])
        user_wallet = Wallet.objects.get(user=request.user)
        user_wallet.balance += amount
        user_wallet.save()
        return HttpResponseRedirect("/view_wallet")
    return render(request, "add_money.html")

# views.py
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = UpdateOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('chef_orders')
    else:
        form = UpdateOrderStatusForm(instance=order)

    return render(request, 'update_order_status.html', {'form': form, 'order': order})


# views.py
#from .models import Order

#from .models import Cart
#from django.shortcuts import render, redirect, get_object_or_404
#from .models import Order, cart
#from .forms import UpdateOrderStatusForm  # Import your form

# ...

def proceed_to_pay(request):
    user_wallet = Wallet.objects.get(user=request.user)
    user_cart = Cart.objects.filter(user=request.user, status=False)

    # Calculate the total amount in the cart
    total_amount = sum(item.product.item_price * item.quantity for item in user_cart)

    # Check if the user has enough balance in the wallet
    if user_wallet.balance >= total_amount:
        # Create a new order
        new_order = Order.objects.create(
            cust_id=request.user,
            chef=user_cart.first().product.item_chef,  # You may need to adjust this based on your model structure
            status=False,  # You might want to set the status based on your logic
        )

        # Update the status of items in the cart and associate them with the order
        for item in user_cart:
            item.status = True
            item.order = new_order
            item.save()

        # Deduct the amount from the user's wallet
        user_wallet.balance -= total_amount
        user_wallet.save()

        return render(request, "payment_success.html", {"amount": total_amount})

    return render(request, "payment_failure.html", {"amount": total_amount})





# views.py


# views.py

#from django.shortcuts import render
#from .models import Order, cart


def order_history(request):
    # Get the orders associated with the logged-in user
    user_orders = Order.objects.filter(cust_id=request.user).order_by('-processed_on')

    # Retrieve detailed information about each order
    order_details = []
    for order in user_orders:
        # Remove empty strings from cart_ids and convert remaining values to integers
        cart_ids = [int(cart_id) for cart_id in order.cart_ids.split(',') if cart_id]

        # Filter cart objects using the cleaned cart_ids
        cart_items = Cart.objects.filter(id__in=cart_ids)

        order_details.append({
            'order': order,
            'items': cart_items,
        })

    return render(request, 'order_history.html', {'order_details': order_details})


#from django.shortcuts import render
#from .models import Order



def chef_orders(request):
    chef = request.user
    orders = Order.objects.filter(chef=chef).prefetch_related('items__product')


    return render(request, 'chef_orders.html', {'orders': orders})



def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.order_status = new_status
        order.save()
        return redirect('chef_orders')
    return render(request, 'update_order_status.html', {'order': order})


def enter_delivery_address(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        location = request.POST.get('delivery_address')

        # Update the order's location
        order.delivery_address = location
        order.save()

        # Redirect to the cart page or any other appropriate page
        return redirect('cart')  # Update 'cart' to the actual URL name or path

    # Handle GET requests if needed
    return render(request, 'cart.html', {'order_id': order_id})

# views.py



def all_chefs(request):
    chefs = register_table.objects.filter(user__is_staff=True)
    return render(request, 'all_chefs.html', {'chefs': chefs})
