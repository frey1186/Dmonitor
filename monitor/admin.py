from django.contrib import admin
from monitor import models
# Register your models here.


class HostAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'address', 'status', 'username']


class TriggerItemAdmin(admin.ModelAdmin):
    list_display = ['indicator', 'group', 'func', 'condition', 'limit_value', 'logic_type']

admin.site.register(models.UserProfile)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.Indicator)
admin.site.register(models.TriggerItem, TriggerItemAdmin)
admin.site.register(models.Trigger)
admin.site.register(models.IndicatorGroup)
admin.site.register(models.AlarmUpgradeTemplate)
admin.site.register(models.Alarm)
admin.site.register(models.AlarmUpgradeItem)

