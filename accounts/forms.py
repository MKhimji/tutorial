from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext as _
from django.contrib.auth import password_validation





class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

##Had to add this from usercreationform documentation becauase the help_text for password1 field wasnt rendering correctly.
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Your password can't be too similar to your other personal information.Your password must contain at least 8 characters.Your password can't be a commonly used password.Your password can't be entirely numeric."


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password1', 'Re-enter password')
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


## class meta example : Got a photo its not describing the contents
## but rather the resolution and size, so describing the pictures
##properties rather than the image

##model = User is telling the RegistrationForm class
##to use the User model in django.contrib.auth.models
##and it's fields to create this custom registration form


    class Meta:
        model = User


        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',


        )



##remember that the user model only has the field username, passowrd1 and 2 defined so user only has to enter username
## an email as we have specified that it has to be required above and the two passwords



    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

##save is just a name
##every class method takes self as first argument
##commit=True  - Go ahead and save this data to the database
##commit = False - don't save the data onto the database yet as I have not yet finished
##editing the data i want to store in the model

##cleaned_data is a django function makes suredata is safe
##if commit: (whether we want to save the data or not.
##running.save runs the actual sql to store the data in the database

class EditProfileForm(forms.ModelForm):


    class Meta:
        model = User

        fields = (
            'email',
            'first_name',
            'last_name',

        )

## ChangePassword is a form that combines parts of setpasswordform and password change form so that i can customize andrender the errors
##  correctly

class ChangePassword(PasswordChangeForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].help_text = "Your password can't be too similar to your other personal information.Your password must contain at least 8 characters.Your password can't be a commonly used password.Your password can't be entirely numeric."
        self.fields['old_password'].help_text = "Enter current password"

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                self.add_error('new_password1','The two password fields didn\'t match')
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

        old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Current password"),
                                   widget=forms.PasswordInput)



    def clean_old_password(self):

        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


