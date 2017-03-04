from django.shortcuts import render,redirect
from .models import Event, Center, Message, Citizen,Copy, Hospital,sms,Attacker
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from twilio.rest import TwilioRestClient 
import urllib2
import json
import operator
from random import randint
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Victim
from django.http import HttpResponse, JsonResponse
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
import urllib
import os
from PyDictionary import PyDictionary

#import simplejson as simplejson

def heatmap(request):
	return render(request, 'heatmap.html')

def get_location(request):
	if(request.method == 'POST'):
		print('working')
		lattitude = request.POST.get('glat')
		longitude = request.POST.get('glng')
		event = Event.objects.create()
		event.lat = lattitude
		event.lng = longitude
		event.save()
		#event = Event.objects.get(id=id)
		#event.location = str(locations.id)
		#event.save()
		#loc_id = locations.id 
		print(lattitude)
		print(longitude)
		return HttpResponseRedirect('/disaster/'+str(event.id))
	else:
		return render(request,'get_location.html')

def disaster_information(request,did):
	if(request.method == 'POST'):
		print('working')
		event = Event.objects.get(id=int(did))
		name = request.POST.get('name')
		description = request.POST.get('description')
		radius = request.POST.get('radius')
		event.name = name
		event.description = description
		event.radius = radius
		event.save()
		#send_sms('HHAHAHAHA','+919833175929')
		return HttpResponseRedirect('/suggest/'+str(did))
		
	else:
		event = Event.objects.get(id=int(did))
		return render(request,'disaster_information.html',{'id':did,'event':event})

def send_sms(message,number):
	ACCOUNT_SID = "InsertSIDHere" 
	AUTH_TOKEN = "InsertTokenHere" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 	client.messages.create(
    to=number, 
    from_="+16155675585", 
    body=message,
	)


def suggest(request,did):
	
	event = Event.objects.get(id=did)
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+event.lat+","+event.lng+"&radius=2000&types=hospital&key=insertKeyHere"
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	print(type(json_response))
	print(response)
	results = json_response["results"]
	hospital_arr = []
	for result in results:
		if 'hospital' in result["name"] or 'Hospital' in result["name"]:
			place = Center.objects.create()
			place.name = result["name"]
			place.vicinity = result["vicinity"]
			place.place_id = result["id"]
			place.lat = result["geometry"]["location"]["lat"]
			place.lng = result["geometry"]["location"]["lng"]
			place.did = did
			place.typeof = 'H'
			types = ''
			for keyword in result["types"]:
				types = types + ' ' + keyword
			
			place.types = types
			place.save()
			hospital_arr.append(place)
	
	police_arr = []
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+event.lat+","+event.lng+"&radius=2000&types=police&key=InsertKeyHere"
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	print(type(json_response))
	print(response)
	results = json_response["results"]
	for result in results:
		if 'police' in result["name"] or 'Police' in result["name"]:
			place = Center.objects.create()
			place.name = result["name"]
			place.vicinity = result["vicinity"]
			place.place_id = result["id"]
			place.lat = result["geometry"]["location"]["lat"]
			place.lng = result["geometry"]["location"]["lng"]
			place.did = did
			place.typeof = 'P'
			types = ''
			for keyword in result["types"]:
				types = types + ' ' + keyword
			
			place.types = types
			place.save()
			police_arr.append(place)
	
	hosp = hospital_arr[0]
	pol = police_arr[0]
	message = 'A disaster ' + str(event.name) + ' has struck your locality. Kindly be careful.' + ' Description ' + str(event.description) + ' The nearest hospital is: ' +str(hosp.name) + '  at : '  + str(hosp.vicinity) + ' Nearest Police Station ' + pol.name + ' at : ' + pol.vicinity + '  Thank You' 
	#number = '+919773876646'
	#number = '+919930087431'
	number = '+919833175929'
	print(message)
	send_sms(message,number)
	#return render(request,'suggest.html')
	return render(request,'suggest.html',{'hosp':hospital_arr,'pol':police_arr,'did':did})
	
	arr = Center.objects.all()
	arr = arr[1:7]
	retrieve_messages()
	return render(request,'suggest.html',{'hosp':arr,'did':did})

def retrieve_messages():
	ACCOUNT_SID = "ACe7bf6e6156e9e765ca4067f186fa0955" 
	AUTH_TOKEN = "491b594692de8545d7782c8e97aaa9b9" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 	#client.messages.create(
    #to=number, 
    #from_="+16155675585", 
    #body=message,
	#)
	smss = client.sms.messages.list()
	for sms in smss:
		print(sms.body)
	#print(smss)

