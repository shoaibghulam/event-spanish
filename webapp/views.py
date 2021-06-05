from django.shortcuts import render , HttpResponse , redirect
from django.views import View
from passlib.hash import django_pbkdf2_sha256 as handler
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import datetime 
import requests
from passlib.hash import django_pbkdf2_sha256 as handler
from webapp.models import *
import stripe
import json
import hashlib
from django.db.models import Sum
import random 
from django.http import JsonResponse
BASE="https://eventticket.pythonanywhere.com/"

# stripe testing key
stripe.api_key='sk_test_SD1VLYLcME6RYimXA3xxNKXW00eXfNnzuC'

def emailverify(subject,to,link,message):

    from_email="event@victoriadesafios.com"
        
        
    html_content = f'''
                <h1 style="text-align:center; font-family: 'Montserrat', sans-serif;">{message}</h1>
                    
                <div style='width:300px; margin:0 auto;'> <a href='{link}' style=" background-color:#0066ff; border: none;  color: white; padding: 15px 32px;  text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-family: PT Sans, sans-serif;" >click here to verify</a>
            </div>
                '''

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class index(View):
    def get(self,request):
        

       
        webdata = setting.objects.all()[0]
        request.session['title']=webdata.website_title
        request.session['desc']=webdata.website_description
        request.session['logo']=str(webdata.website_logo.url)
        data={
             'slider':slider.objects.all()[0],
              'data':Event.objects.all().order_by('-EventId')[0:3]
        }
        return render(request,'landing/index.html',data)
        # return render(request,'public/index.html',data)


class superadminlogin(APIView):
    def get(self,request):

        if  request.session.has_key('adminid'):
            return redirect("/superadmin")

        
        else:

            try:
                webdata = setting.objects.all()[0]
                request.session['title']=webdata.website_title
                request.session['desc']=webdata.website_description
                request.session['logo']=str(webdata.website_logo.url)
                return render(request ,'superadmin/login.html')

            except:

                return redirect("/superadminlogin")



    
    def post(self,request):

        try:
        
            SEmail = request.POST['SEmail']
            SPassword = request.POST['SPassword']
            fetchobj = Super_AdminAccount.objects.filter(SEmail = SEmail )
            if fetchobj and handler.verify(SPassword,fetchobj[0].SPassword):
                request.session['adminid'] =  fetchobj[0].SId
                request.session['adminname'] =  fetchobj[0].SFname + fetchobj[0].SLname 
                request.session['adminimg'] =  fetchobj[0].SProfile.url
                print(request.session['adminid'])
                messages.success(request,"Login Successfully")
                return redirect("/superadmin")


            else:
                messages.error(request,"Invalid Credientials")
                return redirect("/superadminlogin")

        except:
            return redirect("/superadminlogin")

class superadmin(View):
    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")

        try:
            user = User_Signup.objects.all().count()
            userregister = User_Event_Registration.objects.all().count()
            event = Event.objects.all().count()
            latestuser = User_Event_Registration.objects.all().order_by('-Registration_id')[0:1]
            eventlist = Event.objects.all().order_by('-EventId')[0:4]
            return render(request ,'superadmin/index.html',{'user':user,'userregister':userregister,'event':event,'latestuser':latestuser,'eventlist':eventlist})

        except:
            return redirect("/superadmin")


class superadminlogout(APIView):

    def get(self,request):

        try:
            del request.session['adminid']
            del request.session['adminname']
            del request.session['adminimg']
            return redirect('/superadminlogin')

        except:
            return redirect('/superadminlogin')


class superadminuser(View):
    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")

        try:

            data = User_Signup.objects.all()
            countuser = User_Signup.objects.all().count()
        
            return render(request ,'superadmin/user.html',{'data':data,'countuser':countuser})

        except:
            return redirect("/superadmin")


class superadminevent(View):
    def get(self,request):


        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")


        try:

            data = Event.objects.all()
        
            return render(request ,'superadmin/event.html',{'data':data})

        except:

            return redirect("/superadmin")

        
