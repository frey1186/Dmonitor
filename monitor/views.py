#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse
from monitor import models
from monitor.backends import redis_conn
from MyMonitor import settings
from django.views.decorators.csrf import csrf_exempt
from backends import data_processer
import json
import docker
import time
from backends import alert



# Create your views here.

REDIS_OBJ = redis_conn.redis_conn(settings)

def index(request):
    # print(request.user.userprofile.name)

    # return render(request, 'base.html')
    return render(request, 'monitor/highchart_test.html')


def host_list(request):
    host_objs = models.Host.objects.all()
    return render(request,
                  'monitor/host_list.html',
                  {'host_list': host_objs}
                  )


def host_detail(request, host_id):
    host = models.Host.objects.get(id=host_id)
    conn_para = 'tcp://%s:%s' % (host.address, host.port)
    c = docker.Client(conn_para, timeout=2)
    images = c.images()
    containers = c.containers()

    return render(request,
                  'monitor/host_detail.html',
                  {'images_list': images,
                   'containers_list': containers,
                   'host': host}
                  )


def images_list(request):
    host_objs = models.Host.objects.filter(status="Online")
    images = {}
    for host in host_objs:
        conn_para = 'tcp://%s:%s' % (host.address, host.port)
        c = docker.Client(conn_para)
        images_in_host = c.images()
        images[host.address] = images_in_host

    return render(request,
                  'monitor/images_list.html',
                  {'images_list':images,
                   'host_list':host_objs}
                  )


def container_list(request):
    host_objs = models.Host.objects.filter(status="Online")
    containers = {}
    for host in host_objs:
        conn_para = 'tcp://%s:%s' % (host.address, host.port)
        c = docker.Client(conn_para)
        containers_in_host = c.containers(all=True)
        containers[host] = containers_in_host
    return render(request,
                  'monitor/containers_list.html',
                  {'containers_list': containers,
                   }
                  )

def container_detail(request,host_id, container_id):
    host = models.Host.objects.get(id=host_id)
    conn_para = 'tcp://%s:%s' % (host.address, host.port)
    c = docker.Client(conn_para)
    inspect_container_dict = c.inspect_container(container_id)
    return render(request,
                  'monitor/containers_detail.html',
                  {
                      'inspect_container':inspect_container_dict,
                  }
                  )



def _get_alert_re():
    return ['memory','MemUsage','>','80']


def real_host(request):
    host_objs = models.Host.objects.filter(status="Online")
    data = {}



    for host in host_objs:
        real_raw_data_dic = {}
        for service_name in ['cpu','memory','network','block']:
            real_data = REDIS_OBJ.lrange("RawData_(%s,)_host_%s" % (host.id,service_name), 0, 0)
            # print "raw------>",real_data[0]

            if real_data:
                report_time,real_raw_data = real_data[0].split(",", 1)
                # print real_raw_data
                # print 'time===>',time.strftime(report_time)
                real_raw_data_dic[service_name] = eval(real_raw_data)

                # print real_raw_data_dic,type(real_raw_data_dic)
            else:
                real_raw_data_dic[service_name] = ''
        data[host.id] = real_raw_data_dic
            # """
            # data = {
            #     "host_id":
            #         "cpu":{'status': 0, 'iowait': '0.00', 'system': '2.14', 'idle': '97.24', 'user': '0.61', 'steal': '0.00', 'nice': '0.00'},
            #         "memory":{'MemUsage': 123, 'SwapUsage': 0},
            #         "network":{'ens33': {'net_out': '0.00', 'net_in': '0.00'}},
            #         "block":{'fsusage': 58, 'breadps': '0.00', 'rtps': '0.00', 'wtps': '0.00', 'bwrtnps': '0.00'},
            # }
            # """
        # alert
        alert_service_name,alert_parameter = _get_alert_re()[0],_get_alert_re()[1]
        alert_exp = ''.join(_get_alert_re()[2:])
        # for alert
        try:
            real_parameter_data =data[host.id][alert_service_name][alert_parameter]
            print str(real_parameter_data)+alert_exp
            if eval(str(real_parameter_data)+alert_exp):
                #send email to alert
                mail_sub = 'Docker Host Perf Alart.'
                mail_htmltext = '''<html>
                    <h1>alert message:</h1>
                    <hr>
                    <p>hostname:%s</p>
                    <p>alert massage:</p>
                    <p>alert exp:%s%s</p>
                    <p>host:%s=%s</p>
                                </html>'''%(host.hostname,
                                            alert_parameter,
                                            alert_exp,
                                            alert_parameter,
                                            real_parameter_data )
                alert.SendEmail('yangfeilong_2009@126.com',mail_sub,mail_htmltext)
            else:
                pass
        except:
            pass



    return render(request, 'monitor/realtime_host.html',
                  {
                      "host_list":host_objs,
                      "real_host_data":data,
                  })

