from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here.
def registration(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if (len(username) > 300):
            messages.info(request,"Username should be less than 300 characters long")
            return redirect('/users/registration?uname={0}&fname={1}&lname={2}&email={3}'.format(username, first_name, last_name, email))
        elif (len(email) > 254):
            messages.info(request,"Email should be less than 254 characters long")
            return redirect('/users/registration?uname={0}&fname={1}&lname={2}&email={3}'.format(username, first_name, last_name, email))

        if (len(password1) < 8 or
            len(password1) > 20 or
            not password1.isalnum()):

            messages.info(request,"Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.")
            return redirect('/users/registration?uname={0}&fname={1}&lname={2}&email={3}'.format(username, first_name, last_name, email))

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                return redirect('/users/registration?uname={0}&fname={1}&lname={2}&email={3}'.format(username, first_name, last_name, email))

            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email already exists")
                return redirect('/users/registration?uname={0}&fname={1}&lname={2}&email={3}'.format(username, first_name, last_name, email))

            else:
                try:
                    user = User.objects.create_user(
                        username = username,
                        password = password1,
                        email = email,
                        first_name = first_name,
                        last_name = last_name
                    )
                    user.save()
                except:
                    messages.info(request,"Something went wrong! Please try again")
                    return redirect('/users/registration?uname={0}&fname={1}&lname={2}&email={3}'.format(username, first_name, last_name, email))

        else:
            messages.info(request,"Passwords do not Match")
            return redirect('/users/registration?uname={0}&fname={1}&lname={2}&email={3}'.format(username, first_name, last_name, email))

        return redirect("/users/login")

    else:
        uname = fname = lname = email = ''
        if request.method == "GET":
            uname = request.GET.get('uname') if ('uname' in request.GET) else ''
            fname = request.GET.get('fname') if ('fname' in request.GET) else ''
            lname = request.GET.get('lname') if ('lname' in request.GET) else ''
            email = request.GET.get('email') if ('email' in request.GET) else ''

        return render(request,'users/registration.html', {
            'uname' : uname,
            'fname' : fname,
            'lname' : lname,
            'email' : email,
        })


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid credentials")
            return redirect("/users/login")

    else:
        return render(request,'users/login.html')



def logout(request):
    if not request.user.is_authenticated:
        return redirect('/')

    auth.logout(request)
    return redirect("/")


def profile(request, username):
    return redirect("/")
