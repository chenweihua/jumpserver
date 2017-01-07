# coding: utf-8

from django.db import models

from juser.models import User
from jasset.models import Asset,AssetGroup
from juser.models import  Dept
from jumpserver.models import Env,ScmType,CompileTool,ConfigType,PublishMode,PublishStatus,PublishType

class SCMSetting(models.Model):
    scm_url = models.CharField(max_length=100, null=True, unique=True, default=None, verbose_name=u'GitLab域名')
    scm_type = models.CharField(max_length=30, null=True, unique=True, default=None, verbose_name=u'管理员token')
    default_user=models.CharField(max_length=32)
    default_password=models.CharField(max_length=64)
    default_token=models.CharField(max_length=128)
    def __unicode__(self):
        return self.scm_url



class SCMToken(models.Model):
    scmsetting = models.ForeignKey(SCMSetting)
    scm_user = models.CharField(max_length=32)
    scm_password= models.CharField(max_length=64)
    scm_user_token = models.CharField(max_length=128, null=True, unique=True, default=None, verbose_name=u'用户token')
    fullname = models.ForeignKey(User, null=False, blank=False, verbose_name=u'姓名')
    def __unicode__(self):
        return self.scm_user

class ProjectGroup(models.Model):
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
    scm_model_type= models.ForeignKey(CompileTool)
    scm_type = models.ForeignKey(ScmType)
    owner = models.ForeignKey(User,related_name="owner")
    dept = models.ForeignKey(Dept)
    group=models.ManyToManyField(ProjectGroup)
    dependent=models.ManyToManyField('self')
    manage =models.ForeignKey(User,related_name="manage")
    phone = models.CharField(max_length=20)
    work=models.CharField(max_length=255)
    web_work=models.CharField(max_length=255)
    backup =models.CharField(max_length=128)
    def __unicode__(self):
        return self.name



class Config(models.Model):
    project=models.ForeignKey(Project)
    file=models.CharField(max_length=255)
    item=models.CharField(max_length=64)
    confvalue=models.CharField(max_length=128)
    filetype=models.CharField(max_length=10)
    def __unicode__(self):
        return self.file




class PublishConfig(models.Model):
    project=models.ForeignKey(Project)
    env=models.ForeignKey(Env)
    prefix = models.CharField(max_length=255)
    file=models.CharField(max_length=255)
    item=models.CharField(max_length=64)
    confvalue=models.CharField(max_length=128)
    filetype=models.CharField(max_length=10)
    def __unicode__(self):
        return self.item



class Publish(models.Model):
    project=models.ForeignKey(Project)
    projectgroup=models.ForeignKey(ProjectGroup)
    env=models.ForeignKey(Env)
    commits=models.CharField(max_length=255)
    branch=models.CharField(max_length=255)
    asset=models.ForeignKey(Asset)
    assetgroup=models.ForeignKey(AssetGroup)
    schedule=models.ForeignKey('Schedule')
    user=models.ForeignKey(User)
    before=models.CharField(max_length=255)
    after=models.CharField(max_length=255)
    model=models.ForeignKey(PublishMode)
    status= models.ForeignKey(PublishStatus)
    def __unicode__(self):
        return self.name

class Schedule(models.Model):
    type = models.ForeignKey(PublishType)
    start=models.DateField()
    schedule=models.CharField(max_length=32)
    def __unicode__(self):
        return self.type

class publishHistory(models.Model):
    publish=models.ForeignKey(Publish)
    start=models.DateField()
    end=models.DateField()
    user=models.ForeignKey(User)
    status= models.ForeignKey(PublishStatus)



