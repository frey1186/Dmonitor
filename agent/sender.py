#_*_coding:utf-8_*_
from canister import DataCollector,HostCollector,BasicCollector
import settings
import time, threading
import urllib
import urllib2
import json
import os
import docker


def run_forever():
    exit_flag = False
    while not exit_flag:
        # get all containers name
        # container_list = []
        # for f in os.listdir('/sys/fs/cgroup/cpu/docker'):
        #     if os.path.isdir('/sys/fs/cgroup/cpu/docker/' + f):
        #         container_list.append(f)

        base_url = 'unix:///var/run/docker.sock'
        docker_conn = docker.Client(base_url=base_url)
        container_list = [a.get("Id") for a in docker_conn.containers()]
        data_collector = DataCollector(container_list=container_list)
        contrainer_realtime_data = data_collector.get_from_file(settings.target_dict)

        host_collector = HostCollector()
        host_realtime_data = host_collector.collector()

        basic_data = BasicCollector()

        basic_host_data = {
            "HostID": settings.configs['HostID'],
            "containers_list":basic_data.get_containers(),
            "images_list":basic_data.get_images(),
        }

        # print contrainer_realtime_data
        url_request(
            settings.configs['urls']['service_report'][1],
            settings.configs['urls']['service_report'][0],
            {'con_real_data':contrainer_realtime_data,
             'host_real_data':host_realtime_data,
             'basic_data':basic_host_data
             }
        )
        time.sleep(10)


def url_request(action, url, extra_data):
    '''
    cope with monitor server by url
    :param action: "get" or "post"
    :param url: witch url you want to request from the monitor server
    :param extra_data: extra parameters needed to be submited
    :return:
    '''
    abs_url = "http://%s:%s/%s" % (settings.configs['Server'],
                                   settings.configs["ServerPort"],
                                   url)
    print abs_url
    if action in ('get', 'GET'):
        print(abs_url, extra_data)
        try:
            req = urllib2.Request(abs_url)
            req_data = urllib2.urlopen(req, timeout=settings.configs['RequestTimeout'])
            callback = req_data.read()
            # print "-->server response:",callback
            return callback
        except urllib2.URLError as e:
            exit("\033[31;1m%s\033[0m" % e)

    elif action in ('post', 'POST'):
        # print(abs_url,extra_data['params'])
        try:
            # print extra_data
            data_encode = urllib.urlencode(extra_data)

            req = urllib2.Request(url=abs_url, data=data_encode)
            res_data = urllib2.urlopen(req, timeout=settings.configs['RequestTimeout'])
            callback = res_data.read()
            callback = json.loads(callback)
            print("\033[31;1m[%s]:[%s]\033[0m response:\n%s" % (action, abs_url, callback))
            return callback
        except Exception as e:
            print('---exec', e)
            exit("\033[31;1m%s\033[0m" % e)

if __name__ == '__main__':
    run_forever()