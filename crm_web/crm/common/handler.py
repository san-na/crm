# -*- coding: utf-8 -*-


import random
from IPython import embed
from datetime import datetime

from models import Customer, Admin, Group, Product, Opportunity
from crm import db
from crm import settings


# set utf-8 env
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)



class AdminCtl(object):
    """Admin
    实现对管理员的一些操作
    """

    @staticmethod
    def add(name, email, password):
        """添加管理员
    :param name: 用户名 :type: string.
    :param email: Email :type: string.
    :param password: 登录密码 :type: string.
    :return: : True
        """
        if not Admin.query.filter(Admin.email == email).first():
            admin = Admin(name, email, password)
            admin.save()
            return True
        else:
            return False

    @staticmethod
    def get_active():
        """获取active的用户
        """
        result = Admin.query.filter(Admin.status == '1').all()
        return result

    @staticmethod
    def delete(uid):
        """删除管理员
        """
        admin = Admin.query.filter(Admin.id == uid).first()
        if admin:
            admin.delete()
            return True

        return False

    @staticmethod
    def disable(uid):
        """禁用管理员
        """
        admin = Admin.query.filter(Admin.id == uid).first()
        if admin:
            admin.status = 2
            admin.update()
            return True
        return False


    @staticmethod
    def undisable(uid):
        """禁用管理员
        """
        admin = Admin.query.filter(Admin.id == uid).first()
        if admin:
            admin.status = 1
            admin.update()
            return True
        return False


    @staticmethod
    def login(email, password):
        """管理员登录
        当验证登录信息正确后，更新用户上次登录时间为系统当前时间

        :param email: Email :type: string.
        return: : Admin Obj
        """
        admin = Admin.query.filter(Admin.email == email).first()
        all_admin = Admin.query.all()
        try:
            assert all_admin != []
            # 管理员status若不为1，则表示不处于活跃状态，则不允许登录
            if admin and admin.status != '1':
                return None
            if admin and admin.check_password(password):
                admin.last_login = datetime.now()
                admin.update()
                return admin
        except:
            if not all_admin:
                admin = Admin('admin', email, password)
                admin.save()
                print '没有管理员，添加第一个管理员'
                return True
            print '找不到用户'

        return None

    @staticmethod
    def get(uid):
        """通过Email获取管理员
        :param email: uid : type:int
        :return: Admin Obj
        """
        admin = Admin.query.filter(Admin.id == uid).first()
        if admin:
            return admin

        return None

    @staticmethod
    def get_all():
        """获取所有管理员
        """
        return Admin.query.all()

    @staticmethod
    def update(**kwargs):
        """更新管理员信息
        :param
        :return: True
        """
        admin = Admin.query.filter(Admin.id == kwargs['uid']).first()
        name = kwargs['name']
        password = kwargs['password']
        reg_confirm = kwargs['reg_confirm']
        phone = kwargs['phone']
        status = kwargs['status']

        if name:
            admin.name = name
        if password:
            admin.set_password(password)
        if phone:
            admin.phone = phone
        if status:
            admin.status = status

        admin.update()
        return True

    @staticmethod
    def reset_password(email, password):
        """重置密码
        """
        admin = Admin.query.filter(Admin.email == email).first()
        admin.set_password(password)
        admin.updated = datetime.now()
        admin.save()
        return True


class CustomerCtl(object):
    """User
    实现对客户的一些操作
    """

    @staticmethod
    def add(name, sex, phone, email, company, addr, note, tax_id, uid):
        """添加客户
    :param name: 用户名 :type: string.
    :return: : True
        """
        customer = Customer(name, sex, phone, email, company, addr,
                note, tax_id, uid)
        customer.save()
        return customer

    @staticmethod
    def update_owner(uid, owner):
        """修改客户负责人
        """
        customer = Customer.query.filter(Customer.id == uid).first()
        if customer:
            customer.owner = owner
            customer.update()
            return True
        return False

    @staticmethod
    def get_all():
        """ 获取所有客户
        """
        result = Customer.query.all()
        return result

    @staticmethod
    def delete(uid):
        """删除客户
        """
        user = Customer.query.filter(Customer.id == uid).first()
        if user:
            user.delete()
            return True
        else:
            return False

    @staticmethod
    def get_by_id(uid):
        """通过uid获取客户
        """
        user = Customer.query.filter(Customer.id == uid).first()
        if user:
            return user
        return None

    @staticmethod
    def update(uid, name, sex, phone, email, company, addr, note, tax_id, owner):
        """ 更新客户信息
        """
        customer = Customer.query.filter(Customer.id == uid).first()

        if customer:
            customer.name = name
            customer.sex = sex
            customer.phone = phone
            customer.email = email
            customer.company = company
            customer.addr = addr
            customer.note = note
            customer.tax_id = tax_id
            customer.owner = owner
            customer.update()
            return True

        return None

    @staticmethod
    def reset_password(email, password):
        """重置用户密码
        """
        user = Customer.query.filter(Customer.email == email).first()
        user.set_password(password)
        user.updated = datetime.now()
        user.save()
        return True



class GroupCtl(object):
    """用户组控制器
    实现对用户组的一些操作
    """

    @staticmethod
    def get_all():
        """获取该管理员添加的所有用户组
        """
        group = Group.query.all()
        return group

    @staticmethod
    def add(uid, name, description=''):
        """添加客户组
        """
        group = Group.query.filter(Group.name == name).first()
        if group:
            group.name = name
            group.description = description
            group.modified_by = uid
            group.update()
        else:
            group = Group(name, description, uid, uid)
            group.save()
        return group

    @staticmethod
    def get(group_id):
        """获取顾客组
        """
        group = Group.query.filter(Group.id == group_id).first()
        return group

    @staticmethod
    def delete(group_id):
        """删除用户组
        """
        group = Group.query.filter(Group.id == group_id).first()
        if group:
            group.delete()
            return True
        return False


class ProductCtl(object):
    """产品控制器
    实现对产品的一些操作
    """

    @staticmethod
    def get_all():
        """获取所有产品
        """
        product = Product.query.all()
        return product

    @staticmethod
    def add(uid, name, description=''):
        """添加产品
        """
        product = Product.query.filter(Product.name == name).first()
        if product:
            product.name = name
            product.description = description
            product.modified_by = uid
            product.update()
        else:
            product = Product(name, description, uid, uid)
            product.save()
        return product

    @staticmethod
    def get(group_id):
        """获取产品
        """
        product = Product.query.filter(Product.id == group_id).first()
        return product

    @staticmethod
    def delete(group_id):
        """删除产品
        """
        product = Product.query.filter(Product.id == group_id).first()
        if product:
            product.delete()
            return True
        return False


class OpportunityCtl(object):
    """销售机会控制器

    """

    @staticmethod
    def get_all():
        """获取所有销售机会
        """
        opportunity = Opportunity.query.all()
        return opportunity

    @staticmethod
    def add(uid, name, description=''):
        """新增销售机会
        """
        opportunity = Opportunity.query.filter(Opportunity.name == name).first()
        if opportunity:
            opportunity.name = name
            opportunity.description = description
            opportunity.modified_by = uid
            opportunity.update()
        else:
            opportunity = Opportunity(name, description, uid, uid)
            opportunity.save()
        return opportunity

    @staticmethod
    def get(group_id):
        """获取销售机会
        """
        opportunity = Opportunity.query.filter(Opportunity.id == group_id).first()
        return opportunity

    @staticmethod
    def delete(group_id):
        """删除销售机会
        """
        opportunity = Opportunity.query.filter(Opportunity.id == group_id).first()
        if opportunity:
            opportunity.delete()
            return True
        return False