def monitor(request):
	dictionary=PyDictionary()

	ACCOUNT_SID = "InsertSIDHere" 
	AUTH_TOKEN = "InsertTokenHere" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 	messages = client.sms.messages.list()
 	for message in messages:
 		if(message.direction == 'inbound' and message.from_ == '+919930087431'):
 			print('hurray')
 			
 			msg,notfound = sms.objects.get_or_create(message_id = message.sid)
 			if notfound:
	 			msg.body = message.body
	 			msg.number = message.from_ 
				msg.save()
			else:
				pass
	messages = sms.objects.all()
	terms = {}
	data = []
	labels = []
	for message in messages:
		if message.number == '+919930087431':
			keywords = message.body.split(' ')
			for keyword in keywords:
				if len(keyword) > 0 :
					if keyword in terms:
						terms[keyword] = terms[keyword] + 1
					else:
						terms[keyword] = 1 
	
	terms = sorted(terms.items(), key=operator.itemgetter(1),reverse=True)
	print terms
	
	for dat in terms:
		#print dat
		data.append(dat[1])
		labels.append(dat[0])
	

	#data = '[51, 30, 40, 28, 92, 50, 92]'
	#labels = []
	#labels.append('January')
	#labels = "['January', 'February', 'March', 'April', 'May', 'June', 'July']"
	#return HttpResponse('ok')
	for idx,label in enumerate(labels):
		syns = dictionary.synonym(label)
		if syns:
			for syn in syns:
				labels[idx] = labels[idx] + ' ' + str(syn)
		print(idx)
		print(label)

	
	jlabels = json.dumps(labels)

	return render(request,'monitor.html',{'data':data,'labels':jlabels})

def alt_heatmap(request,did):
	#lat = ['18.9622417','18.9622217']
	#lng = ['72.8389009','72.8389296']
	clat = Event.objects.get(id=did).lat
	clng = Event.objects.get(id=did).lng
	lat = []
	lng = []
	centers = Citizen.objects.all()
	for center in centers:
		lat.append(center.lat)
		lng.append(center.lng)
	cord = zip(lat,lng)
	return render(request,'heatmap.html',{'cord':cord,'clat':clat,'clng':clng})


def test(request):
	centers = Copy.objects.all()
	for center in centers:
		citizen = Citizen.objects.create()
		citizen.name = 'Test-User-' + str(randint(0,1000))
		citizen.age = str(randint(20,35))
		citizen.lng = center.lng
		citizen.lat = center.lat
		citizen.phone = '+9198331759'+str(randint(10,99))
		citizen.gender = 'male'
		citizen.save()

	return HttpResponse('done')

def monitor_center(request,did):
	centers = Center.objects.filter(did=did)
	hosp_arr = []
	police_arr = []
	hosp_empty = []
	hosp_full = []
	police_dat = []
	hosp_objs = []
	for center in centers:
		if center.typeof == 'H':
			#if 'hospital' in center.name or 'Hospital' in center.name:
			hosp,created = Hospital.objects.get_or_create(cid=center.id)
			if created:
				hosp.current_status = str(randint(1,50))
				hosp.capacity = str(randint(80,200))
				hosp.save()
			hosp_objs.append(hosp)
			current_status = hosp.current_status
			capacity = hosp.capacity
			hosp_empty.append(int(current_status))
			hosp_full.append(int(capacity))
			hosp_arr.append(center.name)
		else:
			police_arr.append(center.name)
	
	j_hosp_arr = json.dumps(hosp_arr)
	hosp_combined = zip(hosp_objs,hosp_arr) 
	print(hosp_arr)
	print(hosp_objs)
	event = Event.objects.filter()
	return render(request,'monitor_center.html',{'hosp_arr':j_hosp_arr,'hosp_empty':hosp_empty,
		'hosp_full':hosp_full,'did':did,'hosp_combined':hosp_combined})

