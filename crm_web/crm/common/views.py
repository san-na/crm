# -*- coding: utf-8 -*-

import os, re
from flask import render_template, redirect, url_for, flash, jsonify, request, abort
from datetime import datetime
from IPython import embed
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from time import time

from crm.common import Common
from crm import settings, login_manager
from handler import CustomerCtl, AdminCtl, GroupCtl, ProductCtl, OpportunityCtl
from forms import LoginForm, RegistrationForm, AdminProfileForm, ResetPasswordForm, AddCustomerForm,\
            DataImportForm, EditCustomerForm, AdminAddForm, CustomerFllowForm, GroupAddForm, GroupEditForm,\
            ProductAddForm, OpportrunityAddForm
import utils

@login_manager.user_loader
def load_user(userid):
    return AdminCtl.get(userid)


@Common.route('/')
def index():
    """
    首页
    """
    if current_user.is_authenticated:
        kwargs = {
            'total_customer': len(CustomerCtl.get_all()),
            'total_group': len(GroupCtl.get_all()),
            'total_admin': len(AdminCtl.get_all()),
            'total_product': len(ProductCtl.get_all())

        }
        return render_template('index.html', **kwargs)

    else:
        print '没有登录'
        return redirect(url_for('Common.login'))


@Common.route('/login', methods=('GET', 'POST'))
def login():
    """
    管理员登录
    """
    login_form = LoginForm()
    registration_form = RegistrationForm()

    if login_form.validate_on_submit():
        email = utils.strip_lower(login_form.data['login_email'])
        password = utils.strip_lower(login_form.data['login_password'])
        admin = AdminCtl.login(email, password)

        if admin:
            login_user(admin)
            flash(u'登录成功！', 'success')
        else:
            flash(u'用户名或密码错误', 'error')

        return redirect(url_for('Common.index'))

    for _, errors in login_form.errors.items():
        for error in errors:
            flash(error, 'error')

    kwargs ={
        'login_form': login_form,
        'registration_form': registration_form
        }
    return render_template('login.html', **kwargs)


@Common.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """管理员退出登录
    """
    logout_user()
    flash(u'退出登录成功', 'info')
    return redirect(url_for('Common.login'))


@Common.route('/account_management', methods=['GET', 'POST'])
@login_required
def account_management():
    """
    账号管理
    """
    users = CustomerCtl.get_all_child(current_user.id)

    kwargs = {
        'users': users
    }

    return render_template("account_management.html", **kwargs)


@Common.route('/permission_setting', methods=['GET', 'POST'])
@login_required
def permission_setting():
    """
    权限设置
    """
    kwargs = {

    }
    return render_template("permission_setting.html", **kwargs)


@Common.route('/user_setting', methods=['GET', 'POST'])
@login_required
def user_setting():
    """
    用户管理
    """

    action = request.args.get('action', '')

    admins = AdminCtl.get_all()

    if action == 'add':
        form = AdminAddForm()
        kwargs = {
            'form': form
        }
        if form.validate_on_submit():
            email = form.data['email']
            name = form.data['name']
            password = form.data['password']
            if AdminCtl.add(name, email, password):
                flash(u'添加成功', 'success')
                return redirect(url_for('Common.user_setting'))
        return render_template('user_add.html', **kwargs)
    elif action == 'delete':
        uid = request.args.get('uid', '0')
        if AdminCtl.delete(uid):
            flash(u'删除成功', 'success')
        else:
            flash(u'删除失败', 'error')
        return redirect(url_for('Common.user_setting'))

    kwargs = {
        'admins': admins,
        'STATUS_LIST': settings.CUSTOMER_STATUS_DICT
    }

    return render_template('user_settings.html', **kwargs)


@Common.route('/order_management', methods=['GET', 'POST'])
@login_required
def order_management():
    """
    订单管理
    """

    return render_template('order_management.html')


@Common.route('/opportunity/<action>', methods=['GET', 'POST'])
@login_required
def opportunity(action):
    """
    销售机会管理
    """

    if action =='add':
        form = OpportrunityAddForm()
        if form.validate_on_submit():
            next_contacts = form.data['next_contacts']
            name = form.data['name']
            source = form.data['source']
            if OpportunityCtl.add(name, next_contacts, source):
                flash(u'操作成功', 'success')
            else:
                flash(u'操作失败', 'error')
            return redirect(url_for('Common.opportunity', action='list'))
        kwargs = {
            'form': form,
            'sources': settings.OPPORTUNITY_SOURCE_DICT,
            'owner_dict': AdminCtl.get_all()
        }
        return render_template('opportunity_add.html', **kwargs)

    if action == 'delete':
        opportunity_id = request.args.get('opportunity_id', '')
        result = OpportunityCtl.delete(opportunity_id)
        if result:
            flash(u'操作成功', 'success')
        else:
            flash(u'操作失败', 'error')
        return redirect(url_for('Common.opportunity', action='list'))
    if action == 'list':
        result = OpportunityCtl.get_all()
        owner_dict = {}
        for i in result:
            try:
                owner_dict[i.next_contacts] = AdminCtl.get(i.next_contacts).name
            except:
                # 如果用户被删除，则AdminCtl.get可能引发异常
                pass
        kwargs = {
            'result': result,
            'owner_dict': owner_dict,
            'source_dict': settings.OPPORTUNITY_SOURCE_DICT
        }


        return render_template('opportunity.html', **kwargs)
    return render_template("404.html")

