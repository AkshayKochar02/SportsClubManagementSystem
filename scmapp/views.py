"""views python file docstring """
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from scmapp.models import User, Admin, Event, Book_ground


# Create your views here.


def index(request):
 #User Registration / Login Page
    return render(request,'registration.html')


def user_home(request):
 #User Home Page
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}

        if 'book_status' in request.session:
            data['status'] = request.session['book_status']

        return render(request,'user_home.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'registration.html',context=data)


def user_event(request):
 #User Event Page
    if 'uname' in request.session:
        event = Event.objects.all()
        data = {'event':event}
        return render(request,'user_event.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'registration.html',context=data)


def ground_booking(request):
 #User Ground Booking Page
    if 'uname' in request.session:
        data = {'date':datetime.date.today()}
        return render(request,'ground_booking.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'registration.html',context=data)


def user_logout(request):
 #User Logout
    if 'uname' in request.session:
        del request.session['uname']

    if 'book_status' in request.session:
        del request.session['book_status']

    return render(request,'registration.html')


def admin_login(request):
 #Admin Login Page
    return render(request,'admin_login.html')


def admin_home(request):
 #Admin Home Page
    if 'aname' in request.session:
        data = {'name':request.session.get('aname')}
        return render(request,'admin_home.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'admin_login.html',context=data)


def admin_booking(request):
 #Admin View Bookings
    if 'aname' in request.session:
        booking = Book_ground.objects.all()
        data = {'booking':booking}
        return render(request,'admin_booking.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'admin_login.html',context=data)


def admin_event(request):
 #Admin Manage Event Page
    if 'aname' in request.session:
        event = Event.objects.all()
        data = {'event':event}

        if 'event_status' in request.session:
            data['status'] = request.session.get('event_status')

        return render(request,'admin_event.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'admin_login.html',context=data)


def update_event(request,my_id):
 #Admin Update Event Page
    if 'aname' in request.session:
        event = Event.objects.get(eid=my_id)
        event.date = event.date.strftime('%Y-%m-%d')
        event.time = event.time.strftime('%H:%M:%S')
        data = {'event':event}
        return render(request,'update_event.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'admin_login.html',context=data)


def add_event(request):
 #Admin Add Event Page
    if 'aname' in request.session:
        return render(request,'add_event.html')
    else:
        return HttpResponse('Something went wrong')


def admin_logout(request):
 #Admin Logout
    if 'aname' in request.session:
        del request.session['aname']

    if 'event_status' in request.session:
        del request.session['event_status']

    return render(request,'admin_login.html')


def test(request):
 #BACKEND -> For User Registration
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        re_password = request.POST.get('repassword')

        if(password == re_password):
            user = User(name=name,email=email,gender=gender,password=password)
            user.save()
            request.session['uname'] = name
            return user_home(request)
        else:
            data = {'status':"Password and Re-entered password must be same"}
            return render(request,'registration.html',context=data)
    else:
        return HttpResponse("Something went wrong!!!!!")


def login_user(request):
 #BACKEND -> For User Login
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = User.objects.get(name=name)

            if user.password == password:
                request.session['uname'] = name
                return user_home(request)
            else:
                data = {'status':"Incorrect Password!!!"}
                return render(request,'registration.html',context=data)

        except Exception as e:
            data = {'status':"User does not exists! You have to register first."}
            return render(request,'registration.html',context=data)
    else:
        return HttpResponse("Something went wrong!!!!!")


def login_admin(request):
 #BACKEND -> For Admin Login
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Admin.objects.get(name=name)

            if user.password == password:
                request.session['aname'] = name
                # return HttpResponse('ffaf')
                return admin_home(request)
            else:
                data = {'status':"Incorrect Password!!!"}
                return render(request,'admin_login.html',context=data)

        except Exception as e:
            data = {'status':"Invalid Username"}
            return render(request,'admin_login.html',context=data)
    else:
        return HttpResponse("Something went wrong faffsffa!!!!!")


def db_ground_booking(request):
 #BACKEND -> For Ground Booking
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        date = request.POST.get('date')
        time = request.POST.get('time')

        try:
            book = Book_ground.objects.get(date=date)
            data = {'status':'Please select other date'}
            return render(request,'ground_booking.html',context=data)
        except Exception as e:
            user = User.objects.get(name=request.session['uname'])
            book = Book_ground(uid=user.uid,name=user.name,mobile=mobile,date=date,time=time)
            book.save()
            request.session['book_status'] = "Booking successful"
            return user_home(request)
    else:
        return HttpResponse("Something went wrong!!!!!")


def db_update_event(request,my_id):
 #BACKEND -> For Update Event
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        duration = request.POST.get('duration')

        event = Event.objects.get(eid=my_id)
        event.name = name
        event.date = date
        event.time = time
        event.duration = duration
        event.save()

        request.session['event_status'] = 'Event updated successfuly'
        return admin_event(request)
    else:
        return HttpResponse("Something went wrong!!!!!")


def db_delete_event(request,my_id):
 #BACKEND -> For Delete Events
    if request.method == 'GET':
        event = Event.objects.get(eid=my_id)
        event.delete()

        request.session['event_status'] = 'Event deleted successfuly'
        return admin_event(request)
    else:
        return HttpResponse("Something went wrong!!!!!")


def db_add_event(request):
 #BACKEND -> For Add Event
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        duration = request.POST.get('duration')

        event = Event(name=name,date=date,time=time,duration=duration)
        event.save()
        request.session['event_status'] = 'Event added successfuly'
        return admin_event(request)
    else:
        return HttpResponse("Something went wrong!!!!!")