def hospital_portal(request,hid):
	if(request.method=='POST'):
		hospital = Hospital.objects.get(id=hid)
		admitted = request.POST.get('admitted')
		discharged = request.POST.get('discharged')
		if admitted:
			new_admit = int(admitted)
			current_status = str(int(hospital.current_status) + new_admit)
			hospital.current_status = current_status
			hospital.save()
		if discharged:
			new_discharge = int(discharged)
			current_status = str(int(hospital.current_status) - new_discharge)
			hospital.current_status = current_status
			hospital.save()
		calc()
		return HttpResponseRedirect('/hospitalportal/'+str(hid))
		
	else:
		hospital = Hospital.objects.get(id=hid)
		return render(request,'hospital_portal.html',{'hospital':hospital})

def calc():
	
	ACCOUNT_SID = "InsertSIDHere" 
	AUTH_TOKEN = "InsertTokenHere" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 	messages = client.sms.messages.list()
 	for message in messages:
 		if(message.direction == 'inbound'):
 			msg,found = sms.objects.get_or_create(message_id = message.sid)
 			msg.body = message.body
 			msg.number = message.from_ 
			msg.save()
	print('lol')
	
	messages = Message.objects.all()
	for message in messages:
		if message.number == "+919833175929":
			if 'admit' in message.body:
				msg = message.body.strip()
				print msg
				number = int(msg[7:]) 
				
				#print (number)

			#print(message.body)

def home(request):
	return render(request, 'snap.html')

def detect_face(headers, cloud):
	params = urllib.urlencode({
	# Request parameters
	'returnFaceId': 'true',
	'returnFaceLandmarks': 'false'
	})
	body = {
	"url": str(cloud['url'])
	}

	r = requests.post('https://westus.api.cognitive.microsoft.com/face/v1.0/detect', params=params, data=str(body),
	headers=headers)

	return r

def find_similar(headers, cloud, faceId):
	body = {
	    # Request parameters
	    "faceId": str(faceId),
	    "faceListId": "my-face-list",  
	    "mode": "matchPerson"
	}

	r = requests.post('https://westus.api.cognitive.microsoft.com/face/v1.0/findsimilars', data=str(body), 
	    headers=headers)
	return r

def add_to_list(headers, cloud):
	params = urllib.urlencode({
	    # Request parameters
	    'faceListId' : 'my-face-list'
	})
	listId = 'my-face-list'
	body = {
	    "url": str(cloud['url'])   
	}
	r = requests.post('https://westus.api.cognitive.microsoft.com/face/v1.0/facelists/' + listId + '/persistedFaces', params=params, data=str(body),
	    headers=headers)

	return r

@csrf_exempt
def upload(request):
    cloudinary.config( 
      cloud_name = "degz2imaz", 
      api_key = "", 
      api_secret = "" 
    )
    if request.method == 'POST':
        #print 'yes'
        handle_uploaded_file(request.FILES['webcam'])
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '',
        }
        module_dir = os.path.dirname(__file__)
        img = os.path.join(module_dir, 'media/pictures/img.jpg')
        cloud = cloudinary.uploader.upload(img)
        victim = Victim.objects.create(url=cloud['url']) 
        #victim = Victim.objects.create(picture=request.FILES['webcam'])
        r = detect_face(headers, cloud)
        faceId = r.json()[0]['faceId']
        r = find_similar(headers,cloud, faceId)
        
        if len(r.json()) > 0:
            res = "Matched with:" + r.json()[0]['persistedFaceId']
            print res
            return JsonResponse({'found': 'True', 'res' : res})
            #return (200, res)
        else:
            r = add_to_list(headers, cloud)
            res = 'Face added to list' + r.text
            print res
            faceId = r.json()['persistedFaceId']
            victim.pic_id = faceId
            victim.save()
            return JsonResponse({'found': 'False', 'res' : res})
        print r.text
def save_victim(request):
    victim = Victim.objects.latest('url')
    victim.name = request.POST.get('name')
    victim.age = request.POST.get('age')
    victim.age = '21'
    victim.gender = request.POST.get('gender')
    victim.gender = 'M'
    victim.save()
    return render(request, 'snap.html', {'show' : True})
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def honey_pot(request):
    ip = get_client_ip(request)
    Attacker.objects.create(ip=ip)
    return redirect('/')
def attackers(request):
    attackers = Attacker.objects.all()
    return render(request, 'attacker.html', {'attackers': attackers})

