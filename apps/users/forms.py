# -*- coding:utf-8 -*-
from django import forms
from captcha.fields import CaptchaField
from users.models import UserProfile

class LoginFrom(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True)


class RegisterFrom(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class UploadImageForm(forms.ModelForm):
    class Meta:
        model=UserProfile

        fields=['image']

class ChangepswFrom(forms.Form):
    password1=forms.CharField(required=True)
    password2=forms.CharField(required=True)
    password3=forms.CharField(required=True)

    def clean_password3(self):
        password3=self.cleaned_data['password3']
        password2=self.cleaned_data['password2']
        if password3 == password2:
            return password3
        else:
            raise forms.ValidationError(u"新密码不一致", code="psw_invalid")

class UserinfoForm(forms.ModelForm):
    class Meta:
        model=UserProfile

        fields=['birday','gender','nick_name','adress','mobile']