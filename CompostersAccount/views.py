import json
from django.shortcuts import render, redirect
from .forms import ComposterForm, ComposterLoginForm
from .models import Composter
from GreenersAccount.models import Greener, GreenerNotifications
from django.contrib import messages
from CompostItem.models import CompostOffer
from django.http import JsonResponse
from django.db.models import Sum,Min,Max
from django.views.decorators.csrf import csrf_exempt

#libraries for auth
from django.contrib.auth.hashers import make_password
from .backends import ComposterAuthBackend
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def composterSignup(request):
    if request.method == 'POST':
        form = ComposterForm(request.POST)
        if form.is_valid():
            # do something with the cleaned form data
            organization_name = form.cleaned_data['OrganizationName']
            community_name = form.cleaned_data['CommunityName']
            email = form.cleaned_data['Email']
            password = make_password(form.cleaned_data['password'])
            phone_number = form.cleaned_data['PhoneNumber']
            location = form.cleaned_data['Location']
            composter = Composter.objects.create(OrganizationName=organization_name, CommunityName=community_name, Email=email, password=password, PhoneNumber=phone_number, Location=location)
            composter.save()
            

            return redirect('/')  
    else:
        form = ComposterForm()

    return render(request, 'Composter_signup.html', {'form': form})


def composterLogin(request):
    if request.user.is_authenticated and isinstance(request.user, Composter):
        return redirect('composterHome')
    if request.method == 'POST':
        form = ComposterLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, email=email, password=password, backend=ComposterAuthBackend())

            if user is not None:
                if isinstance(user, Greener):
                    messages.error(request, 'Invalid email or password.')
                else:
                    login(request, user)
                    return redirect('composterHome')
            else:
                # Authentication failed, show an error message
                messages.error(request, 'Invalid email or password.')
    else:
        form = ComposterLoginForm()

    return render(request, 'Composter_login.html', {'form': form})



@login_required
def composterHome(request):
    if request.user.is_authenticated:
        return render(request, 'Composter_home.html')
    else:
        return redirect('composterHome')


@login_required
def GreenersOffers(request):
    offers = CompostOffer.objects.filter(Greener__composter=request.user, Status='pending').select_related('Greener').values('Greener_id', 'Greener__FirstName', 'Greener__LastName', 'Greener__Location').annotate(
        AnimalManureQuantities=Sum('AnimalManureQuantity'),
        PlantFertilizersQuantities=Sum('PlantFertilizersQuantity'),
        BiodegradableFertilizersQuantities=Sum('BiodegradableFertilizersQuantity'),
        start_date=Max('StartDate'),
        end_date=Min('EndDate')
    ).order_by('Greener_id')

    GreenersOffersJson = []
    for offer in offers:
        GreenersOffersJson.append({
            'GreenerId': offer['Greener_id'],  
            'GreenerFirstName' : offer['Greener__FirstName'],
            'GreenerLastName': offer['Greener__LastName'],
            'GreenerLocationX': offer['Greener__Location'].x,
            'GreenerLocationY': offer['Greener__Location'].y,
            'AnimalManureQuantity': offer['AnimalManureQuantities'],  
            'PlantFertilizersQuantity': offer['PlantFertilizersQuantities'],
            'BiodegradableFertilizersQuantity': offer['BiodegradableFertilizersQuantities'],
            'StartDate': offer['start_date'],
            'EndDate': offer['end_date']
        }) 
    return JsonResponse({'GreenersOffersJson': GreenersOffersJson})

@login_required
def getPendingMembres(request):
    greeners = Greener.objects.filter(composter__id=request.user.id, ComposterStatus='waiting')
    context = {'greenersArray': greeners}
    return render(request, 'pending_membres.html', context)

@csrf_exempt
@login_required
def acceptGreener(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        greener_id = data.get('greenerId')
        if greener_id is not None:
            greener = Greener.objects.get(id=greener_id, composter__id=request.user.id, ComposterStatus='waiting')
            greener.ComposterStatus = 'accepted'
            greener.save()
            notification_message = "Congratulations! You have been accepted to "+ request.user.CommunityName +"community."
            GreenerNotifications.objects.create(greener=greener, Message=notification_message, IsRead = False)

            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def rejectGreener(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        greener_id = data.get('greenerId')
        if greener_id is not None:
            greener = Greener.objects.get(id=greener_id, composter__id=request.user.id, ComposterStatus='waiting')
            greener.composter = None
            greener.save()
            notification_message = "Unfortunately, your request to Community: " + request.user.CommunityName + "has been rejected !"
            GreenerNotifications.objects.create(greener=greener, Message=notification_message, IsRead = False)
            
            return JsonResponse({'status':'ok'})
    return JsonResponse({'status': 'error'})






@login_required
def getGreenersOffer(request):
    offers = CompostOffer.objects.filter(Greener__composter=request.user)
    offersArray = []
    for offer in offers:
        offersArray.append({
            'offerid' : offer.id,
            'Greener': offer.Greener,  
            'AnimalManureQuantity': offer.AnimalManureQuantity,  
            'PlantFertilizersQuantity': offer.PlantFertilizersQuantity,
            'BiodegradableFertilizersQuantity': offer.BiodegradableFertilizersQuantity,
            'StartDate': offer.StartDate,
            'EndDate': offer.EndDate,
            'Status': offer.Status
        }) 
    return render(request , 'greeners_request.html',{'offersArray': offersArray})



@login_required
def getComposterMembers(request):
    membres = Greener.objects.filter(composter__id = request.user.id)
    context = {'membresArray' : membres}
    return render(request, 'Composter_membres.html', context)

def logoff(request):
    logout(request)
    return redirect('index')