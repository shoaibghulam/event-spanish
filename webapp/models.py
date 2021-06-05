from django.db import models
from rest_framework import serializers
# Create your models here.
STATUS=(
    ('Active','Active'),
    ('Disable','Disable'),
)

PAYMENT=(
    ('Pending','Pending'),
    ('Paid','Paid'),
    ('Unpaid','Unpaid'),
)
class Super_AdminAccount(models.Model):

    SId = models.AutoField(primary_key=True)
    SFname=models.CharField(max_length=100, default="First Name")
    SLname=models.CharField(max_length=100, default="Last Name")
    SEmail=models.CharField(max_length=100, default="Email Name")
    SUsername=models.CharField(max_length=100, default="Username ")
    SPassword=models.TextField(max_length=3000, default="Password ")
    SContactNo=models.CharField(max_length=100, default="Contact no")
    SProfile= models.ImageField(upload_to='SuperAdmin/',default="SuperAdmin/dummy.jpg")
    def __str__(self):
        return self.SFname


class Event_Type(models.Model):
    EventTypeId = models.AutoField(primary_key=True)
    EventType = models.CharField(max_length=255, default="")
    Super_AdminAccount_id=models.ForeignKey(Super_AdminAccount , on_delete=models.SET_NULL,blank=True,null=True)


    def __str__(self):
        return self.EventType

class Event(models.Model):
    EventId = models.AutoField(primary_key=True)
    EventName = models.CharField(max_length=255, default="")
    Cost = models.FloatField(default=0.0)
    Registration_start = models.DateField()
    Registration_end = models.DateField()
    Runner_quantity = models.IntegerField(default=0)
    Event_logo = models.ImageField(upload_to='Eventlogo/',default="SuperAdmin/dummy.jpg")
    Status = models.CharField(max_length=50, default="")
    EventTypeId = models.ForeignKey(Event_Type , on_delete=models.SET_NULL,blank=True,null=True)
    Description = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True, blank=True)
    distance=models.FloatField(default="")

    
    def __str__(self):
        return self.EventName


class User_Signup(models.Model):
    user_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, default="")
    Surname = models.CharField(max_length=255, default="")
    Ci = models.CharField(max_length=255, default="")
    Ruc = models.CharField(max_length=255, default="")
    Gender = models.CharField(max_length=20, default="")
    Phones = models.CharField(max_length=20, default="")
    Email = models.EmailField(max_length=255, default="")
    Direction = models.CharField(max_length=255, default="")
    City =  models.CharField(max_length=255, default="")
    Birth_date  = models.DateField()
    Creation = models.DateTimeField(auto_now_add=True, blank=True)
    Password = models.TextField(max_length=500 , default="")
    Token = models.CharField(max_length=40, default="")


    def __str__(self):
        return self.Name


class User_Event_Registration(models.Model):
    Registration_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User_Signup , on_delete=models.SET_NULL,blank=True,null=True)
    EventId = models.ForeignKey(Event , on_delete=models.CASCADE ,blank=True,)
    Description = models.CharField(max_length=255, default="")
    created = models.DateTimeField(auto_now_add=True, blank=True)
    status =models.CharField(max_length=100, choices=STATUS , default="Disable")

   


class Transactions(models.Model):
    Transaction_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User_Signup , on_delete=models.SET_NULL,blank=True,null=True)
    event_id= models.ForeignKey(Event , on_delete=models.SET_NULL,blank=True,null=True)
    order_id = models.CharField(max_length=255, default="")
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    totalAmount = models.FloatField(default=0.0)
    status =models.CharField(max_length=100, choices=PAYMENT , default="Pending")
    
  
  





class event_progress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    EventId = models.ForeignKey(Event , on_delete=models.SET_NULL,blank=True,null=True)
    user_id = models.ForeignKey(User_Signup , on_delete=models.SET_NULL,blank=True,null=True)
    meter = models.FloatField( default=0 , null=True)
    date = models.DateField()
    time = models.TimeField()
    weight = models.FloatField(default=0.0)
    running_point =models.IntegerField(default=0)
    

    

class contact_us(models.Model):
    contact_id= models.AutoField(primary_key=True)
    contact_name= models.CharField(max_length=100)
    contact_email= models.EmailField(max_length=100)
    contact_subject=models.CharField(max_length=100)
    contact_comment= models.TextField(max_length=1000)
    contact_date= models.DateField(auto_now_add=True, null=True)
    # contact_mark=models.CharField(max_length=2,default="0")

    

    def __str__(self):
        return self.contact_name


class setting(models.Model):
    setting_id=models.AutoField(primary_key=True)
    website_title=models.CharField(max_length=100)
    website_description=models.CharField(max_length=256)
    website_logo = models.ImageField(upload_to='Eventlogo/',default="SuperAdmin/dummy.jpg")

    def __str__(self):
        return self.website_title
        

class slider(models.Model):
    slider_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    button_name=models.CharField(max_length=256)
    button_link=models.CharField(max_length=256)
    background = models.ImageField(upload_to='slider/',default="SuperAdmin/dummy.jpg")
    front_img = models.ImageField(upload_to='slider/',default="SuperAdmin/dummy.jpg")
    front_img_two = models.ImageField(upload_to='slider/',default="SuperAdmin/dummy.jpg")

    def __str__(self):
        return self.title




# serilizer 


class serUserSignUp(serializers.ModelSerializer):
  
    class Meta:
        model = User_Signup 
        fields='__all__'

        
class serProgress(serializers.ModelSerializer):
    user_id=serUserSignUp()
    class Meta:
        model = event_progress 
        fields='__all__'