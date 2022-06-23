from django.contrib import admin
from .models import Country, State, City, Address, MyUser, IdProof

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(MyUser)
admin.site.register(IdProof)

# Register your models here.
