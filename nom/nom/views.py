from django.shortcuts import render
from backend.models import Company, FoodEvent
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.http import (HttpResponse, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseServerError,
    HttpResponseRedirect)
from django.utils.decorators import method_decorator

from backend.models import User as UserData

import datetime

months = ["", "January", "February", "March", "April",
          "May", "June", "July", "August", "September",
          "October", "November", "December"]

def cmp_events(e1, e2):
  if cmp(e1.date, e2.date) == 0:
    return cmp(e1.startTime, e2.startTime)
  else:
    return cmp(e1.date, e2.date)

def parse_time(time_string):
  hour, minuteplus = time_string.split(":")
  minute, ampm = minuteplus.split(" ")
  hour, minute = int(hour), int(minute)
  hour += ((ampm == "PM" and hour != 12) * 12)
  return datetime.time(hour, minute)

def parse_date(date_string):
  day, monthplus, year = date_string.split()
  month = monthplus[:-1]
  day, month, year = int(day), months.index(month), int(year)
  return datetime.date(year, month, day)

def get_event_data(event):
  data = {}
  data["name"] = event.name
  data["num_attendees"] = event.attendees.count()
  data["org_name"] = event.company.name
  data["org_id"] = event.company.id
  data["org_phone"] = event.company.phone
  data["org_email"] = event.company.email
  data["start_time"] = event.startTime
  data["end_time"] = event.endTime
  data["date"] = event.date
  data["location"] = event.location
  data["description"] = event.description
  data["id"] = event.id
  return data 

class Context(object):

  @staticmethod
  def get_base_context(request):
    context = {"user": request.user}
    if (request.user.is_authenticated()):
      email = request.user.__dict__["_wrapped"].email
      ud = UserData.objects.get(email = email)
      context["ud"] = ud.__dict__
      context["ud"]["has_org"] = bool(ud.orgs.count())
    return context

class LoginView(View):
  def get(self, request):
    return render(request, "login.html")

  def post(self, request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect("/login")

class LogoutView(View):
  def get(self, request):
    logout(request)
    return HttpResponseRedirect("/login")

  def post(self, request):
    return self.get(request)

class SignupView(View):
  def get(self, request):
    return render(request, "signup.html", Context.get_base_context(request))

  def post(self, request):
    post_data = dict(request.POST)
    un = post_data["username"][0]
    pw = post_data["password"][0]
    email = post_data["email"][0]
    user = User.objects.create_user(un, email, pw)
    user.save()
    ud = UserData(name = un, email = email)
    ud.save()
    user_login = authenticate(username=un, password=pw)
    login(request, user_login)
    return HttpResponseRedirect("/")

class HomepageView(View):
  def get(self, request):
    if not request.user.is_authenticated():
      return render(request, "new_person_homepage.html", Context.get_base_context(request))
    events = list(FoodEvent.objects.all().order_by("date")[:10])
    events = sorted(events, cmp_events)[::-1]
    context = Context.get_base_context(request)
    context["events"] = map(lambda x: get_event_data(x), events)
    return render(request,'homepage.html', context)

class CompanyView(View):
  @method_decorator(login_required)
  def get(self, request, id):
    c = Company.objects.get(id=int(id))
    context = Context.get_base_context(request)
    company = {}
    company['name'] = c.name
    company['phone'] = c.phone
    company['email'] = c.email
    company['website'] = c.website
    context["company"] = company

    events = []
    e = list(FoodEvent.objects.filter(company_id=int(id)))
    e = sorted(e, cmp_events)[::-1]
    context['events'] = map(get_event_data, e)
    return render(request,'company.html',context)


class EventCreationView(View):
  @method_decorator(login_required)
  def get(self, request):
    context = Context.get_base_context(request)
    user_email = request.user.__dict__["_wrapped"].email
    ud = UserData.objects.get(email = user_email)
    context["orgs"] = []
    for org in ud.orgs.all():
      context["orgs"].append(org.__dict__)
    return render(request, 'create_event.html', context)

  @method_decorator(login_required)
  def post(self, request):
    post_data = dict(request.POST)
    org = Company.objects.get(id = int(post_data["org"][0]))
    event_name = post_data["name"][0]
    description = post_data["description"][0]
    start_time = parse_time(post_data["start_time"][0])
    end_time = parse_time(post_data["end_time"][0])
    event_date = parse_date(post_data["event_date"][0])
    location = post_data["location"][0]
    event = FoodEvent(name=event_name, company=org, date=event_date,
      startTime=start_time, endTime=end_time, location=location,
      description=description)
    event.save()
    user_email = request.user.__dict__["_wrapped"].email
    ud = UserData.objects.get(email = user_email)
    event.attendees.add(ud)
    event.save()
    return HttpResponseRedirect("/")

class OrganizationCreationView(View):
  @method_decorator(login_required)
  def get(self, request):
    return render(request, 'create_org.html', Context.get_base_context(request))

  @method_decorator(login_required)
  def post(self, request):
    post_data = dict(request.POST)
    name = post_data["name"][0]
    phone = post_data["phone"][0]
    email = post_data["email"][0]
    website = post_data["website"][0]
    user_email = request.user.__dict__["_wrapped"].email
    ud = UserData.objects.get(email = user_email)
    org = Company(name = name, phone = phone, email = email, website = website)
    org.save()
    ud.orgs.add(org)
    return HttpResponseRedirect("/")

class EventJoin(View):
  @method_decorator(login_required)
  def get(self, request, id):
    id = int(id)
    if (not FoodEvent.objects.filter(id = id).count()):
      return HttpResponseRedirect("/")
    user_email = request.user.__dict__["_wrapped"].email
    ud = UserData.objects.get(email = user_email)
    event = FoodEvent.objects.get(id = id)
    event.attendees.add(ud)
    return HttpResponseRedirect("/event/%d" % id)

class EventPageView(View):
  @method_decorator(login_required)
  def get(self, request, id):
    id = int(id)
    if (not FoodEvent.objects.filter(id = id).count()):
      return HttpResponseRedirect("/")
    event = FoodEvent.objects.get(id = id)
    context = Context.get_base_context(request)
    context["event"] = get_event_data(event)
    context["attendees"] = map(lambda x: x.name, event.attendees.all())
    user_email = request.user.__dict__["_wrapped"].email
    ud = UserData.objects.get(email = user_email)
    context["attending"] = event in ud.attended_events.all()
    return render(request, 'event.html', context)