@Common.route('/system_settings', methods=['GET', 'POST'])
@login_required
def system_settings():
    """
    系统设置
    """
    return render_template('system_settings.html')


@Common.route('/customer/delete', methods=["GET"])
@login_required
def customer_delete():
    """删除客户
    """
    uid = request.args.get('uid', '0')
    user = CustomerCtl.delete(uid)
    if user:
        flash(u'删除成功', 'success')
    else:
        flash(u'客户不存在', 'error')
    return redirect(url_for('Common.customer', action='list'))


@Common.route('/admins/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    """管理员信息
    """
    form = AdminProfileForm()


    if form.validate_on_submit():
        kwargs = {
            'uid': form.data['uid'],
            'name': form.data['name'],
            'password': form.data['password'],
            'reg_confirm': form.data['reg_confirm'],
            'phone': form.data['phone'],
            'status': form.data['status']
            }
        name = form.data['name']
        if name and len(name) < 2 or len(name)  > 26:
            flash(u'用户名长度长度必须在2~25之间', 'error')
            return redirect(url_for('Common.admin_profile'))
        if AdminCtl.update(**kwargs):
            flash(u'信息更新完成', 'success')
        return redirect(url_for('Common.user_setting'))
    for _, errors in form.errors.items():
        for error in errors:
            print errors
            flash(error, 'error')


    uid = request.args.get('uid', '')
    user = AdminCtl.get(uid)
    form.name.data = user.name
    form.status.data = user.status
    form.phone.data = user.phone
    form.uid.data = user.id
    kwargs ={
        'form': form
    }

    return render_template("user_profile.html", **kwargs)


@Common.route('/user_disable', methods=['GET', 'POST'])
@login_required
def user_disable():
    """禁用用户
    """
    uid = request.args.get('uid', '')

    if uid == str(current_user.id).decode('utf-8'):
        flash(u'不运行操作当前登录用户', 'warning')
    elif AdminCtl.disable(uid):
        flash(u'操作成功', 'success')
    else:
        flash(u'操作失败', 'error')
    return redirect(url_for('Common.user_setting'))


@Common.route('/user_undisable', methods=['GET', 'POST'])
@login_required
def user_undisable():
    """禁用用户
    """
    uid = request.args.get('uid', '')
    if uid == str(current_user.id).decode('utf-8'):
        flash(u'不运行操作当前登录用户', 'warning')
    elif AdminCtl.undisable(uid):
        flash(u'操作成功', 'success')
    else:
        flash(u'操作失败', 'error')
    return redirect(url_for('Common.user_setting'))


@Common.route('/customer_follow_up', methods=['GET', 'POST'])
@login_required
def customer_follow_up():
    """客户跟进
    """
    customer_id = request.args.get('customer_id', '')
    form = CustomerFllowForm()
    owners = AdminCtl.get_active()
    if form.validate_on_submit():
        customer_id = form.data['customer_id']
        owner = form.data['owner']
        if CustomerCtl.update_owner(customer_id, owner):
            flash(u'修改成功', 'success')
        else:
            flash(u'修改失败', 'error')
        return redirect(url_for('Common.customer', action='list'))
    form.customer_id.data = customer_id
    kwargs = {
        'customer_id': customer_id,
        'form': form,
        'owners': owners
        }
    return render_template('customer_follow_up.html', **kwargs)


@Common.route('/group/<action>', methods=['GET', 'POST'])
@login_required
def group(action):
    """group
    """
    if action =='add':
        form = GroupAddForm()
        if form.validate_on_submit():
            name = form.data['name']
            description = form.data['description']
            if GroupCtl.add(current_user.id, name, description):
                flash(u'操作成功', 'success')
            else:
                flash(u'操作失败', 'error')
        kwargs = {
            'form': form
        }
        return render_template('customer_group_add.html', **kwargs)
    if action == 'edit':
        group_id = request.args.get('group_id', '')
        group = GroupCtl.get(group_id)
        form = GroupEditForm()
        if group:
            form.group_id.data = group.id
            form.name.data = group.name
            form.description.data = group.description
        kwargs = {
            'form': form
        }
        return render_template('customer_group_add.html', **kwargs)
    if action == 'delete':
        group_id = request.args.get('group_id', '')
        group = GroupCtl.delete(group_id)
        if group:
            flash(u'操作成功', 'success')
        else:
            flash(u'操作失败', 'error')
        return redirect(url_for('Common.group', action='list'))
    if action == 'list':
        groups = GroupCtl.get_all()
        owner_dict = {}
        for i in groups:
            try:
                owner_dict[i.owner] = AdminCtl.get(i.owner).name
            except:
                # 如果用户被删除，则AdminCtl.get可能引发异常
                pass
        kwargs = {
            'groups': groups,
            'owner_dict': owner_dict
        }

        return render_template('customer_group.html', **kwargs)
    return render_template("404.html")


@Common.route('/customer/<action>', methods=['GET', 'POST'])
@login_required
def customer(action):
    """
    用户列表
    """
    if action == 'add':
        form = AddCustomerForm()
        if form.validate_on_submit():
            name = form.data['name']
            sex = form.data['sex']
            phone = form.data['phone']
            email = form.data['email']
            company = form.data['company']
            addr = form.data['addr']
            note = form.data['note']
            tax_id = form.data['tax_id']
            CustomerCtl.add(name, sex, phone, email, company, addr,
                    note, tax_id, current_user.id)
            flash(u'添加成功', 'success')
            return redirect(url_for('Common.customer', action='list'))
        return render_template('customer_add.html', form=form)
    if action == 'edit':
        form = EditCustomerForm()
        if form.validate_on_submit():
            uid = form.data['uid']
            name = form.data['name']
            sex = form.data['sex']
            phone = form.data['phone']
            email = form.data['email']
            company = form.data['company']
            addr = form.data['addr']
            note = form.data['note']
            tax_id = form.data['tax_id']
            customer = CustomerCtl.update(uid, name, sex, phone, email, company, addr,
                    note, tax_id, current_user.id)
            if customer:
                flash(u'编辑成功', 'success')
            else:
                flash(u'编辑失败', 'error')
            return redirect(url_for('Common.customer', action='list'))
        uid = request.args.get('uid', '0')
        customer = CustomerCtl.get_by_id(uid)
        if customer:
            form.uid.data = customer.id
            form.name.data = customer.name
            form.sex.data = customer.sex
            form.phone.data = customer.phone
            form.email.data = customer.email
            form.company.data = customer.company
            form.addr.data = customer.addr
            form.note.data = customer.note
            form.tax_id.data = customer.tax_id
        else:
            flash(u'找不到该客户', 'error')
            return redirect(url_for('Common.customer', action='list'))
        return render_template('customer_edit.html', form=form)

    if action == 'list':
        result = CustomerCtl.get_all()
        owner_dict = {}
        for i in result:
            try:
                owner_dict[i.owner] = AdminCtl.get(i.owner).name
            except:
                # 如果用户被删除，则AdminCtl.get可能引发异常
                pass

        kwargs = {
            'result': result,
            'STATUS_LIST': settings.CUSTOMER_STATUS_DICT,
            'owner_dict': owner_dict
        }

        return render_template("customer.html", **kwargs)
    return render_template("404.html")




@Common.route('/product/<action>', methods=['GET', 'POST'])
@login_required
def product(action):
    """product
    """
    if action =='add':
        form = ProductAddForm()
        if form.validate_on_submit():
            name = form.data['name']
            description = form.data['description']
            if ProductCtl.add(current_user.id, name, description):
                flash(u'操作成功', 'success')
            else:
                flash(u'操作失败', 'error')
            return redirect(url_for('Common.product', action='list'))
        kwargs = {
            'form': form
        }
        return render_template('product_add.html', **kwargs)
    if action == 'delete':
        pid = request.args.get('pid', '')
        if ProductCtl.delete(pid):
            flash(u'操作成功', 'success')
        else:
            flash(u'操作失败', 'error')
        return redirect(url_for('Common.product', action='list'))

    if action == 'list':

        products = ProductCtl.get_all()

        owner_dict = {}
        for i in products:
            try:
                owner_dict[i.owner] = AdminCtl.get(i.owner).name
            except:
                # 如果用户被删除，则AdminCtl.get可能引发异常
                pass
        kwargs = {
            'products': products,
            'owner_dict': owner_dict
        }

        return render_template('product.html', **kwargs)
    return render_template("404.html")
