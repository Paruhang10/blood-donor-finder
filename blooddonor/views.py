from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Donor, BloodRequest
from .algorithm import find_donors

# HOME PAGE
def home(request):
    return render(request, 'home.html')

# REGISTER PAGE
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        blood_group = request.POST['blood_group']
        district = request.POST['district']
        phone = request.POST['phone']

        # create user using Django built-in auth
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.first_name = name
        user.save()

        # create donor profile
        Donor.objects.create(
            user=user,
            blood_group=blood_group,
            district=district,
            phone=phone
        )
        return redirect('/login')
    return render(request, 'register.html')

# LOGIN PAGE
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password!'})
    return render(request, 'login.html')

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('/login')

# DASHBOARD
@login_required
def dashboard(request):
    donor = Donor.objects.get(user=request.user)
    # get all blood requests sent to this donor
    requests = BloodRequest.objects.filter(donor=donor)
    return render(request, 'dashboard.html', {
        'donor': donor,
        'requests': requests
    })
# SEARCH PAGE
def search(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        district = request.POST['district']
        results = find_donors(blood_group, district)
        return render(request, 'results.html', {
            'results': results,
            'blood_group': blood_group,
            'district': district
        })
    return render(request, 'search.html')

# TOGGLE AVAILABILITY
@login_required
def toggle(request):
    donor = Donor.objects.get(user=request.user)
    # if available make unavailable and vice versa
    donor.is_available = not donor.is_available
    donor.save()
    return redirect('/dashboard/')

# REQUEST PAGE - patient sends blood request to specific donor
def submit_request(request, donor_id):
    # get donor by id from database
    donor = Donor.objects.get(id=donor_id)

    if request.method == 'POST':
        # save patient request details to database
        BloodRequest.objects.create(
            patient_name=request.POST['patient_name'],
            blood_group_needed=request.POST['blood_group_needed'],
            district=request.POST['district'],
            phone=request.POST['phone'],
            donor=donor
        )
        return redirect('/request-sent/')

    # show request form with selected donor info
    return render(request, 'request.html', {'donor': donor})

# REQUEST SENT PAGE - confirmation after request is submitted
def request_sent(request):
    return render(request, 'request_sent.html')