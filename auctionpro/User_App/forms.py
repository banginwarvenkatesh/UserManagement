from django import forms
from .models import MyUser

gender = [('male','MALE'),('female','FEMALE'),('transgender','TRANSGENDER')]
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['user_contact'].required = True
        
    class Meta:
        model=MyUser
        fields = ['username','first_name', 'last_name', 'email','user_contact','gender','password','confirm_password', 'is_admin']

        labels = {
            'username':'USERNAME',
            'first_name': 'FRIST NAME',
            'last_name': 'LAST NAME',
            'email': 'EMAIL',
            'password':'PASSWORD',
            'confirm_password':'CONFIRM PASSWORD',
            'user_contact': 'CONTACT NUMBER',
            'gender': 'GENDER',
            'is_admin': 'REGISTER AS AUCTIONEER'
        }

        widgets = {
            'username':forms.TextInput(attrs={'placeholder':'eg. Bond007'}),
            'first_name':forms.TextInput(attrs={'placeholder':'eg. Joe'}),
            'last_name':forms.TextInput(attrs={'placeholder':'eg. Known'}),
            'email':forms.TextInput(attrs={'placeholder':'eg. Joe@xyz.com'}),
            'password':forms.TextInput(attrs={'placeholder':'eg. ******'}),
            'confirm_password':forms.TextInput(attrs={'placeholder':'eg. ******'}),
            'user_contact':forms.NumberInput(attrs={'placeholder':'eg. 9891929394'}),
            'gender': forms.RadioSelect(choices=gender)
        }