class superadminaddevent(View):
    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")


        try:

            data = Event_Type.objects.all()
        
            return render(request ,'superadmin/addevent.html',{'data':data})

        except:

            return redirect("/superadminevent")


    def post(self,request):

        try:

            EventName = request.POST['EventName']
            Cost = request.POST['Cost']
            Registration_start = request.POST['Registration_start']
            Registration_end = request.POST['Registration_end']
            Event_logo = request.FILES['Event_logo']
            Status = request.POST['Status']
            Description = request.POST['Description']
            EventTypeId = request.POST['EventTypeId']
            BuyLink = request.POST['buy_link']
            
            Super_AdminAccount_id = request.session['adminid']


            data = Event(EventName=EventName,Cost=Cost,Registration_start=Registration_start,Registration_end=Registration_end,Event_logo=Event_logo,Status=Status,Description=Description,EventTypeId = Event_Type.objects.get(EventTypeId=EventTypeId),distance=BuyLink)

            data.save()

            messages.success(request,"Add Successfully")
            return redirect("/superadminaddevent")

        except:
            return redirect("/superadminaddevent")


class admindeleteevents(APIView):

    def get(self,request):

        try:

            id = request.GET['id']
            data=Event.objects.filter(EventId=id)
            data.delete()
            messages.error(request,"Deleted Sucessfully")
            return HttpResponse("Delete")

        except:
            return redirect('/superadminevent')






class superadmineventtype(View):

    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")

        try:

            data = Event_Type.objects.all()
        
            return render(request ,'superadmin/eventtype.html',{'data':data})

        except:
            return redirect('/superadmin')


class superadminaddeventtype(APIView):
    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")


        else:
     
            return render(request ,'superadmin/addeventtype.html')

    def post(self,request):

        try:

            EventType = request.POST['EventType']
            
            Super_AdminAccount_id = request.session['adminid']

            checkevent = Event_Type.objects.filter(EventType = EventType )

            if checkevent:

                messages.error(request,"Event Already Exist")
                return redirect("/superadminaddeventtype")

            data = Event_Type(EventType=EventType,Super_AdminAccount_id=Super_AdminAccount.objects.get(SId = Super_AdminAccount_id))
            data.save()

            messages.success(request,"Add Successfully")
            return redirect("/superadminaddeventtype")

        except:
            return redirect("/superadminaddeventtype")

    


class editeventtype(APIView):

    def post(self,request):

        EventTypeId = request.POST['EventTypeId']
        EventType = request.POST['EventType']

        data = Event_Type.objects.get(EventTypeId = EventTypeId)

        data.EventType = EventType
        data.save()

        messages.success(request,"Edit Successfully")
        return redirect("/superadmineventtype")

        




class admindeleteevent(APIView):

    def get(self,request):

        try:

            id = request.GET['id']
            data=Event_Type.objects.filter(EventTypeId=id)
            data.delete()
            messages.error(request,"Deleted Sucessfully")
            return HttpResponse("Delete")

        except:
            return redirect('/superadminaddeventtype')



class superadminregister(View):
    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")

        try:

            data = User_Event_Registration.objects.all()
        
            return render(request ,'superadmin/register.html',{'data':data})

        except:
            return redirect("/superadmin")

class superadmintransition(View):
    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")

        try:
            
            data = Transactions.objects.all()
            return render(request ,'superadmin/transition.html',{'data':data})

        except:
            return redirect("/superadmin")


