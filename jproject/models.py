# coding: utf-8

from django.db import models

from juser.models import User
from jasset.models import Asset,AssetGroup
from juser.models import  Dept


SCM_TYPE_CHOICES= (
    ("GIT","gitlab"),
    ("SVN","svn")
)
SCM_MODEL_CHOICES = (
    ("java","java"),
    ("python","python")
)


PUBLISH_TYPE_CHOICES = (
    ("dev","dev"),
    ("product","product"),
    ("test","test")
)



class SCMSetting(models.Model):
    scm_url = models.CharField(max_length=100, null=True, unique=True, default=None, verbose_name=u'GitLab域名')
    scm_type = models.CharField(max_length=30, null=True, unique=True, default=None, verbose_name=u'管理员token')
    default_user=models.CharField(max_length=32)
    default_password=models.CharField(max_length=64)
    default_token=models.CharField(max_length=128)


class SCMToken(models.Model):
    scmsetting = models.ForeignKey(SCMSetting)
    scm_user = models.CharField(max_length=32)
    scm_password= models.CharField(max_length=64)
    scm_user_token = models.CharField(max_length=128, null=True, unique=True, default=None, verbose_name=u'用户token')
    fullname = models.ForeignKey(User, null=False, blank=False, verbose_name=u'姓名')


class Group(models.Model):
    code=models.CharField(max_length=32,unique=True)
    name=models.CharField(max_length=32,unique=True)
    def __unicode__(self):
        return self.name



class Project(models.Model):
    name =models.CharField(max_length=128,unique=True)
    code = models.CharField(max_length=30,unique=True)
    scm_url =models.CharField(max_length=255,unique=True)
    scm = models.ForeignKey(SCMSetting)
    scm_project = models.CharField(max_length=255,blank=True)
    scm_model_type = models.CharField(max_length=10, choices=SCM_MODEL_CHOICES, default='java')
    scm_type = models.CharField(max_length=10, choices=SCM_TYPE_CHOICES, default='GIT')
    owner = models.ForeignKey(User)
    dept = models.ForeignKey(Dept)
    group=models.ManyToManyField(Group)
    dependent=models.ManyToManyField('self')
    manage =models.CharField(max_length=32)
    phone = models.CharField(max_length=20)
    work=models.CharField(max_length=255)
    web_work=models.CharField(max_length=255)
    backup =models.CharField(max_length=128)

# class ProjectMembership(models.Model)
#     project=models.ForeignKey(Project)
#     group=models.ForeignKey(ProjectGroup)
#     sort= models.IntegerField

class Config(models.Model):
    CONFIG_FLAG_CHOICES=(('1','必须'),('2','非必须'))
    project=models.OneToOneField('Project')
    file=models.CharField(max_length=255)
    item=models.CharField(max_length=255)
    defaultvalue=models.CharField(max_length=255)
    filetype=models.CharField(max_length=32)
    flag=models.CharField(max_length=2,choices=CONFIG_FLAG_CHOICES)



class Env(models.Model):
    name= models.CharField(max_length=10, choices=PUBLISH_TYPE_CHOICES, default='test')
    precode=models.CharField(max_length=10)
    code=models.CharField(max_length=32)

class Parameter(models.Model):
    project=models.ForeignKey(Project)
    env=models.ForeignKey(Env)
    file=models.CharField(max_length=255)
    item=models.CharField(max_length=255)
    confvalue=models.CharField(max_length=255)
    filetype=models.CharField(max_length=32)

STATUS_CHOICES=(("1","申请"),("2","批准"),("3","成功"),("4","失败"),("5","申请回退"),("6","回退中"),("7","回退完成"))
MODEL_CHOICES=(("1","local"),("2","remotersync"),("3","bit"))
SCHEDULE_TYPE_CHOICES=(("1","一次"),("2","定时"),("3","不限次"))

class Publish(models.Model):
    project=models.ForeignKey(Project)
    projectgroup=models.ForeignKey(Group)
    env=models.ForeignKey(Env)
    commits=models.CharField(max_length=255)
    branch=models.CharField(max_length=255)
    asset=models.ForeignKey(Asset)
    assetgroup=models.ForeignKey(AssetGroup)
    schedule=models.ForeignKey('Schedule')
    user=models.ForeignKey(User)
    before=models.CharField(max_length=255)
    after=models.CharField(max_length=255)
    model=models.CharField(max_length=20,choices=MODEL_CHOICES)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES)


class Schedule(models.Model):
    type=models.CharField(max_length=20,choices=SCHEDULE_TYPE_CHOICES)
    start=models.DateField()
    schedule=models.CharField(max_length=32)

class publishHistory(models.Model):

    publish=models.ForeignKey(Publish)
    start=models.DateField()
    end=models.DateField()
    user=models.ForeignKey(User)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES)
    


