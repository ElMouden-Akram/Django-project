from django.shortcuts import render , redirect
# from .forms import ClientRegistrationForm , AdminstrateurRegistrationForm , ClientSettingsForm , VoyageForm , categorieForm , hotelForm , volForm , notificationForm
from .forms import ClientRegistrationForm , AdminstrateurRegistrationForm , ClientSettingsForm , VoyageForm , categorieForm , hotelForm , volForm , notificationForm , promotionForm , commentaireForm
from django.contrib.auth import authenticate , login , logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .decorators import user_authenticated , allowed_users
from .models import Voyage , Categorie , Client_voyage ,Hotel , Vol , Client , Adminstrateur , Client , Notification , Promotion , Commentaire
from django.http import HttpResponse
import stripe
from datetime import date
from .filters import VoyageFilter

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

stripe.api_key = "sk_test_51MxJ30AhdCO5CiRyKgfCeJhC1y2i1iXTiUBS9YpKaQYtSp5ZmMpJ2Y8yIRtQUMzmvJHZtCIt0xkYmBO7NslpAqkx00PZKLjYrT"

# 👇for testing purpose :
def test2(request) : 
  context = {}
  return render(request,"app1/!login-register.html" , context)

def home(request) : 
    commentaires = Commentaire.objects.all()
    categories = Categorie.objects.all()
    # print(categories)
    voyages = Voyage.objects.all()
    myfilter = VoyageFilter(request.GET,queryset=voyages)
    # voyages=myfilter.qs
    context = {'voyages': voyages,'myfilter':myfilter,'categories':categories,'commentaires':commentaires}
    print("context : ",myfilter)
    # breakpoint()
    return render(request,"app1/home.html" , context)


def test(request) : 
    voyages = Voyage.objects.all()
    myfilter = VoyageFilter(request.GET,queryset=voyages)
    voyages=myfilter.qs
    context = {"voyages":voyages,"myfilter":myfilter}
    return render(request,"app1/testo.html" , context)

@user_authenticated  #makatkhlich user li loged in i3aawd irje3 l login page wla ay view kat7t fo9ha had decorator
def loginPage(request): #knt smitha login walakin ghatkhlet m3A login dyal django li kandiro biha login
  if request.method == 'POST':
      username = request.POST.get('username') #input smito usename f login.html
      password = request.POST.get('password') #input smito password f login.html
    #   breakpoint()
      user = authenticate(request, username=username, password=password) #kat9lb f database
      if user is not None:
          login(request, user)  #kan3tiwha objet user li rj3ato authenticate
          if user.groups.filter(name='admin').exists():
              return redirect('AdminPage')
          elif user.groups.filter(name='client').exists():
              return redirect('home')
          else:
              return HttpResponse('This user should be associated with a group')
      else:
          messages.info(request, 'Username or password is incorrect')

  context = {'form':ClientRegistrationForm()}
#   form = ClientRegistrationForm()
  return render(request, 'app1/login.html', context)

@user_authenticated 
def register(request): #

    if request.method == 'POST':
        # print("request.POST : ",request.POST)
        # breakpoint()
        form = ClientRegistrationForm(request.POST)
        print("form : ",form.is_valid())
        print("data : ",request.POST)
        # breakpoint()
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username') #to get user name from the form
            messages.success(request,'Account created for '+user)
            return redirect('login')
        else:
            print("not valid form")
            print(form.errors)
            # breakpoint()
            return redirect('./#!',{'form': form})
    else:
        form = ClientRegistrationForm()

    return render(request, 'app1/login.html', {'form': form})


@login_required(login_url='home') #ila makanch mconecti aymchi l home
@allowed_users(allowed_roles=['client']) #katkhli ghir clients homa li ydkhlo t9dr tbdl roles kima bghiti 3la 7sab groups 
def ClientPage(request): 
    user = request.user
    #for notifications :
    id_user = request.user.id
    client = get_object_or_404(Client, fk_user=id_user)
    notifications = Notification.objects.filter(client=client)[:3]
    #for reservations :
    reservations =Client_voyage.objects.filter(fk_client=client.id)[:3]
    
    context ={'user':user, 'notifications': notifications , 'reservations':reservations}
    return render(request , 'app1/ClientPage.html',context)



