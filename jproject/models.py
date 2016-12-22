# coding: utf-8

from django.db import models

from juser.models import User
from jasset.models import Asset,AssetGroup

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
    scm_address =models.ForeignKey(SCMSetting)
    scm_url =models.CharField(max_length=255,unique=True)
    scm_model_type = models.CharField(max_length=10, choices=SCM_MODEL_CHOICES, default='java')
    scm_type = models.CharField(max_length=10, choices=SCM_TYPE_CHOICES, default='GIT')
    scm_branch=models.CharField(max_length=128,default="master")
    user = models.ForeignKey(User)
    projectgroup=models.ManyToManyField(ProjectGroup)
    depproject=models.ManyToManyField('self')
    proejct_username =models.CharField(max_length=32)
    project_phone = models.CharField(max_length=20)
    project_work=models.CharField(max_length=255)
    project_web_work=models.CharField(max_length=255)


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
    publish_type= models.CharField(max_length=10, choices=PUBLISH_TYPE_CHOICES, default='test')
    pubish_commits=models.CharField(max_length=255)
    publish_code=models.CharField(max_length=32)
    asset=models.ForeignKey(Asset)
    assetgroup=models.ForeignKey(AssetGroup)

