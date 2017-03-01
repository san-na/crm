# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, validators, SubmitField,\
    BooleanField, HiddenField, TextAreaField, RadioField, SelectMultipleField,\
     SelectField, DateField
from wtforms.fields.html5 import EmailField

from crm import settings

class LoginForm(FlaskForm):
    login_email = EmailField('Email', validators=[validators.DataRequired()])
    login_password = PasswordField('password', validators=[validators.DataRequired()])
    login_submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    reg_username = StringField('Username', [validators.Length(min=2, max=25, message=u'用户名长度必须为2~25')])
    reg_email = EmailField('Email Address', [validators.Length(min=4, max=35, message=u'邮箱长度必须为4~35')])
    reg_password = PasswordField('New Password', [
        validators.EqualTo('reg_confirm', message=u'密码不一致')
    ])
    reg_confirm = PasswordField('Repeat Password')
    reg_submit = SubmitField("Register")


class AdminAddForm(FlaskForm):
    name = StringField('name')
    email = EmailField('email')
    password = PasswordField('password')
    submit = SubmitField('add')


class AdminProfileForm(FlaskForm):
    uid = HiddenField('uid')
    name = StringField('Name', [validators.Length(min=2, max=25, message=u'用户名长度必须为2~25')])
    password = PasswordField('New Password', [
        validators.EqualTo('reg_confirm', message=u'密码不一致')
    ])
    status = StringField('status')
    reg_confirm = PasswordField('Repeat Password')
    phone = StringField('Phone')


class ResetPasswordForm(FlaskForm):
    token = HiddenField('token')
    password = PasswordField('New Password', [
        validators.EqualTo('reg_confirm', message=u'密码不一致')
    ])
    reg_confirm = PasswordField('Repeat Password')
    submit = SubmitField("提交")


class AddCustomerForm(FlaskForm):
    name = StringField('姓名')
    sex = StringField('性别')
    phone = StringField('电话')
    email = StringField('email')
    company = StringField('公司')
    addr = TextAreaField('地址')
    note = TextAreaField('备注')
    tax_id = StringField('税号')
    submit = SubmitField("添加")


class EditCustomerForm(FlaskForm):
    uid = HiddenField('uid')
    name = StringField('姓名')
    sex = StringField('性别')
    phone = StringField('电话')
    email = StringField('email')
    company = StringField('公司')
    addr = TextAreaField('地址')
    note = TextAreaField('备注')
    tax_id = StringField('税号')
    submit = SubmitField("添加")


class UserProfileUpdateForm(FlaskForm):
    uid = HiddenField('uid')
    username = StringField('username', [validators.Length(min=1, max=100, message=u'用户名长度必须为1~100')])
    email = EmailField('Email Address')
    status = RadioField('Label', coerce=int, choices=[(1, 'Active'), (2, 'Bypass'), (3, 'Disable')], default=1)
    group = StringField('group')
    note = TextAreaField('note')
    submit = SubmitField("保存修改")


class DataImportForm(FlaskForm):
    csv_file = FileField('csv_file', validators=[
        FileAllowed(['csv'], u'只允许上传csv文件!')
    ])
    submit = SubmitField('Upload')


class CustomerFllowForm(FlaskForm):
    customer_id = HiddenField('customer_id')
    owner = StringField('owner')
    submit = SubmitField('添加')


class GroupAddForm(FlaskForm):
    name = StringField('组名')
    description = TextAreaField('描述')
    submit = SubmitField('添加')


class GroupEditForm(FlaskForm):
    group_id = HiddenField('group_id')
    name = StringField('组名')
    description = TextAreaField('描述')
    submit = SubmitField('添加')


class ProductAddForm(FlaskForm):
    name = StringField('产品名')
    description = TextAreaField('描述')
    submit = SubmitField('添加')


class OpportrunityAddForm(FlaskForm):
    source = StringField('source')
    name = StringField('name')
    next_contacts = StringField('next_contacts')
    submit = SubmitField('添加')
