# coding: utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser
import time
# from jasset.models import Asset, AssetGroup

DEPT_TYPE_CHOICES = (
        ('1', 'comp'),
        ('2', 'dept'),

)

class Dept(models.Model):
    name=models.CharField(max_length=80,unique=True)
    parent=models.ForeignKey("self", blank=True, null=True, related_name="children")
    type=models.CharField(max_length=2, choices=DEPT_TYPE_CHOICES, default='CU')

class UserGroup(models.Model):
    name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('SU', 'SuperUser'),
        ('GA', 'GroupAdmin'),
        ('CU', 'CommonUser'),
    )
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=100)
    role = models.CharField(max_length=2, choices=USER_ROLE_CHOICES, default='CU')
    group = models.ManyToManyField(UserGroup)
    ssh_key_pwd = models.CharField(max_length=200)
    # is_active = models.BooleanField(default=True)
    # last_login = models.DateTimeField(null=True)
    # date_joined = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.username


class AdminGroup(models.Model):
    """
    under the user control group
    用户可以管理的用户组，或组的管理员是该用户
    """

    user = models.ForeignKey(User)
    group = models.ForeignKey(UserGroup)

    def __unicode__(self):
        return '%s: %s' % (self.user.username, self.group.name)


class Document(models.Model):
    def upload_to(self, filename):
        return 'upload/'+str(self.user.id)+time.strftime('/%Y/%m/%d/', time.localtime())+filename

    docfile = models.FileField(upload_to=upload_to)
    user = models.ForeignKey(User)


class Menu(models.Model):

    name = models.CharField(max_length=32, verbose_name=u'菜单名')
    parent = models.ForeignKey('self',
                               verbose_name=u'父级菜单',
                               null=True,
                               blank=True,
                               default='0',
                               help_text=u'如果添加的是子菜单，请选择父菜单')
    show = models.BooleanField(verbose_name=u'是否显示',
                               default=False,
                               help_text=u'菜单是否显示，默认添加不显示')
    url = models.CharField(max_length=300,
                           verbose_name=u'菜单url地址',
                           null=True,
                           blank=True,
                           default='javascript:void(0)',
                           help_text=u'是否给菜单设置一个url地址')
    priority = models.IntegerField(verbose_name=u'显示优先级',
                                    null=True,
                                    blank=True,
                                    default=-1,
                                    help_text=u'菜单的显示顺序，优先级越大显示越靠前')
    permission_id = models.IntegerField(verbose_name=u'权限编号',
                                        help_text=u'给菜单设置一个编号，用于权限控制',
                                        error_messages={'field-permission_id': u'只能输入数字'})

    def __str__(self):
         return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
         verbose_name = u"菜单"
         verbose_name_plural = u"菜单"
         ordering = ["-priority", "id"]