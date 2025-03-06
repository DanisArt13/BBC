import email
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User, UserProfile

class UserLoginForm(AuthenticationForm): 
    
    class Meta:
        model = User
        fields = ["username", "password"]

    username=forms.CharField()
    password=forms.CharField()   
    
class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = (
        "username",
        "password1",
        "password2",
    )    
 
class UserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number'] 
        exclude = ['username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            if phone_number and len(phone_number) != 10:
                raise forms.ValidationError("Номер телефона должен содержать 10 цифр.")
            return phone_number
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'middle_name', 'profile_image']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),

        }
        
        def clean_age(self):
            age = self.cleaned_data.get('age')
            if age is not None and age < 0:
                raise forms.ValidationError("Возраст не может быть отрицательным.")
            return age

    