class eventview(View):
    def get(self,request,id):
        if not request.session.has_key('user_id'):
            return redirect("/clientlogin")

        data = Event.objects.get(EventId = id)
        return render(request,'userapp/viewevent.html',{'d':data})


    def post(self,request,id):

        if not request.session.has_key('user_id'):
            messages.error(request,"Please Create Account")
            return redirect(f'/eventview/{id}')

        try:
            price = request.POST['price']
            price = float(price)
           
            exp = request.POST['expiry']
            exp=exp.split('/')
            month=exp[0]
            year=exp[1]
            print("te price idfffffffffffffffffffffffffffffffffffffffffffffffffs ",price)
            cvc=request.POST['cvv']
            card=request.POST['number']
            createtoken = stripe.Token.create(
                        card={
                        "number": card,
                        "exp_month": int(month),
                        "exp_year":int(year) ,
                        "cvc": cvc,
                        },
                        )
            # price=2.253
            # price *=100
            # print("the price is ",price)
            charge = stripe.Charge.create(
                        amount = round(price)*100,
                        currency='usd',
                        description='Apointment created',
                        source = createtoken
                        )
            print("the charge is ",charge)
            if(charge['paid']==True):
                eventid=Event.objects.get(pk=id)
                userid=User_Signup.objects.get(pk=request.session['user_id'])
                reg_event=User_Event_Registration(user_id=userid,EventId=eventid)
                reg_event.save()
                order_data=Transactions(user_id= userid,event_id=eventid,order_id=charge['id'],totalAmount=price)
                order_data.save()
                messages.success(request,'Event has been register successfully')
                request.session['event_status']=True
                return redirect('/myevent')

        except stripe.error.CardError as e:
            messages.error(request,e.error.message)
            return redirect(f'/eventview/{id}')
            
   

class events(APIView):
    def get(self,request):
        if request.session.has_key('eventid'):
             del request.session['eventid']
        webdata = setting.objects.all()[0]
        request.session['title']=webdata.website_title
        request.session['desc']=webdata.website_description
        request.session['logo']=str(webdata.website_logo.url)
        if not request.session.has_key('user_id'):
            return redirect("/clientlogin")
        alreadyid=list()
        listed=User_Event_Registration.objects.filter(user_id= request.session['user_id'])
        for x in listed:
            alreadyid.append(x.EventId.EventId)

        eventlist = Event.objects.filter(~Q(pk__in=alreadyid)).order_by('-EventId')
        return render(request,'userapp/allevents.html',{'data':eventlist})


class contact(View):
    def get(self,request):
        return render(request,'landing/contact.html')
    
    def post(self,request):
        name= request.POST['name']
        email= request.POST['email']
        subject= request.POST['subject']
        comment= request.POST['comment']
        data=contact_us(contact_name=name,contact_email=email,contact_subject=subject,contact_comment=comment)
        data.save()
        messages.success(request,'Message has been sent')
        return redirect('contact')




class login(APIView):
    def get(self,request):
        return render(request,'public/signup.html')


        




class signup(APIView):
    def get(self,request):
        return render(request,'landing/signup.html')

    def post(self,request):

        Name = request.POST['Name']
        # Surname = request.POST['Surname']
        Ci = request.POST['Ci']
        Ruc = request.POST.get('Ruc','')
        Gender = request.POST['Gender']
        Phones = request.POST['Phones']
        Email = request.POST['Email']
        Direction = request.POST['Direction']
        City = request.POST['City']
        Birth_date = request.POST['Birth_date']
        Password = request.POST['Password']
        Password = handler.hash(Password)

        checkuser = User_Signup.objects.filter(Ci = Ci)
        if checkuser:

            messages.error(request,"CI already exists ")
            return redirect('/login')

        data = User_Signup(Name = Name, Ci=Ci,Ruc=Ruc,Gender=Gender,Phones=Phones,Email=Email,Direction=Direction,City=City,Birth_date=Birth_date,Password=Password)

        data.save()

        messages.success(request,"Signup Sucessfully")
        return redirect('/clientlogin')



        


        

        































































