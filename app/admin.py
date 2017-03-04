from django.contrib import admin
from .models import Event,Center,Message,Citizen,Hospital,Copy,Victim,sms,Attacker
# Register your models here.
admin.site.register(Event)
admin.site.register(Center)
admin.site.register(Message)
admin.site.register(Citizen)
admin.site.register(Hospital)
admin.site.register(Copy)
admin.site.register(Victim)
admin.site.register(sms)
admin.site.register(Attacker)