def find_missing_person(request):
	if request.method == 'POST':
		notfound = False
		if request.POST.get('name'):
			name = request.POST.get('name')
			victim = Victim.objects.get(name=name)
			return render(request, 'find_person.html', {'victim' : victim, 'notfound' : False})
		else:
			cloudinary.config( 
			  cloud_name = "degz2imaz", 
			  api_key = "", 
			  api_secret = "" 
			)
			image = request.FILES['image']
			handle_uploaded_file(image)
			headers = {
			    # Request headers
			    'Content-Type': 'application/json',
			    'Ocp-Apim-Subscription-Key': '',
			}
			module_dir = os.path.dirname(__file__)
			img = os.path.join(module_dir, 'media/pictures/img.jpg')
			cloud = cloudinary.uploader.upload(img)
			r = detect_face(headers, cloud)
			faceId = r.json()[0]['faceId']
			print faceId
			r = find_similar(headers,cloud, faceId)
			if len(r.json()) > 0:
				faceId = r.json()[0]['persistedFaceId']
				print faceId
				victim = ''
				try:
					print 'here'
					victim = Victim.objects.get(pic_id=faceId)
					print 'here2'
				except Exception, e:
					notfound = True
			else:
				notfound = True
			return render(request, 'find_person.html', {'victim' : victim, 'notfound' : notfound})
			'''else:
				return render(request, 'find_person.html', {'notfound' : True})'''
	else:
		return render(request, 'find_person.html', {'notfound' : False})

def handle_uploaded_file(f):
	module_dir = os.path.dirname(__file__)
	img = os.path.join(module_dir, 'media/pictures/img.jpg')
	destination = open(img, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

def test_suggest(request,did):
	event = Event.objects.get(id=did)
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+event.lat+","+event.lng+"&radius=4000&types=restaurant&key=InsertKeyHere"
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	print(type(json_response))
	print(response)
	results = json_response["results"]
	hospital_arr = []
	for result in results:
		#if 'hospital' in result["name"] or 'Hospital' in result["name"]:
		place = Copy.objects.create()
		place.name = result["name"]
		place.vicinity = result["vicinity"]
		place.place_id = result["id"]
		place.lat = result["geometry"]["location"]["lat"]
		place.lng = result["geometry"]["location"]["lng"]
		place.did = did
		#place.typeof = 'H'
		types = ''
		for keyword in result["types"]:
			types = types + ' ' + keyword
		
		place.types = types
		place.save()
		hospital_arr.append(place)
	
	police_arr = []
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+event.lat+","+event.lng+"&radius=4000&types=cafe&key=InsertKeyHere"
	response = urllib2.urlopen(url).read()
	json_response = json.loads(response)
	print(type(json_response))
	print(response)
	results = json_response["results"]
	for result in results:
		#if 'police' in result["name"] or 'Police' in result["name"]:
		place = Center.objects.create()
		place.name = result["name"]
		place.vicinity = result["vicinity"]
		place.place_id = result["id"]
		place.lat = result["geometry"]["location"]["lat"]
		place.lng = result["geometry"]["location"]["lng"]
		place.did = did
		place.typeof = 'P'
		types = ''
		for keyword in result["types"]:
			types = types + ' ' + keyword
		place.types = types
		place.save()
		police_arr.append(place)
	return HttpResponse('lol')	
'''
def cleanup(request):
	ACCOUNT_SID = "InsertSIDHere" 
	AUTH_TOKEN = "InsertTokenHere" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 	messages = client.sms.messages.list()
 	
 	for message in messages:
 		if(message.direction == 'inbound'):
 			print message.body
 			#message.media_list.delete()
 			msg,found = sms.objects.get_or_create(message_id = message.sid)
 			msg.body = message.body
 			msg.number = message.from_ 
			msg.save()

'''

def hospital_edit(request,hid):
	ACCOUNT_SID = "InsertSIDHere" 
	AUTH_TOKEN = "InsertTokenHere" 
 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 	messages = client.sms.messages.list()
 	
 	for message in messages:
 		if(message.direction == 'inbound' and message.from_ == '+919833175929'):
 			print message.body
 			#message.media_list.delete()
 			msg,not_found = sms.objects.get_or_create(message_id = message.sid)
 			print(msg.body)
 			if not_found:
 				msg.body = message.body
	 			msg.number = message.from_ 
				msg.save()
 			else:
				pass
	messages = sms.objects.all()
	
	for message in messages:
		if 'admit' in message.body and message.number == '+919833175929' :
			number = int(message.body[8:])
			print number
			hosp = Hospital.objects.get(id=int(hid))
			hosp.current_status = str(int(hosp.current_status)+number)
			hosp.save()
	return HttpResponseRedirect('/hospitalportal/'+str(hid))

	