# supr admin update event
class superadmineditevent(APIView):
    def get(self,request,id):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")


        try:

     

            data = Event.objects.get(EventId = id)
            event_data = Event_Type.objects.all()
            
        
            return render(request ,'superadmin/editevent.html',{'data':data,'event_data':event_data})

        except:
            return redirect("/superadmin")

    def post(self,request,id):

        # try:

            EventName = request.POST['EventName']
            Cost = request.POST['Cost']
            Registration_start = request.POST['Registration_start']
            Registration_end = request.POST['Registration_end']
            Event_logo = request.FILES.get('Event_logo',False)
            Status = request.POST['Status']
            Description = request.POST['Description']
            EventTypeId = request.POST.get('EventTypeId')
            BuyLink = request.POST['buy_link']


            data = Event.objects.get(EventId = id)

            data.EventName = EventName
            data.Cost = Cost
            data.Registration_start = Registration_start
            data.Registration_end = Registration_end
            
            data.Status = Status
            data.Description = Description
            if EventTypeId:
                EventTypeId = Event_Type.objects.get(EventTypeId=EventTypeId)
                data.EventTypeId = EventTypeId
            data.distance = BuyLink

            if Event_logo:
                data.Event_logo = Event_logo


            data.save()

            messages.success(request,"Edit Successfully")
            return redirect("/superadminevent")

        # except:
        #     return redirect("/superadmin")









        
class superadmincontact(View):
    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")


        try:

            data = contact_us.objects.all()
        
            return render(request ,'superadmin/contact.html',{'data':data})

        except:

            return redirect("/superadminevent")



    
    
        
class superadmindelevent(View):
    def get(self,request,id):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")


        try:

            data = contact_us.objects.get(pk=id)
            data.delete()
            messages.success(request,"Message has been deleted")
            return redirect("superadmincontact")
            

        except:

            return redirect("/superadminevent")




