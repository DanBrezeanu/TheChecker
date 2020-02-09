from django import forms
from django.contrib.auth.models import User

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='',
        widget=forms.FileInput(attrs={'accept':'.cpp,.c'})
    )

    problemnumber = forms.IntegerField(
        label='Problem number',
        help_text=''
    )

class UserRegistration(forms.Form):
    username = forms.CharField(
        label = 'Username',
        help_text = '',
        max_length=20
    )

    email = forms.EmailField(
        label = 'Email',
        help_text = 'Email address'
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text = 'Password encrypted and salted with the pbkdf2_sha256 algorithm'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        help_text = 'Password encrypted and salted with the pbkdf2_sha256 algorithm'
    )

    def clean(self):
        users = User.objects.all()
        has_error = False

        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match'])
            self._errors['confirm_password'] = self.error_class(['Passwords do not match'])

            del cleaned_data['password']
            del cleaned_data['confirm_password']

            has_error = True

        if any([user.email == cleaned_data.get('email') for user in users]):
            self._errors['email'] = self.error_class(['Email already exists'])

            has_error = True

        
        if any([user.username == cleaned_data.get('username') for user in users]):
            self._errors['username'] = self.error_class(['Username already exists'])

            has_error = True

        if has_error:
            raise forms.ValidationError('Form not valid')

class ImageUpload(forms.Form):
    image = forms.ImageField(
        label='Select a file',
        help_text='',
        widget=forms.FileInput(attrs={'accept':'.jpg,.png,.jpeg,.svg,.gif,.bmp'})
    )