@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def AdminPage(request):      
    context ={}
    return render(request , 'app1/AdminPage.html',context)

def logoutUser(request):
  logout(request) #defauLt method dyal django
  return redirect('login')

@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def registerAdmin(request): #
    if request.method == 'POST':
        form = AdminstrateurRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AdminPage')
    else:
        form = AdminstrateurRegistrationForm()

    return render(request, 'app1/registerAdmin.html', {'form': form})

@login_required(login_url='home') 
@allowed_users(allowed_roles=['client'])
def ClientSettings(request) :  
  client = request.user.client
  form = ClientSettingsForm(instance=client)

  if request.method == 'POST':
      form = ClientSettingsForm(request.POST, request.FILES,instance=client)
      if form.is_valid():
        form.save()
  context={'form':form}
  return render(request,'app1/ClientSettings.html',context)

@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def voyages(request) : 
    voyages = Voyage.objects.all()
    context = {'voyages':voyages}
    return render(request,"app1/voyages.html" , context)

@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def createvoyage(request):
    if request.method == 'POST':
        form = VoyageForm(request.POST , request.FILES) #🔥🔥🔥🔥🔥request.FILES zdtha bach doz image tahia
        if form.is_valid():
            voyage = form.save(commit=False)
# Check if a promotion is selected
            if voyage.promotion:
                # Reduce the price based on the promotion percentage
                voyage.prix -= (voyage.prix * voyage.promotion.pourcentage_reduction) / 100

            voyage.save()            
            return redirect('voyages')  
        else : 
            print("form addvoyage fiha mochkil ")

    else:
        # If the request method is GET, render the form
        form = VoyageForm()

    context = {'form': form}
    return render(request, 'app1/addvoyage.html', context)

@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def updatevoyage(request, pk):
    voyage = Voyage.objects.get(id=pk)
    form = VoyageForm(instance=voyage)

    if request.method == 'POST':
        form = VoyageForm(request.POST, request.FILES, instance=voyage)
        if form.is_valid():
            voyage = form.save(commit=False)

            # Check if a promotion is selected
            if voyage.promotion:
                # Reduce the price based on the promotion percentage
                voyage.prix -= (voyage.prix * voyage.promotion.pourcentage_reduction) / 100

            voyage.save()
            return redirect('voyages')

    context = {'form': form}
    return render(request, "app1/addvoyage.html", context)

