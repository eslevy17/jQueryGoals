from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core import serializers

import re, time, json
import datetime
import bcrypt

from apps.users.models import *

NAME_MATCH = re.compile(r'.[^1-9\s]*')
EMAIL_MATCH = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request,'users/login.html', {})

def success(request):
    if request.session['logged_in'] and request.session['user'] != {}:
        user = User.objects.get(id=request.session['user']['user_id'])
        request.session['user'] = {'user_id':user.id, 'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email}
    return redirect('/activities')

def logoff(request):
    if request.method == 'POST':
        request.session['logged_in'] = False
        request.session['user'] = {}
    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        if len(User.objects.filter(email=email)) > 0 and User.objects.get(email=email):
            user = User.objects.get(email=email)
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['logged_in'] = True
                request.session['user'] = {'user_id':user.id, 'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email}
                #messages.info(request, "You successfully registered (or loggined in)!")
                return redirect('../success')
        messages.info(request, "There was an error with logging in")
        return redirect('/')
    return redirect('/')

def register(request):
    if request.method != 'POST':
        return redirect('/')
    
    form = request.POST
    
    if len(form['first_name']) < 3 or len(form['last_name']) < 3 or len(form['email']) < 1 or len(form['password']) < 1 or len(form['confirm_password']) < 1 or form['password'] != form['confirm_password'] or (not EMAIL_MATCH.match(form['email']) and len(form['email']) > 0) or (len(form['password']) > 0 and len(form['password']) < 8 and form['password'] == form['confirm_password']):
        if len(form['email']) < 1:
            messages.error(request, "Email cannot be empty!")
        
        if len(form['first_name']) < 1:
            messages.error(request, "First name cannot be empty!")
        elif len(form['first_name']) <= 2:
            messages.error(request, "First name must be more than two letters!")
        
        if len(form['last_name']) < 1:
            messages.error(request, "Last name cannot be empty!")
        elif len(form['last_name']) <= 2:
            messages.error(request, "Last name must be more than two letters!")        
        
        if len(form['password']) < 1:
            messages.error(request, "Password cannot be empty!")
        
        if len(form['confirm_password']) < 1:
            messages.error(request, "Confirm Password cannot be empty!")
        
        if form['password'] != form['confirm_password']:
            messages.error(request, "Passwords do not match!")
        
        if not EMAIL_MATCH.match(form['email']) and len(form['email']) > 0:
            messages.error(request, "Invalid Email Address!")
        
        if len(form['password']) > 0 and len(form['password']) < 8 and form['password'] == form['confirm_password']:
            messages.error(request, "Password does not meet the minimum length of 8 characters!")
        
        return redirect('/')
    else:
        data = {'first_name': form['first_name'],
                'last_name': form['last_name'],
                'email': form['email'],
                'password': bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        }
        user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])
        request.session['logged_in'] = True
        request.session['user'] = {'user_id':User.objects.get(email=data['email']).id, 'first_name':data['first_name'], 'last_name':data['last_name'], 'email':data['email']}
        #messages.info(request, "You successfully registered (or logged in)!")
        
        return redirect('../success')

def user(request, num=None):
    users = User.objects.filter(id=num)
    if len(users) > 0:
        return render(request, "users/user.html", {})
    return redirect('/activities')