class superadminsetting(View):
    def get(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")


        try:
            data = setting.objects.all()[0]
            data={
                'data':data,
                'slider':slider.objects.all().order_by('-pk')[0]
            }
            return render(request ,'superadmin/setting.html',data)

        except:

            return redirect("/superadminevent")


    def post(self,request):

        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")


        try:
            data = setting.objects.all()[0]
            data.website_title = request.POST['title']
            data.website_description= request.POST['desc']
            logo = request.FILES.get('logo')
            if logo:
                data.website_logo=logo
            data.save()
            
            messages.success(request,'Website Data has been updated')
            return redirect('superadminsetting')

        except:

            return redirect("/superadminevent")



    
    



class clientlogin(View):
    def get(self,request):
        webdata = setting.objects.all()[0]
        request.session['title']=webdata.website_title
        request.session['desc']=webdata.website_description
        request.session['logo']=str(webdata.website_logo.url)
        return render(request,'public/clientlogin.html')

    def post(self, request):
        try:
            
            Surname = request.POST['Surname']
            Password = request.POST['Password']
            fetchobj = User_Signup.objects.filter(Ci = Surname )
            if fetchobj and handler.verify(Password,fetchobj[0].Password):
                request.session['user_id'] =  fetchobj[0].user_id
                request.session['Surname'] =  fetchobj[0].Surname 
                request.session['name'] =  fetchobj[0].Name 
                checkevent=User_Event_Registration.objects.filter(user_id=fetchobj[0].user_id)
                if checkevent:
                    request.session['event_status']=True
                else:
                    request.session['event_status']=False

                messages.success(request,"Login Successfully")
                return redirect("/events")


            else:
                messages.error(request,"Invalid Credientials")
                return redirect("/clientlogin")

        except:
            return redirect("/clientlogin")


































































































































































































































































































































class myevent(View):
    def get(self, request):

        if not request.session.has_key('user_id'):
            return redirect("/clientlogin")

        try:
            if request.session.has_key('eventid'):
                del request.session['eventid']

            data = User_Event_Registration.objects.filter(user_id = request.session['user_id'])
            return render(request,'userapp/myevents.html',{'data':data})

        except:
            return redirect('/')

class eventapp(View):
    def get(self,request,id):
        webdata = setting.objects.all()[0]
        request.session['title']=webdata.website_title
        request.session['desc']=webdata.website_description
        request.session['logo']=str(webdata.website_logo.url)
        if not request.session.has_key('user_id'):
            return redirect("/clientlogin")

        try:

            data = Event.objects.get(EventId = id)
            request.session['eventid'] = id
            request.session['distance'] = data.distance
            print(request.session['eventid'])
            return render(request,'userapp/index.html',{'data':data}) 

        except:

            return redirect('/events')


class uploadprogress(View):
    def get(self,request):

        if not request.session.has_key('user_id'):
            return redirect("/clientlogin")

        return render(request,'userapp/uploadprogress.html') 

    def post(self,request):

        try:
            
            EventId = request.session['eventid']

            
            user_id = request.session['user_id']
            date = request.POST['date']
            hour = request.POST['HH']
            mint = request.POST['MM']
            second = request.POST['SS']
            time =f"{hour}:{mint}:{second}"
            weight = request.POST['weight']
            fulltime=datetime.datetime.strptime(time, '%H:%M:%S')
            # print("the full time is===========> ",fulltime)
            # running_point = request.POST['running_point']
            weather = request.POST['weather']

            

            eventobj = Event.objects.get(EventId = EventId) 
            user_obj = User_Signup.objects.get(user_id = user_id) 

            data = event_progress(EventId = eventobj,user_id= user_obj,date=date,time=fulltime,weight=weight,meter=weather)

            data.save()

            messages.success(request,"Progress Upload Successfully")
            return redirect('/Progress')
           

        except:

            return redirect('/events')




class Progress(APIView):

    def get(self,request):

        if not request.session.has_key('user_id'):
            return redirect("/clientlogin")

        try:
            data = event_progress.objects.filter(user_id = request.session['user_id'],EventId=request.session['eventid']).order_by('-pk')[0]
            userdata=User_Signup.objects.get(pk=request.session['user_id'])
            year = datetime.date.today().year
            age= year- userdata.Birth_date.year
            #calories burned = distance run (kilometres) x weight of runner (kilograms) x 1.036
            kcal=(data.meter/1000) * data.weight *1.036
            print("mune year",kcal)



            data={
                'kcal':kcal
            }
            # return HttpResponse("weatherlist")

            return render(request,"userapp/progress.html",data)
        except:
            messages.success(request,'Please Upload Progress')
            return redirect('uploadprogress')









































class adminslider(View):
    def post(self, request):
        if not request.session.has_key('adminid'):
            return redirect("/superadminlogin")
    

        # try:





    
        data=slider.objects.get(pk=request.POST['pk'])
       
        data.title=request.POST['title']
        data.desc=request.POST['btnname']
        data.button_name=request.POST['btnlink']
        data.button_link=request.POST['desc']
        back=request.FILES.get('back')
        if back:
             data.background=back
        thumb = request.FILES.get('thumb')
        if thumb:
              data.front_img=thumb
        # data= slider(slider_first_word=fword,slider_second_word=sword,slider_description=desc,slider_thumb=thumb)
        data.save()
        messages.success(request,'Slider has been Update Successfully')
        return redirect('superadminsetting')

        # except:

        #     return redirect("/superadminevent")






class clientlogout(APIView):

    def get(self,request):

        try:
            del request.session['user_id']
            del request.session['Surname']
          
            return redirect('/')

        except:
            return redirect('/')



class leaderboard(View):
    
    def get(self,request):
        if not request.session.has_key('user_id'):
            return redirect("/clientlogin")
        return render(request,'userapp/leaderboard.html')

class leaderboarddata(View):
    def get(self, request):
        if not request.session.has_key('user_id'):
            return redirect("/clientlogin")
        alldata=list()
        # data= event_progress.objects.order_by().values('user_id__Name','meter','weight').distinct()
        # data= event_progress.objects.filter(EventId=request.session['eventid']).order_by('-pk')
        # data=event_progress.objects.filter(EventId=request.session['eventid']).aggregate(Sum('meter'))
        data=event_progress.objects.filter(EventId=request.session['eventid']).values('user_id','user_id__Name','EventId__distance').annotate(meter=Sum('meter')).order_by('-user_id')
        for x in data:
            # print(x)
            alldata.append(x)
        print("mune data haydda a",alldata)
        # for x in data:
        #     if not x.user_id.user_id in alldata:
        #         alldata.append(x)
        # print(alldata)
        # print("the data is ",alldata)
        # serdata= serProgress(data, many=True)
        # x=f"[{data}]"
        return HttpResponse(json.dumps(alldata))








class userprogress(View):
    def get(self, request):
        totlrun=event_progress.objects.filter(user_id=request.session['user_id']).aggregate(Sum('meter'))
        data = event_progress.objects.filter(user_id = request.session['user_id'],EventId=request.session['eventid']).order_by('-pk')
        serdata=serProgress(data, many=True)
        print(request.session['distance'])
        alldata ={
            'data':serdata.data, 
            'totalrun':totlrun,
            'eventdistance': request.session['distance'],
        }
        print("the sum is here ====>?",alldata)
        return HttpResponse(json.dumps(alldata))














class pagopar(View):
    def get(self , request):
        # hash_object = hashlib.sha1(b'HelWorld')


        # comerce tokens (I will provide that)
        hash = hashlib.sha1()
        tokenPrivado='776f01c35b6cf70a0bc62a15a5cb0513'
        tokenPublico='84898c14f223ce9cee2d21eb34b327f3'

        # build the token to get the payment method, 
        # you have to cancatenate the private token with FORMA-PAGO
        # token = tokenPrivado+'1'
        order_id='p33'
        price=33.3
        token = tokenPrivado+order_id+str(price)
        # print("the token is now ",token)
# echo sha1($data.$orderID.$j);
        #concatenate this to make a sha1
        hash.update(str(token).encode('utf-8'))
        print("the hash is ",hash.hexdigest())
# /        sha1 ($ data [ ' private_token_trade ' ]. $ orderID. strval (floatval ($ j [ 'total_amount' ])));


        # for the example, payment methods are listed
        url = 'https://api.pagopar.com/api/comercios/1.1/iniciar-transaccion'
        # url = f'https: //www.pagopar.com/pagos/{hash.hexdigest()}?forma_pago=1'
        # return redirect(url)
        # url = ' https://api.pagopar.com/api/comercios/1.1/iniciar-transaccion/'

        # data you send to pagopar
        data ={
            "token": hash.hexdigest(),
            # "token_publico": tokenPublico
        }

        # set header jason tipe
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        # make petition
        req = requests.post(url, data=json.dumps(data), headers=headers)

        # print data
        print("the result of json is ",req.json())

        return HttpResponse("doe")

class forgotpassword(View):
    def get(self,request):
        return render(request,'userapp/forgot.html')

    def post(self,request):
        tk=  rand_token =random.randint(1,5000)
        ci=request.POST['ci']
        try:
            data=User_Signup.objects.get(Ci=ci)
            if data:
                data.Token=tk
                link=f"{BASE}forget/{ci}/{tk}"
                msg="Rest Password"
                emailverify("Forget password",data.Email,link,msg)
                data.save()
                messages.success(request,"A Reset link has been sent")
             
                return redirect('/clientlogin')
        except:
                messages.success(request,"Please Enter Correct Ci")
                return redirect('/forgotpassword')


class forget(View):
    def get(self, request,username,token):
        try:
            data=User_Signup.objects.get(Ci=username,Token=token)
            if data:
                return render(request,'userapp/reset.html',{'data':data})
        except:
             messages.success(request,'Token has been expire')
             return redirect('/clientlogin')
        

    def post(self, request,username,token):
       
        password= handler.hash(request.POST['password'])

      
        data=User_Signup.objects.get(Ci=username,Token=token)
        tk= random.randint(1,5000)
        if data:
            data.Password=password
            data.Token=tk
            data.save()
            messages.success(request,"Password has been Changed")
            return redirect("/clientlogin")
    