@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def deletevoyage(request , pk) : 
  item = Voyage.objects.get(id=pk)
  if request.method == "POST" :
    item.delete()
    return redirect('voyages')

  context={'item':item }
  return render(request , 'app1/deletevoyage.html' , context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def categories(request) : 
    categories = Categorie.objects.all()
    context = {'categories':categories}
    return render(request,"app1/categories.html" , context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def addcategorie(request):
    if request.method == 'POST':
        form = categorieForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            print("categorie tzadt")
            return redirect('categories')  
        else : 
            print("form addcategorie fiha mochkil ")
            #return redirect('addvoyage')

    else:
        # If the request method is GET, render the form
        form = categorieForm()

    context = {'form': form}
    return render(request, 'app1/addcategorie.html', context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def updatecategorie(request , pk):
  categorie = Categorie.objects.get(id=pk)
  form = categorieForm(instance=categorie)
  if request.method == 'POST' : 
      form = categorieForm(request.POST ,request.FILES,instance=categorie)
      if form.is_valid :
        form.save()
        return redirect('categories')
  context={'form' : form}
  return render(request, "app1/addcategorie.html",context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def deletecategorie(request , pk) : 
  item = Categorie.objects.get(id=pk)
  if request.method == "POST" :
    item.delete()
    return redirect('categories')

  context={'item':item }
  return render(request , 'app1/deletecategorie.html' , context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['client'])
def reservationclient(request,pk) : 
    reservations =Client_voyage.objects.filter(fk_client=pk)
    context = {'reservations':reservations}
    return render(request,"app1/reservationclient.html" , context)

@login_required(login_url='home') 
@allowed_users(allowed_roles=['client'])
def reserve(request,pk) : 
    voyageid = pk
    voyage = Voyage.objects.get(id=pk)
    userid = request.user.id 
    client = Client.objects.get(fk_user=userid)
    client_id = client.id
    admin = Adminstrateur.objects.get(id=2)
    if request.method == 'POST' : 
        # print('data : ',request.POST)
        customer = stripe.Customer.create(
            email = client.fk_user.email,
            name = client.fk_user.username,
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer = customer,
            amount = voyage.prix*100, #stripe kayst3ml cent so khask dreb f 100
            currency = 'mad',
            description = voyage.description
        )

        reservation = Client_voyage.objects.create(
                fk_client_id=client_id,
                fk_voyage=voyage,
                date_reservation=date.today(),
                amountPaid=voyage.prix,
                paymentStatus=True  # Set to True since the payment was successful
            )
        
        notification = Notification.objects.create(
            client=client,
            adminstrateur=admin,
            message=f"Notification pour réservation du voyage {voyage.id}",
        )

        voyage.nbr_places -= 1
        voyage.save()

        res_id = reservation.id
        context = {'prix' : voyage.prix,'res_id':res_id}
        return render(request,"app1/succes.html",context)


    context = {'voyageid' : voyageid}
    return render(request,"app1/reserve.html" , context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def hotels(request) : 
    hotels = Hotel.objects.all()
    context = {'hotels':hotels}
    return render(request,"app1/hotels.html" , context)



@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def addhotel(request):
    if request.method == 'POST':
        form = hotelForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            print("hotel tzad")
            return redirect('hotels')  
        else : 
            print("form addhotel fiha mochkil ")
            #return redirect('addvoyage')

    else:
        # If the request method is GET, render the form
        form = hotelForm()

    context = {'form': form}
    return render(request, 'app1/addhotel.html', context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def updatehotel(request , pk):
  hotel = Hotel.objects.get(id=pk)
  form = hotelForm(instance=hotel)
  if request.method == 'POST' : 
      form = hotelForm(request.POST ,request.FILES,instance=hotel)
      if form.is_valid :
        form.save()
        return redirect('hotels')
  context={'form' : form}
  return render(request, "app1/addhotel.html",context)



@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def deletehotel(request , pk) : 
  item = Hotel.objects.get(id=pk)
  if request.method == "POST" :
    item.delete()
    return redirect('hotels')

  context={'item':item }
  return render(request , 'app1/deletehotel.html' , context)



@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def vols(request) : 
    vols = Vol.objects.all()
    context = {'vols':vols}
    return render(request,"app1/vols.html" , context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def addvol(request):
    if request.method == 'POST':
        form = volForm(request.POST) 
        if form.is_valid():
            form.save()
            print("vol tzad")
            return redirect('vols')  
        else : 
            print("form addvol fiha mochkil ")
            #return redirect('addvoyage')

    else:
        # If the request method is GET, render the form
        form = volForm()

    context = {'form': form}
    return render(request, 'app1/addvol.html', context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def updatevol(request , pk):
  vol = Vol.objects.get(id=pk)
  form = volForm(instance=vol)
  if request.method == 'POST' : 
      form = volForm(request.POST ,instance=vol)
      if form.is_valid :
        form.save()
        return redirect('vols')
  context={'form' : form}
  return render(request, "app1/addvol.html",context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def deletevol(request , pk) : 
  item = Vol.objects.get(id=pk)
  if request.method == "POST" :
    item.delete()
    return redirect('vols')

  context={'item':item }
  return render(request , 'app1/deletevol.html' , context)



@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def admins(request) : 
    admins = Adminstrateur.objects.all()
    context = {'admins':admins}
    return render(request,"app1/admins.html" , context)



def detailsvoyage(request,pk) : 

    voyage = Voyage.objects.get(id=pk)
    context = {'voyage':voyage}

    return render(request,"app1/detailsvoyage.html",context)


def categorievoyage(request,pk) : 

    voyages = Voyage.objects.filter(categorie__nom=pk)
    context = {'voyages':voyages}
    return render(request,"app1/categorievoyage.html",context)



@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def clients(request) : 
    clients = Client.objects.all()
    print(clients)
    context = {'clients':clients}
    return render(request,"app1/clients.html" , context)





@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def sendnotification(request, pk):

    if request.method == 'POST':
        form = notificationForm(request.POST) 
        if form.is_valid():
            form.save()
            print("message tseft tzad")
            return redirect('clients')  
        else : 
            print("form addhotel fiha mochkil ")
            form = notificationForm() 

    else:
        # If the request method is GET, render the form
        form = notificationForm(initial={'client': pk, 'adminstrateur': request.user.id})

    context = {'form': form}
    return render(request, 'app1/sendnotification.html', context)

from django.shortcuts import get_object_or_404

@login_required(login_url='home') 
@allowed_users(allowed_roles=['client'])
def notifications(request):
    id_user = request.user.id
    client = get_object_or_404(Client, fk_user=id_user)
    
    notifications = Notification.objects.filter(client=client)
    print(notifications)
    
    context = {'notifications': notifications}
    return render(request, "app1/notifications.html", context)









@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def promotions(request) : 
    promotions = Promotion.objects.all()
    print(promotions)
    context = {'promotions':promotions}
    return render(request,"app1/promotions.html" , context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def addpromotion(request):
    if request.method == 'POST':
        form = promotionForm(request.POST) 
        if form.is_valid():
            form.save()
            print("promotion tzadt")
            return redirect('promotions')  
        else : 
            print("form addpromotion fiha mochkil ")
          

    else:
        # If the request method is GET, render the form
        form = promotionForm()

    context = {'form': form}
    return render(request, 'app1/addpromotion.html', context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def updatepromotion(request , pk):
  promotion = Promotion.objects.get(id=pk)
  form = promotionForm(instance=promotion)
  if request.method == 'POST' : 
      form = promotionForm(request.POST ,instance=promotion)
      if form.is_valid :
        form.save()
        return redirect('promotions')
  context={'form' : form}
  return render(request, "app1/addpromotion.html",context)


@login_required(login_url='home') 
@allowed_users(allowed_roles=['admin'])
def deletepromotion(request , pk) : 
  item = Promotion.objects.get(id=pk)
  if request.method == "POST" :
    item.delete()
    return redirect('promotions')

  context={'item':item }
  return render(request , 'app1/deletepromotion.html' , context)






@login_required(login_url='home') 
@allowed_users(allowed_roles=['client'])
def addcommentaire(request):
    if request.method == 'POST':
        form = commentaireForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('client')  
        else : 
            print("form addpromotion fiha mochkil ")
            id_user = request.user.id
            client = get_object_or_404(Client, fk_user=id_user)
            form = commentaireForm(initial={'client':client.id})
          

    else:
        # If the request method is GET, render the form
        id_user = request.user.id
        client = get_object_or_404(Client, fk_user=id_user)
        form = commentaireForm(initial={'client':client.id})

    context = {'form': form}
    return render(request, 'app1/commentaire.html', context)

@login_required(login_url='home')
@allowed_users(allowed_roles=['client'])
def download_pdf(request, pk):

    reservation = get_object_or_404(Client_voyage,id=pk)
    voyage = get_object_or_404(Voyage, id=reservation.fk_voyage.id)
    client = get_object_or_404(Client, fk_user=request.user.id)
    hotel = Hotel.objects.get(id=reservation.fk_voyage.hotel.id)
    vol = Vol.objects.get(id=reservation.fk_voyage.vol.id)

    template_path = 'app1/reservation_template.html'
    context = {'voyage': voyage, 'client': client, 'hotel': hotel,'vol':vol,'res_id':pk}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reservation.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    return response