def _get_data_temp(host_id):
    data_temp = {
        "cpu": ['status','iowait','system', 'idle','user','steal','nice',],
        "memory": ['MemUsage', 'SwapUsage'],
        "network": {'ens33': ['net_out', 'net_in'], },
        "block": ['fsusage','breadps','rtps','wtps','bwrtnps',],
    }
    return data_temp

def monitor_data_detail(request, host_id):
    host_obj = models.Host.objects.get(id=host_id)
    data_temp = _get_data_temp(host_id)
    return render(request, 'monitor/monitor_host_detail.html',
              {
                  "host_obj": host_obj,
                  "data_temp": data_temp,
              })



import random
def monitor_data(request, host_id):
    #'iowait': '0.00', 'system': '2.14', 'idle': '97.24', 'user': '0.61', 'steal': '0.00', 'nice': '0.00'
    redis_keys = 'RawData_(%s,)_host_*' % host_id
    redis_values = {}
    for redis_key in redis_keys:
        redis_values[redis_key] = REDIS_OBJ.lrange(redis_key, 0, 30)
    temp_data = []
    for obj in redis_values:
        report_time, mondata = obj.split(',', 1)
        mondata = eval(mondata)
        data_unit = [report_time, mondata]
        temp_data.append(data_unit)
    # print "old----->:",temp_data
    temp_data.reverse()

    data = json.dumps(temp_data)
    return HttpResponse(data)



def current_data(request, host_id):
    # redis_keys = REDIS_OBJ.keys('"RawData_(%s,)_host_*' % host_id)
    # redis_keys.sort()
    # print(redis_keys)
    # key = redis_keys[-1]
    # data = REDIS_OBJ.lrange(key, -1, -1)[0]
    # data = json.loads(data.decode())
    # print('--->lasted data:', data)

    ################################ cpu idle ###########################
    redis_key = 'RawData_(%s,)_host_cpu' % host_id
    obj = REDIS_OBJ.lrange(redis_key, 0, 0)[0]
    report_time, mondata = obj.split(',', 1)
    mondata = eval(mondata)['idle']
    # print "-"*50,'>',report_time,mondata
    data = json.dumps([report_time, mondata])

    # ################################## mem usage ##############################
    # redis_key = 'RawData_(%s,)_host_memory' % host_id
    # obj = REDIS_OBJ.lrange(redis_key, 0, 0)[0]
    # report_time, mondata = obj.split(',', 1)
    # mondata = eval(mondata)['MemUsage']
    # # print "-"*50,'>',report_time,mondata
    # data = json.dumps([report_time, mondata])




    return HttpResponse(data)

def real_data_detail(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)
    return render(request,
                  'monitor/realtime_host_detail.html',
                  {
                      "host_obj":host_obj,
                  })



def client_configs(request):
    pass

@csrf_exempt
def service_data_report(request):
    if request.method == 'POST':
        # print("---->",request.POST)
        # REDIS_OBJ.set("test_alex",'hahaha')
        try:
            # print('host=%s, service=%s' %(request.POST.get('client_id'),request.POST.get('service_name') ) )
            # data =  json.loads(request.POST['data'])
            # print request.POST['con_real_data']
            # print request.POST['host_real_data']
            client_id = eval(request.POST.get('basic_data'))["HostID"]

            con_real_data = eval(request.POST['con_real_data'])
            host_real_data = eval(request.POST['host_real_data'])
            basic_data = eval(request.POST['basic_data'])

            host_data_saveing_obj = data_processer.DataProcessor(client_id,"host",host_real_data,REDIS_OBJ)
            host_data_saveing_obj.data_save()
            con_data_saveing_obj = data_processer.DataProcessor(client_id, "container", con_real_data, REDIS_OBJ)
            con_data_saveing_obj.data_save()
            basic_data_saveing_obj = data_processer.DataProcessor(client_id, "basic", basic_data, REDIS_OBJ)
            basic_data_saveing_obj.data_save()

            # service_name = request.POST.get('service_name')
            # data_saveing_obj = data_optimization.DataStore(client_id,service_name,data,REDIS_OBJ)

            #redis_key_format = "StatusData_%s_%s_latest" %(client_id,service_name)
            #data['report_time'] = time.time()
            #REDIS_OBJ.lpush(redis_key_format,json.dumps(data))

            #在这里同时触发监控
            # host_obj = models.Host.objects.get(id=client_id)
            # service_triggers = get_host_triggers(host_obj)
            #
            # trigger_handler = data_processing.DataHandler(settings,connect_redis=False)
            # for trigger in service_triggers:
            #     trigger_handler.load_service_data_and_calulating(host_obj,trigger,REDIS_OBJ)
            # print("service trigger::",service_triggers)


            #更新主机存活状态
            #host_alive_key = "HostAliveFlag_%s" % client_id
            #REDIS_OBJ.set(host_alive_key,time.time())
        except IndexError as e:
            print('----->err:',e)


    return HttpResponse(json.dumps("---report success---"))



