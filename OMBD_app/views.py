from django.shortcuts import render
import json
from django.core import serializers
from .models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
import re
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from tinyec import registry #('tinyec library' for ECDH in Python )
import secrets
import base64
#from .blowfish import *
from .algo import *
import cv2
import os
import numpy as np
import random
from django.core.mail import EmailMessage
from datetime import datetime
from datetime import date
import socket


@never_cache
# Create your views here.
###############LOGIN & REGISTRATION START
def display_login(request):
    return render(request, "login.html", {})


def show_register(request):
    return render(request, "register.html", {})

@never_cache
def logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    return render(request,'login.html')


def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

def generate_key():
	#The elliptic curve used for the ECDH calculations is 256-bit named curve brainpoolP256r1
	curve = registry.get_curve('brainpoolP256r1')

	PrivKey = secrets.randbelow(curve.field.n)
	print("private key:", PrivKey)
	PubKey = PrivKey * curve.g
	my_pubkey=compress(PubKey)
	print("public key:", compress(PubKey))

	return my_pubkey,PrivKey


def register(request):
	
	username = request.GET.get("uname")
	phone = request.GET.get("phone")
	email=request.GET.get("email_id")
	password = request.GET.get("pass")
	age=request.GET.get("age")
	gender=request.GET.get("gender")

	a = Users.objects.filter(username=username)
	c = a.count()
	if(c == 1):
	    return HttpResponse("[INFO]: Username is already Taken, Choose another one")
	else:
		if re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$',email):

			obj1=Temp_Users.objects.filter(username=username, phone=phone, email=email,password=password,age=age,gender=gender)
			cc=obj1.count()

			if(cc==1):
				return HttpResponse("Already Registered, Wait for Approval")
			else:

			    b = Temp_Users(username=username, phone=phone, email=email,password=password,age=age,gender=gender)
			    b.save()

			    return HttpResponse("Wait for the Approval")
		else:
			return HttpResponse("Try valid email id")


def check_login(request):
	username = request.GET.get("uname")
	password = request.GET.get("password")

	print(username)
	print(password)

	if username == 'admin' and password == 'admin':
		request.session["uid"] = "admin"
		return HttpResponse("Admin Login Successful")
	else:
	    d = Users.objects.filter(username=username, password=password)
	    c = d.count()
	    if c == 1:
	        d2 = Users.objects.get(username=username, password=password)
	        request.session["uid"] = d2.u_id
	        return HttpResponse("Login Successful")
	    else:
	        return HttpResponse("Invalid")

###############LOGIN & REGISTRATION END