def edit_user(request):
    if request.method != 'POST':
        return redirect('/success')
    
    form = request.POST
    
    errors = {}
    
    user = User.objects.get(id=request.session['user']['user_id'])
    if len(form['first_name']) < 3 or len(form['last_name']) < 3 or ((form['email'] != user.email and len(User.objects.filter(email=form['email'])) > 0) or (not EMAIL_MATCH.match(form['email']))):
        if (form['email'] != user.email and len(User.objects.filter(email=form['email'])) > 0) or (not EMAIL_MATCH.match(form['email'])):
            messages.error(request, "Error cannot change email")
        
        if len(form['first_name']) < 3:
            messages.error(request, "First name cannot be less than three characters")
        if len(form['last_name']) < 3:
            messages.error(request, "Last name cannot be less than three characters")        
        return redirect('/myaccount/{id}'.format(id=user.id))        
    
    
    user.email = form['email']
    user.first_name = form['first_name']
    user.last_name = form['last_name']    
    user.save()
    
    request.session['user'] = {'user_id':user.id, 'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email}
    
    return redirect('/success')

def myaccount(request, num=None):
    if num != request.session['user']['user_id']:
        return redirect('/activities')
    return render(request, "users/myaccount.html", {})

def activities(request):
    if not ('logged_in' in request.session.keys()) and not request.session['logged_in'] and request.session['user'] == {}:
        return redirect('/')
    
    today = datetime.date.today()
    lastMonth = today-datetime.timedelta(days=7)
    
    goals = User.objects.get(email=request.session['user']['email']).goals.all()
    #events = Event.objects.filter(user=User.objects.get(email=request.session['user']['email'])).filter(created_at__range=(lastMonth, today)).all()
    
    days = ["Today", "Yesterday", "2 Days Ago", "3 Days Ago",
            "4 Days Ago", "5 Days Ago", "6 Days Ago"]
    
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    
    a = {str(goal.id):[] for goal in goals}
    b = {str(goal.id):[] for goal in goals}
    
    
    for goal in goals:
        j = { day:0 for day in days[::-1] }
        y = { month:0 for month in months }
        for event in goal.events.all():
            if event.created_at >= lastMonth:
                diffTime = int(abs((event.created_at - today).total_seconds()/(24*3600)))
                j[days[diffTime]] = event.duration
            
            if event.created_at.year == today.year:
                y[months[event.created_at.month-1]] += event.duration
        #print(y)
        
        for day in days[::-1]:
            a[str(goal.id)].append({'label':day, 'y':j[day]})
        
        for month in months:
            b[str(goal.id)].append({'label':month, 'y':y[month]})
    
    return render(request, "users/activity_progress.html", {'goals':goals, 'events':a, 'months':b})

def add_goal(request):
    if request.method != 'POST' or (not request.session['logged_in'] and request.session['user'] == {}):
        return redirect('/activities')
    
    form = request.POST
    
    user = User.objects.get(email=request.session['user']['email'])
    
    if len(Activity.objects.filter(activity=form['activity'])) > 0:
        activity = Activity.objects.get(activity=form['activity'])
    else:
        activity = Activity.objects.create(activity=form['activity'])
    
    if len(Goal.objects.filter(user=user).filter(activity=activity)) > 0:
        goal = Goal.objects.get(user=user, activity=activity)
        goal.goal = int(form['hours'])
        goal.save()
    else:
        goal = Goal.objects.create(goal=int(form['hours']), user=user, activity=activity)
    return redirect('/activities')    

def add_event(request):
    if request.method != 'POST' or (not request.session['logged_in'] and request.session['user'] == {}):
        return redirect('/activities')
    
    form = request.POST
    
    conv = time.strptime(form['date'], "%b %d, %Y")
    date = time.strftime("%Y-%m-%d", conv).split('-')
    date = datetime.date(int(date[0]), int(date[1]), int(date[2]))    
    
    user = User.objects.get(email=request.session['user']['email'])
    goal = Goal.objects.get(user=user, id=form['goal_id'])
    activity = Activity.objects.get(id=goal.activity.id)
    
    if len(goal.events.filter(created_at=date, goal=goal, user=user)) > 0:
        event = Event.objects.get(created_at=date, goal=goal, user=user)
        event.duration = float(form['duration'])
        event.save()
    else:
        Event.objects.create(duration=float(form['duration']), user=user, activity=activity, goal=goal, created_at=date)
    
    return redirect('/activities')

def addToEvent(request):
    if request.method != 'POST':
        return HttpResponse('hi')
    form = request.POST
    
    goal = Goal.objects.get(id=form['id'])
    goal.goal += 3
    goal.save()
    
    json_data = {'data':serializers.serialize('json', goal.events.all()), 'total':goal.goal}
    return HttpResponse(json.dumps(json_data), content_type="application/json")