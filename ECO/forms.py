# from .models import RegisterInfo
# from datetime import date
# from django import forms
#
# # class UserForm(forms.ModelForm):
# #     sex = forms.ChoiceField(
# #         required=False,
# #         label=u'性别',
# #         initial='male',
# #         choices=(('male','男'),('female','女'),('unknown','保密')),
# #         widget=forms.Select(),
# #         )
# #
# #     confirm_password = forms.CharField(
# #         required=True,
# #         label=u'确认密码',
# #         min_length=6,
# #         max_length=18,
# #         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
# #         )
# #
# #     class Meta:
# #         model = RegisterInfo
# #         fields = ['username', 'email', 'password', 'confirm_password', 'sex', 'birthday']
# #         labels = {'username':'用户名', 'email':'邮箱', 'password':'密码', 'confirm_password':'确认密码', 'sex':'性别', 'birthday': '出生日期'}
# #         widgets = {'password':forms.PasswordInput(), 'birthday': forms.SelectDateWidget()}
# #
# #     def clean_username(self):
# #         username = self.cleaned_data['username']
# #         if ' ' in username or '@' in username:
# #             raise forms.ValidationError(u'昵称中不能包含空格和@字符')
# #         res = RegisterInfo.objects.filter(username=username)
# #         if len(res) != 0:
# #             raise forms.ValidationError(u'此用户名已经注册，请重新输入')
# #         return username
# #
# #     def clean_email(self):
# #         email = self.cleaned_data['email']
# #         res = RegisterInfo.objects.filter(email=email)
# #         if len(res) != 0:
# #             raise forms.ValidationError(u'此邮箱已经注册，请重新输入')
# #         return email
# #
# #     def clean(self):
# #         cleaned_data = super(UserForm, self).clean()
# #         password = cleaned_data.get('password')
# #         confirm_password = cleaned_data.get('confirm_password')
# #         if password and confirm_password:
# #             if password != confirm_password:
# #                 raise forms.ValidationError(u'两次密码输入不一致，请重新输入')
#
# class RegisterForm(forms.Form):
#     username = forms.CharField(
#         required=True,
#         label=u'用户名',
#         max_length=20,
#         initial='',
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         )
#
#     email = forms.EmailField(
#         required=True,
#         label=u'邮箱',
#         max_length=25,
#         initial='',
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         )
#
#     password = forms.CharField(
#         required=True,
#         label=u'密码',
#         min_length=6,
#         max_length=18,
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         )
#
#     confirm_password = forms.CharField(
#         required=True,
#         label=u'确认密码',
#         min_length=6,
#         max_length=18,
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         )
#
#     sex = forms.ChoiceField(
#         required=False,
#         label=u'性别',
#         initial='male',
#         choices=(('male','男'),('female','女'),('unknown','保密')),
#         widget=forms.Select(),
#         )
#
#     birthday = forms.DateField(
#         required=False,
#         label=u'出生日期',
#         initial=date.today(),
#         widget=forms.SelectDateWidget(attrs={'class': 'form-control'}),
#         )
#
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if ' ' in username or '@' in username:
#             raise forms.ValidationError(u'昵称中不能包含空格和@字符')
#         res = RegisterInfo.objects.filter(username=username)
#         if len(res) != 0:
#             raise forms.ValidationError(u'此用户名已经注册，请重新输入')
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         res = RegisterInfo.objects.filter(email=email)
#         if len(res) != 0:
#             raise forms.ValidationError(u'此邮箱已经注册，请重新输入')
#         return email
#
#     def clean(self):
#         cleaned_data = super(RegisterForm, self).clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password and confirm_password:
#             if password != confirm_password:
#                 raise forms.ValidationError(u'两次密码输入不一致，请重新输入')
#
#     def save(self):
#         username = self.cleaned_data['username']
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']
#         sex = self.cleaned_data['sex']
#         birthday = self.cleaned_data['birthday']
#         RegisterInfo.objects.create(username=username, email=email, password= password, sex=sex, birthday=birthday).save()
#
# class UsernameLoginForm(forms.Form):
#     username = forms.CharField(
#         required=True,
#         label=u'用户名',
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#     )
#
#     password = forms.CharField(
#         required=True,
#         label=u'密码',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#     )
#
# class EmailLoginForm(forms.Form):
#     email = forms.EmailField(
#         required=True,
#         label=u'邮箱',
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#     )
#
#     password = forms.CharField(
#         required=True,
#         label=u'密码',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#     )