@never_cache
###############ADMIN START
def show_home_admin(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		return render(request,'home_admin.html') 
	else:
		return render(request,'login.html')


@never_cache
def get_requests_admin(request):
	if 'uid' in request.session:
		request_list=Temp_Users.objects.all()

		return render(request,"view_requests_admin.html",{'rqst':request_list,})
	else:
		return render(request,'login.html') 



def approve(request):
	u_id=request.POST.get('u_id')
	username=request.POST.get('username')
	password=request.POST.get('password')
	phone=request.POST.get('phone')
	email=request.POST.get("email")
	age=request.POST.get('age')
	gender=request.POST.get('gender')

	obj1=Users(username=username, phone=phone, email=email,password=password,age=age,gender=gender)
	obj1.save()

	obj3=Temp_Users.objects.get(u_id=int(u_id))
	obj3.delete()

	#key generation
	public_key,private_key=generate_key()

	obj11=Users.objects.get(username=username)
	user_id=obj11.u_id
	print("user_id : ",user_id)

	obj2=Keys(u_id=user_id,public_key=public_key,private_key=private_key)
	obj2.save()

	return HttpResponse("<script>alert('Approved Successfully');window.location.href='/get_requests_admin/'</script>")

	
def reject(request):
	u_id=request.POST.get('u_id')
	obj1=Temp_Users.objects.get(u_id=int(u_id))
	obj1.delete()
	return HttpResponse("<script>alert('Request Rejected');window.location.href='/get_requests_admin/'</script>")


@never_cache
def view_users_admin(request):
	if 'uid' in request.session:
		users_list=Users.objects.all()

		return render(request,"view_users_admin.html",{'usr':users_list,})
	else:
		return render(request,'login.html') 

#############ADMIN END

################USER START
@never_cache
def show_dmbd_user(request):
	if 'uid' in request.session:
		u_id=request.session['uid']
		obj1=Users.objects.get(u_id=int(u_id))
		u_name=obj1.username
		return render(request,'dmbd_user.html',{'username':u_name}) 
	else:
		return render(request,'login.html')
		
def get_images(request):
	username=request.GET.get("my_username")
	print("username : ",username)

	path="OMBD_app/static/Decoy_images/"+username
	files=os.listdir(path)
	print(files)
	print(len(files))

	data={}
	data["key"]=files

	return JsonResponse(data,safe=False)

@never_cache
def go_to_verification(request):
	if 'uid' in request.session:
		return render(request,'verification_user.html') 
	else:
		return render(request,'login.html')

def verify_key(request):
	get_key=request.POST.get("private_key")
	u_id=request.session["uid"]

	print("get_key : ",get_key)
	print("user_id : ",u_id)

	obj1=Keys.objects.get(u_id=int(u_id))
	private_key=obj1.private_key

	print("private_key :",private_key)

	if(get_key==private_key):
		return HttpResponse("<script>alert('Key Verification Successful');window.location.href='/upload_data_user/'</script>")
	else:
		return HttpResponse("<script>alert('Verification Failed! Enter correct Key');window.location.href='/go_to_verification/'</script>")


@never_cache
def upload_data_user(request):
	if 'uid' in request.session:
		return render(request,'upload_data_user.html') 
	else:
		return render(request,'login.html')


def create_decoy(image_category,username,file_name):

	if not os.path.isdir("OMBD_app/static/Decoy_images/"+username):
		os.makedirs("OMBD_app/static/Decoy_images/"+username)

	if image_category=="X_Ray Images":
		path="OMBD_app/static/All_Decoy/X_Ray Images"
		files=os.listdir(path)
		d=random.choice(files)
		print("*************")
		print(d)
		decoy=cv2.imread(path+"/"+d)
		cv2.imwrite("OMBD_app/static/Decoy_images/"+username+"/"+file_name,decoy)

	else:
		path="OMBD_app/static/All_Decoy/MRI Images"
		files=os.listdir(path)
		d=random.choice(files)
		print("*************")
		print(d)
		decoy=cv2.imread(path+"/"+d)
		cv2.imwrite("OMBD_app/static/Decoy_images/"+username+"/"+file_name,decoy)

		


def upload(request):
	u_id=request.session["uid"]
	image_category=request.POST.get("s1")
	encryption_key=request.POST.get("public_key")
	f2= request.FILES["file"]
	file_name=str(f2.name)

	print("image_category: ",image_category)
	print("encryption_key: ",encryption_key)
	print("f2: ",f2)
	print("file_name: ",file_name)

	obj22=Users.objects.get(u_id=int(u_id))
	username=obj22.username

	if image_category=="Select Category":
		return HttpResponse("<script>alert('Please Select an Image Category');window.location.href='/upload_data_user/'</script>")
	else:
		obj1=Keys.objects.get(u_id=int(u_id))
		user_public_key=obj1.public_key
		print("user_public_key : ",user_public_key)

		if(user_public_key!=encryption_key):
			return HttpResponse("<script>alert('Please Enter Valid Encryption Key');window.location.href='/upload_data_user/'</script>")
		else:
			fs1 = FileSystemStorage("OMBD_app/static/uploaded_images/"+username)#%username
			fs1.save(f2.name, f2)

			image=cv2.imread("OMBD_app/static/uploaded_images/"+username+"/"+str(f2.name))

			create_decoy(image_category,username,file_name)

			with open("OMBD_app/static/uploaded_images/"+username+"/"+str(f2.name), "rb") as imageFile:
				#read image and convert to bytes
				message = base64.b64encode(imageFile.read())
				# print(type(message))
				print(message)
				# print(len(message))
				print("$$$$$$$$$$$$$$$$$$$$$")
				# print(type(encryption_key))
				# print(len(encryption_key))
				new_en=encryption_key[:10]
				# print("new_en: ",new_en)
				# print(len(new_en))

				#converts bytes to string format
				msg=message.decode()
				print("@@@@@@@@")
				print(msg)
				# print(type(msg))
				print("@@@@@@@@")
				#call encryption function
				encrypted_msg = encrypt_msg(msg,new_en)
				print(encrypted_msg)

			obj30=Images(username=username,image_name=file_name,encrypted_image=encrypted_msg)
			obj30.save()

			return HttpResponse("<script>alert('Image Uploaded Successfully');window.location.href='/upload_data_user/'</script>")

def mail_to(get_email,time,current_date,hostname,IPAddr):
    try:
        message="Attack Detected\n\n Date=%s \n Time=%s \n Hostname=%s \n IPAddress=%s"%(current_date,time,hostname,IPAddr)
        email = EmailMessage('Attack', message, to=[get_email])
        email.send()
    except Exception as e:
        print(e)    
        pass


def send_mail(request):
	username=request.GET.get("my_username")

	obj1=Users.objects.get(username=username)
	get_email=obj1.email

	now = datetime.now()
	time = now.strftime("%H:%M:%S")
	print("Current Time =", time)
	print(type(time))

	today = date.today()
	current_date = today.strftime("%d/%m/%Y")
	print("date =",current_date)
	print(type(current_date))

	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)
	print("hostname : ",hostname)
	print("IPADDRESS : ",IPAddr)

	#send mail (enable this)
	#mail_to(get_email,time,current_date,hostname,IPAddr)

	return HttpResponse("hai")


