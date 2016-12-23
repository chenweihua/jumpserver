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
    gitsetting = models.ForeignKey(SCMSetting)
    scm_user = models.CharField(max_length=32)
    scm_password= models.CharField(max_length=64)
    scm_user_token = models.CharField(max_length=128, null=True, unique=True, default=None, verbose_name=u'用户token')
    fullname = models.ForeignKey(User, null=False, blank=False, verbose_name=u'姓名')


class ProjectGroup(models.Model):
    group_code=models.CharField(max_length=32,unique=True)
    group_name=models.CharField(max_length=32,unique=True)
    def __unicode__(self):
        return self.name



class Project(models.Model):
    project_name =models.CharField(max_length=128,unique=True)
    project_code = models.CharField(max_length=30,unique=True)
    scm_url =models.CharField(max_length=255,unique=True)
    scm_model_type = models.CharField(max_length=10, choices=SCM_MODEL_CHOICES, default='java')
    scm_type = models.CharField(max_length=10, choices=SCM_TYPE_CHOICES, default='GIT')
    owner = models.ForeignKey(User)
    dept = models.ForeignKey(Dept)
    projectgroup=models.ManyToManyField(ProjectGroup)
    dependent=models.ManyToManyField('self')
    manage =models.CharField(max_length=32)
    phone = models.CharField(max_length=20)
    work=models.CharField(max_length=255)

    web_work=models.CharField(max_length=255)

# class ProjectMembership(models.Model)
#     project=models.ForeignKey(Project)
#     group=models.ForeignKey(ProjectGroup)
#     sort= models.IntegerField

class ProjectConfig(models.Model):
    project=models.ForeignKey('Project')
    config_file=models.CharField(max_length=255)
    config_item=models.CharField(max_length=255)
    config_default_value=models.CharField(max_length=255)
    config_filetype=models.CharField(max_length=32)



class PublishEnv(models.Model):
    config_name= models.CharField(max_length=10, choices=PUBLISH_TYPE_CHOICES, default='test')
    config_code=models.CharField(max_length=32)

class PublishConfig(models.Model):
    project=models.ForeignKey(Project)
    publishenv=models.ForeignKey(PublishEnv)
    config_file=models.CharField(max_length=255)
    config_item=models.CharField(max_length=255)
    config_default_value=models.CharField(max_length=255)
    config_filetype=models.CharField(max_length=32)


class PublishProject(models.Model):
    project=models.ForeignKey(Project)
    projectgroup=models.ForeignKey(ProjectGroup)
    publishenv=models.ForeignKey(PublishEnv)
    pubish_commits=models.CharField(max_length=255)
    pubish_branch=models.CharField(max_length=255)
    asset=models.ForeignKey(Asset)
    assetgroup=models.ForeignKey(AssetGroup)
    publish_schedule=models.ManyToManyField()
    publish_type=models.CharField(max_length=20,choices=(("1","一次"),("2","定时")))
    publish_status=models.CharField(max_length=20,choices=(("1","成功"),("2","失败"),("3","申请回退"),("2","回退中"),("2","回退完成")))

class PublishSchedule(models.Model):
    publish_backup =models.CharField(max_length=128)
    publish_start=models.DateField()
    publish_schedule=models.CharField(max_length=32)

class publishHistory(models.Model):
    publishproject=models.ForeignKey(PublishProject)
    publish_start=models.DateField()
    publish_end=models.DateField()
    


