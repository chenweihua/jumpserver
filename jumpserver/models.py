# coding: utf-8

from django.db import models

class Setting(models.Model):
    name = models.CharField(max_length=100)
    field1 = models.CharField(max_length=100, null=True, blank=True)
    field2 = models.CharField(max_length=100, null=True, blank=True)
    field3 = models.CharField(max_length=256, null=True, blank=True)
    field4 = models.CharField(max_length=100, null=True, blank=True)
    field5 = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = u'sys_setting'

    def __unicode__(self):
        return self.name


#物理机 虚拟机  交换机   路由器  防火墙 Docker 其他
class AssetType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_asset_type'
        verbose_name =u"资产状态"

    def __unicode__(self):
        return self.name


#正常 不能联接  当掉
class AssetSatus(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_asset_status'
        verbose_name =u"资产状态"

    def __unicode__(self):
        return self.name

#未安装，安装中，安装完成
class AssetInstallSatus(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_asset_install_status'

    def __unicode__(self):
        return self.name
        verbose_name =u"资产操作系统安装状态"


#新购 使用 故障 报费 空闲
class AssetUseSatus(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_asset_use_status'
        verbose_name =u"服务器使用状态"

    def __unicode__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=32)
    port = models.CommaSeparatedIntegerField(max_length=255)
    type = models.CharField(max_length=20)
    class Meta:
        db_table = u'sys_service'
        verbose_name =u"服务"

    def __unicode__(self):
        return self.name

#Centos Ubuntu  Rdhad
class SystemType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_system_type'

    def __unicode__(self):
        return self.name

#x86_64 i386
class SystemArchType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_system_arch_type'

    def __unicode__(self):
        return self.name

#x7.2 6.8 14.04 16.04
class SystemArchVersion(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_system_arch_version'
    def __unicode__(self):
        return self.name

# 电信 移动 联通 铁通 小带寅
class Operator(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_operator'

    def __unicode__(self):
        return self.name

#cdn,核心
class IdcType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_idc_type'

    def __unicode__(self):
        return self.name

#zookeeper,mesos,k8s,marathon
class ClusterType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_cluster_type'

    def __unicode__(self):
        return self.name

#dev product test
class EnvType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_env_type'

    def __unicode__(self):
        return self.name


class Env(models.Model):
    name= models.CharField(max_length=32)
    code = models.ForeignKey(EnvType)
    precode=models.CharField(max_length=10)
    rsync_resouce= models.CharField(max_length=255)
    rsync_project = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
        db_table = u'sys_env'


class ClusterInfo(models.Model):
    name = models.CharField(max_length=32)
    type = models.ForeignKey(ClusterType)
    env_info = models.ForeignKey("Env")
    item = models.CharField(max_length=255)
    class Meta:
        db_table = u'sys_cluster_info'

    def __unicode__(self):
        return self.name

#硬件产商
class Brand(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_brand'

    def __unicode__(self):
        return self.name


#处理中 观察 没处理 关闭
class IncidentStatus(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_incidnet_status'
    def __unicode__(self):
        return self.name

#zabbix 监控脚本
class IncidentSource(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_incidnet_source'
    def __unicode__(self):
        return self.name

#高危 严重 中级 一般
class IncidentRank(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_incidnet_rank'
    def __unicode__(self):
        return self.name

#gitlab svn github
class ScmType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_scm_tpye'
    def __unicode__(self):
        return self.name

# maven gradle node python php go c
class CompileTool(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_compile_tool'
    def __unicode__(self):
        return self.name

#申请  批准  成功 失败 申请回退 回退中 回退完成
class PublishStatus(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_publish_status'
    def __unicode__(self):
        return self.name

#localsync remotesync  bit
class PublishType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_publish_type'
    def __unicode__(self):
        return self.name

#定时 手工  一次
class PublishMode(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_publish_mode'
    def __unicode__(self):
        return self.name

#必须 非必须
class ConfigType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_config_type'
    def __unicode__(self):
        return self.name

# company  dept
class DeptType(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'sys_dept_type'
    def __unicode__(self):
        return self.name
