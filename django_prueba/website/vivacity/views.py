from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth.models import User, auth
from .models import Destination
from .models import Detailed_desc
from .models import pessanger_detail
from .models import Cards
from .models import Transactions
from .models import NetBanking
from datetime import datetime
from django.shortcuts import render, redirect
from django.forms.formsets import formset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime
from .models import pessanger_detail
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Library
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
import random
from django.conf import settings

from .models import Destination, Detailed_desc

def show_destinations(request):
    destinations = Destination.objects.all()
    detailed_descs = Detailed_desc.objects.all()
    return render(request, 'vivacity/tu_template.html', {'destinations': destinations, 'detailed_descs': detailed_descs})

def mostrar_destinos(request):
    dests = Destination.objects.all()
    return render(request, 'vivacity/vista.html', {'dests': dests})


def home(request):
    return render(request, 'vivacity/index.html') 

def travel(request):
    return render(request, 'vivacity/travel_destination.html') 

def vista(request):
    destinations = Destination.objects.all()
    detailed_descs = Detailed_desc.objects.all()
    return render(request, 'vivacity/vista.html', {'destinations': destinations, 'detailed_descs': detailed_descs})

def list_view(request):
    return render(request, 'vivacity/list.html')

def place_view(request):
    return render(request, 'vivacity/place.html')

def login_user(request):
    if request.method == "POST": 
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Utiliza get en lugar de ['key'] para evitar posibles KeyError
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            
            # Usar request.user.username en lugar de request.session
            request.session['user_logged_in'] = True
            request.session['username'] = request.user.username
            
            # Redirigir a una URL segura después del inicio de sesión
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')
    else:
        return render(request, 'vivacity/login.html')
    
def logout_user(request):
    logout(request)
    return redirect('home')


def registro(request):
    if request.method == "POST": 
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'vivacity/registro.html', {'form':form,})

def search(request):
    try:
        place1 = request.session.get('place')
        print(place1)
        dest = Detailed_desc.objects.get(dest_name=place1)
        print(place1)
        return render(request, 'vivacity/list.html', {'dest': dest})
    except:
        messages.info(request, 'Place not found')
        return redirect('home')

def destination_list(request, country):
    dests = Detailed_desc.objects.all().filter(country=country)
    return render(request, 'vivacity/travel_destination.html', {'dests': dests})

def destination_details(request,city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request,'vivacity/destination_details.html',{'dest':dest})

def vista_destination_details(request, city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request, 'vivacity/destination_details.html', {'dest': dest})

class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()

def pessanger_detail_def(request, city_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)

    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()

            if temp_date < date1:
                return redirect('home')

            try:
                obj = pessanger_detail.objects.get(Trip_id=3)
            except pessanger_detail.DoesNotExist:
                # Manejamos el caso cuando el objeto no existe
                obj = pessanger_detail(Trip_id=3, Trip_date=temp_date)
                obj.save()

            pipo_id = obj.Trip_same_id
            request.session['Trip_same_id'] = pipo_id
            price = request.session['price']
            city = request.session['city']

            usernameget = request.user.get_username()
            request.session['n'] = formset.total_form_count()

            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]

                t = pessanger_detail(
                    Trip_same_id=pipo_id,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    age=form.cleaned_data['age'],
                    Trip_date=temp_date,
                    payment=price,
                    username=usernameget,
                    city=city
                )
                t.save()

            obj.Trip_same_id = (pipo_id + 1)
            obj.save()

            no_of_person = formset.total_form_count()
            price1 = no_of_person * price
            GST = price1 * 0.18
            GST = float("{:.2f}".format(GST))
            final_total = GST + price1
            request.session['pay_amount'] = final_total

            return render(request, 'vivacity/payment.html', {
    'no_of_person': no_of_person,
    'price1': price1,
    'GST': GST,
    'final_total': final_total,
    'city': city,
    'city_name': city_name,  # Asegúrate de agregar esto
})
    else:
        formset = KeyValueFormSet()

    return render(request, 'vivacity/sample.html', {'formset': formset, 'city_name': city_name})


def handle_pessanger_detail_post(request, city_name):
    if request.method == 'POST':
        # Lógica para manejar la solicitud POST a pessanger_detail_def
        return HttpResponse("Solicitud POST manejada correctamente.")
    else:
        # Manejar otros métodos HTTP según sea necesario
        return HttpResponse("Método no permitido.")
    
def upcoming_trips(request):
    username = request.user.get_username()
    date1=datetime.now().date()
    person = pessanger_detail.objects.all().filter(username=username).filter(pay_done=1)
    person = person.filter(Trip_date__gte=date1)
    print(date1)
    return render(request,'vivacity/upcoming trip1.html',{'person':person})

def net_payment(request, city_name):
    username = request.POST['cardNumber']
    Password1 = request.POST['pass']
    Bank_name = request.POST['banks']
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Net Banking'
    try:
        r = NetBanking.objects.get(Username=username, Password=Password1,Bank=Bank_name)
        balance = r.Balance
        request.session['total_balance'] = balance
        if int(balance) >= int(request.session['pay_amount']):
            total_balance = int(request.session['total_balance'])
            rem_balance = int(total_balance - int(request.session["pay_amount"]))
            r.Balance = rem_balance
            r.save(update_fields=['Balance'])
            r.save()
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
            t.save()
            return render(request, 'vivacity/confirmetion_page.html')
        else:
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
            t.save()
            return render(request, 'vivacity/wrongdata.html')
    except :
        return render(request, 'vivacity/wrongdata.html')

def card_payment(request, city_name):
    if request.method == 'POST':
        # Simulación de una transacción exitosa con un valor aleatorio
        pay_amount = random.randint(100, 1000)  # Simulación de un monto aleatorio entre 100 y 1000
        Transactions.objects.create(
            username=request.user.get_username(),
            Trip_same_id=request.session.get('Trip_same_id', 0),
            Amount=pay_amount,
            Payment_method='Debit card',
            Status='Successfull'
        )

        # Marcar los pasajeros como pagados
        pessanger_detail.objects.filter(Trip_same_id=request.session.get('Trip_same_id', 0)).update(pay_done=1)

        # Redirigir a la página de confirmación
        return render(request, 'vivacity/confirmetion_page.html')
    else:
        # Si no es una solicitud POST, redirigir a la página de inicio
        return redirect('home')



def otp_verification(request):
    otp1 = int(request.POST['otp'])
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Debit card'
    if otp1 == int(request.session['OTP']):
        del request.session["OTP"]
        total_balance = int(request.session['total_balance'])
        rem_balance = int(total_balance-int(request.session["pay_amount"]))
        c = Cards.objects.get(Card_number=request.session['dcard'])
        c.Balance = rem_balance
        c.save(update_fields=['Balance'])
        c.save()
        t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
        t.save()
        z = pessanger_detail.objects.all().filter(Trip_same_id=Trip_same_id1)
        for obj in z:
            obj.pay_done = 1
            obj.save(update_fields=['pay_done'])
            obj.save()
            print(obj.pay_done)
        return render(request, 'vivacity/confirmetion_page.html')
    else:
        t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
        t.save()
        return render(request, 'vivacity/wrong_OTP.html')


def data_fetch(request):
    username = request.user.get_username()
    person = pessanger_detail.objects.all().filter(username=username)

def render_template(request, template_name, context=None):
    context = context or {}
    return render(request, template_name, context)
