#_*_coding:utf-8_*_
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

@python_2_unicode_compatible
class UserProfile(models.Model):
    '''
    用户
    '''
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class HostGroup(models.Model):
    '''
    主机组或者集群
    '''
    groupname = models.CharField(u'集群/组', max_length=32,)
    memo = models.TextField(u"备注", blank=True, null=True)

    def __str__(self):
        return self.groupname

@python_2_unicode_compatible
class Host(models.Model):
    '''
    主机
    '''

    hostname = models.CharField(u'主机名', max_length=32,)
    address = models.GenericIPAddressField(u'IP地址',)
    port = models.IntegerField(u'docker运行端口', default=2375)
    group = models.ManyToManyField(HostGroup, verbose_name=u'集群/组')
    status_choices = (
            ('Online', u'在线'),
            ('Offline', u'掉线'),
            # ('Unreachable', u'不可达'),
            ('Maintenance', u'维护'),
        )
    status = models.CharField(u'状态', choices=status_choices, max_length=64)
    username = models.CharField(u'用户名', default='root', max_length=32, blank=True, null=True)
    password = models.CharField(u'密码', max_length=32, blank=True, null=True)  # 明文，后续修改
    memo = models.TextField(u"备注", blank=True, null=True)


    def __str__(self):
        return '%s-%s'% (self.hostname,self.address)

@python_2_unicode_compatible
class Indicator(models.Model):
    '''
    指标
    '''
    name = models.CharField(u'指标名', max_length=32, blank=True, null=True)

    types_choice = (
        ('cpu', 'CPU'),
        ('mem', 'Memory'),
        ('io', 'IO'),
        ('network', 'Network'),
    )
    types = models.CharField(u'类型', choices=types_choice, max_length=16)
    parameter = models.CharField(u'指标参数', max_length=16,)
    memo = models.TextField(u"备注", blank=True, null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class IndicatorGroup(models.Model):
    '''
    指标组
    '''
    name = models.CharField(u'指标组名', max_length=32)
    indicator = models.ManyToManyField(Indicator, verbose_name=u'指标')
    memo = models.TextField(u"备注", blank=True, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TriggerItem(models.Model):
    '''

    触发器条目

    '''

    indicator = models.ForeignKey(Indicator, verbose_name=u'指标参数')
    group = models.ForeignKey(HostGroup, verbose_name=u'集群/组')
    func_choice = (
        ('max', 'Max'),
        ('min', 'Min'),
        ('average', 'Average'),
    )
    func = models.CharField(u'统计方法', choices=func_choice, max_length=16)
    condition_choice = (
        ('gt', u'大于'),
        ('lt', u'小于'),
        ('eq', u'等于'),
        ('gte', u'大于等于'),
        ('lte', u'小于等于'),
    )
    condition = models.CharField(u'运算符', choices=condition_choice, max_length=16)
    limit_value = models.IntegerField(u'阀值')
    logic_type_choices = (
        ('or', 'OR'),
        ('and', 'AND'),
    )
    logic_type = models.CharField(u"与下一个条件的逻辑关系",
                                  choices=logic_type_choices,
                                  max_length=32,
                                  blank=True,
                                  null=True
                                  )
    memo = models.TextField(u"备注", blank=True, null=True)

    def __str__(self):
        return 'TriggerItem-%s'% self.indicator.name

@python_2_unicode_compatible
class Trigger(models.Model):
    '''
    触发器
    '''
    name = models.CharField(u'触发器名', max_length=16)
    triggeritems = models.ManyToManyField(TriggerItem, verbose_name=u'触发器条目')
    level_choices = (
        ('info', u'消息'),
        ('debug', u'调试'),
        ('danger', u'危险'),
        ('disaster', u'灾难'),

    )
    level = models.CharField(u'事件级别', choices=level_choices, max_length=16)
    memo = models.TextField(u"备注", blank=True, null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class AlarmUpgradeItem(models.Model):
    '''
    告警升级处理
    '''
    alarm_times = models.IntegerField(u'告警次数')
    mail_to = models.ForeignKey(UserProfile, verbose_name=u'发送给')

    def __str__(self):
        return '%s times to %s' % (self.alarm_times, self.mail_to.name)


@python_2_unicode_compatible
class AlarmUpgradeTemplate(models.Model):
    name = models.CharField(u'告警升级模版', max_length=16)
    upgrade_items = models.ManyToManyField(AlarmUpgradeItem, verbose_name=u'告警升级条目')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Alarm(models.Model):
    '''
    告警
    '''
    name = models.CharField(u'告警', max_length=16)
    triggers = models.ManyToManyField(Trigger, verbose_name=u'触发器')
    alarm_upgrade = models.ForeignKey(AlarmUpgradeTemplate, verbose_name=u'告警级别升级模版')
    memo = models.TextField(u"备注", blank=True, null=True)

    def __str__(self):
        return self.name