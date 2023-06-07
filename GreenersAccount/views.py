import datetime
import json
from django.shortcuts import render, redirect
from .forms import GreenerForm, GreenerLoginForm
from .models import Greener, GreenerNotifications
from CompostersAccount.models import Composter
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from CompostersAccount.models import Composter
from django.contrib.gis.geos import GEOSGeometry
from CompostItem.models import Compost, CompostOffer
from CompostItem.forms import CompostOfferForm
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

#libraries for auth
from django.contrib.auth.hashers import make_password
from .backends import GreenerAuthBackend
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



# Create your views here.

def greenerSignup(request):
    #Greener to singup
    if request.method == 'POST':
        form = GreenerForm(request.POST)
        #check if form is valid
        if form.is_valid():
        #give each variable a value from the form inputs
            first_name = form.cleaned_data['FirstName']
            last_name = form.cleaned_data['LastName']
            email = form.cleaned_data['Email']
            #hashing password and assigning it a variable
            password = make_password(form.cleaned_data['password'])
            phone_number = form.cleaned_data['PhoneNumber']
            location = form.cleaned_data['Location']

            composterObject = form.cleaned_data['composter']    
            #creat the object in the database       
            greener = Greener.objects.create(FirstName=first_name, LastName=last_name, Email=email, password=password, PhoneNumber=phone_number, Location = location, composter = composterObject)
            greener.save()
            return redirect('/') 
    else:
        form = GreenerForm()

    return render(request,'Greener_signup.html',{'form': form})

#----------------------------------------------------------------------#

def greenerLogin(request):
    if request.method == 'POST':
        form = GreenerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate the user using my custom backend
            user = authenticate(request=request, email=email, password=password, backend=GreenerAuthBackend())

            if user is not None:
                if isinstance(user, Composter):
                    # Reject the login attempt if the user is a Greener
                    messages.error(request, 'Invalid email or password.')
                else:
                    # Authenticate the user and redirect to the home page
                    login(request, user)
                    if request.user.ComposterStatus == 'waiting':
                        return redirect('greenerHomeChooseComposter')
                    else:
                        return redirect('greenerHome')
            else:
                # Authentication failed, show an error message
                messages.error(request, 'Invalid email or password.')
    else:
        form = GreenerLoginForm()

    return render(request, 'Greener_login.html', {'form': form} )

#-----------------------------------------------------------------------#

#function to take greener to composter pick up page 
@login_required
def greenerHomeChooseComposter(request):
    if request.user.ComposterStatus == 'accepted':
        return redirect('greenerHome')
    else:
        return render(request, 'Greener_home_choose_composter.html')



@login_required
def greenerRequestComposterLink(request):
    context = {'user' : request.user}
    if request.user.ComposterStatus == 'accepted':
        return redirect('greenerHome')
    else:
        return render(request, 'Greener_request_composter_link.html', context)
    


@login_required
def updateComposter(request):
    if request.method == 'POST':
        #load the post request
        data = json.loads(request.body)
        print(data)
        greener_id = data.get('greenerId')
        composter_id = data.get('composterId')
        if composter_id is not None:
            #return a composter object from a given id
            composter = Composter.objects.get(id=composter_id)
            #return a greener object from a given id
            greener = Greener.objects.get(id=greener_id)
            #update the greener composter and assign for it new composter
            greener.composter = composter
            greener.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})




@login_required
def greenerHome(request):
    return render(request, 'Greener_home.html')

@login_required
def greenerNotification(request):
    notifications = GreenerNotifications.objects.filter(greener__id=request.user.id, IsRead=False).order_by('-Timestamp')
    context = {'notificationsArray': notifications}

    return render(request, 'Greener_notification.html', context)




#----------------------------API during signup for picking up the closest compster-------------------------------------------#

def getClosestComposters(request):
    UserLocationWKT = request.GET.get('UserLocation')
    UserLocationWKB = GEOSGeometry(UserLocationWKT)
    point = Point(UserLocationWKB.x, UserLocationWKB.y, srid=4326)
    radius = request.GET.get('Radius', 10000)
    radius = float(radius)*1000
    composters = Composter.objects.filter(Location__distance_lte=(point, radius)).annotate(distance=Distance('Location', point)).order_by('distance')

    closest_composters = []
    for composter in composters:
        closest_composters.append({
            'id': composter.id,
            'OrganizationName': composter.OrganizationName,
            'CommunityName': composter.CommunityName,
            'Email': composter.Email,
            'PhoneNumber': composter.PhoneNumber,
            'distance': composter.distance.m,
            'LocationX': str(composter.Location.x),
            'LocationY': str(composter.Location.y)
        })

    return JsonResponse({'closest_composters': closest_composters})

def checkEmail(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        print(email)

        # Check if email exists in the Greener table
        exists = Greener.objects.filter(Email=email).exists()
        print(exists)

        return JsonResponse({'exists': exists})





@login_required
def compostOffer(request):
    composts = Compost.objects.all()
    context = {'composts': composts}
    if request.method == 'POST':
        form = CompostOfferForm(request.POST)
        if form.is_valid():
            manure_quantity = form.cleaned_data.get('animal_mature_quantities')
            plant_based_fertilizers_quantities  = form.cleaned_data.get('plant_based_fertilizers_quantities')
            biodegradable_fertilizers_quantities =  form.cleaned_data.get('biodegradable_fertilizers_quantities') 
            date_range = form.cleaned_data.get('date_range')
            date_start = datetime.strptime(date_range.split('to')[0].strip(), '%Y-%m-%d').date()
            date_end = datetime.strptime(date_range.split('to')[1].strip(), '%Y-%m-%d').date()
            greener = request.user
            offer = CompostOffer.objects.create(AnimalManureQuantity = manure_quantity, PlantFertilizersQuantity = plant_based_fertilizers_quantities, BiodegradableFertilizersQuantity = biodegradable_fertilizers_quantities,
                                                StartDate = date_start, EndDate = date_end, Greener = greener)
            offer.save()
            
            return redirect('greenerHome')

    else:
        form = CompostOfferForm()
        context['form'] = form
    return render(request, 'Compost_offer.html', context)


def logoff(request):
    logout(request)
    return redirect('index')