from django.shortcuts import render
from backend.models import Company, FoodEvent

def mayasPage(request):
	return render(request,'base.html')

def company(request, id):
	c = Company.objects.get(id=int(id))
	company = {}
	company['name'] = c.name
	company['phone'] = c.phone
	company['email'] = c.email
	company['website'] = c.website
	events = []
	e = FoodEvent.objects.filter(company_id=int(id))
	for event in e:
		events.append(event)
	company['events'] = events
	print events
	return render(request,'company.html',{'company':company})