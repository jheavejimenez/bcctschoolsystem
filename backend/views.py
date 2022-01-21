from django.shortcuts import render
from backend.models import *
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect


def index(request):
    template = 'home.html'
    context = {}
    return render(request, template, context)


def about_view(request):
    template = 'about.html'
    context = {}
    return render(request, template, context)


def login_view(request):
    logout(request)
    username = password = ''
    template = 'login.html'
    context = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            context.update(
                error_message='Authentication Error - Please check your username and password.')
        elif user.is_active and user.is_staff:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL, request.path)
        else:
            context.update(
                error_message='Your account has been disabled please wait for approval.'
            )
            return render(request, template, context)
    return render(request, template, context)


def contact_view(request):
    template = 'contact.html'
    context = {}
    return render(request, template, context)


def registration_view(request):
    template = 'registration.html'
    strand = Strand.objects.all()
    print(strand)
    context = {}
    context.update(strand=strand)
    if request.method == 'GET':
        return TemplateResponse(request, template, context)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        first_name = request.POST.get('first_name')
        strand = request.POST.get('strand')
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        hashed_password = make_password(password)
        set_strand = Strand.objects.get(pk=strand)
        student = Student.objects.filter(
            Q(last_name=last_name) &
            Q(middle_name=middle_name) &
            Q(first_name=first_name)
        )
        if student:
            context.update(
                error_message="Student is already Registered"
            )
            return TemplateResponse(request, template, context)

        Student.objects.create(
            last_name=last_name,
            first_name=first_name,
            password=hashed_password,
            username=username,
            middle_name=middle_name,
            birth_date=birthdate,
            gender=gender,
            strand=set_strand,
            email=email,
            my_password="Set by Student",
        )
        context.update(
            error_message="You are now Successfully Registered"
        )
        return TemplateResponse(request, template, context)


def oldstud_view(request):
    template = 'oldstud.html'
    context = {}

    return render(request, template, context)