@never_cache
def show_data_user(request):
	if 'uid' in request.session:
		u_id=request.session['uid']
		obj1=Users.objects.get(u_id=int(u_id))
		u_name=obj1.username

		data_list=Images.objects.filter(username=u_name)

		return render(request,"show_data_user.html",{'data':data_list,})
	else:
		return render(request,'login.html') 

def download(request):
	image_id=request.POST.get('image_id')
	image_name=request.POST.get('image_name')
	encrypted_image=request.POST.get('encrypted_image')
	decryption_key=request.POST.get('decryption_key')


	u_id=request.session["uid"]
	obj1=Keys.objects.get(u_id=int(u_id))
	get_key=obj1.public_key

	if(decryption_key!=get_key):
		return HttpResponse("<script>alert('Please provide valid Decryption Key');window.location.href='/show_data_user/'</script>")
	else:
		new_dec=decryption_key[:10]

		decrypted_msg = decrypt_msg(encrypted_image,new_dec)
		print(decrypted_msg)
		print(type(decrypted_msg))
		result = bytes(decrypted_msg, 'utf-8')
		print(result)
		print(type(result))

		image_64_decode = base64.b64decode(result) 
		image_result = open("OMBD_app/static/Decrypted_Images/"+image_name, 'wb') # create a writable image and write the decoding result
		image_result.write(image_64_decode)


		try:
			file1_path = "OMBD_app/static/Decrypted_Images/"+image_name
			print(os.path.exists(file1_path))
			print(file1_path)
			print("********************")
			print(os.path.basename(file1_path))

			if os.path.exists(file1_path):
			    with open(file1_path, 'rb') as fh:
			        response = HttpResponse(fh.read(), content_type="image/jpg")#image/jpg #application/vnd.ms-excel
			        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file1_path)
			        return response
			raise HttpResponse("<script>alert('File does not exists');window.location.href='/show_data_user/'</script>")
		except Exception as ex:
			print("Exception: ",ex)
			print("--")

			return HttpResponse("<script>alert('File does not exists');window.location.href='/show_data_user/'</script>")
