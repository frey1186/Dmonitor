#_*_coding:utf-8_*_
import os
import sys
import subprocess
import docker

class BasicCollector(object):

    def __init__(self):
        base_url = 'unix:///var/run/docker.sock'
        self.docker_conn = docker.Client(base_url=base_url)

    def get_containers(self):
        containers_list = self.docker_conn.containers(all=True)
        return containers_list

    def get_images(self):
        images_list = self.docker_conn.images()
        return images_list




class HostCollector(object):

    # data = {
    #     'cpu':2,  #
    #     'memory':40,
    #     'network':100,
    #     'fs':100,
    # }



    def get_cpu_usage(self):

        # CPU使用率

        # p = subprocess.Popen("head -1 /proc/stat | awk '{ print $2,$3,$4,$5 }'",
        # # p = subprocess.Popen("head -1 / proc / stat ",
        #                                  shell=True,
        #                                  stdout=subprocess.PIPE)
        # user, nice, system, idle = p.stdout.readline().split()
        # # print user, nice,system,idle
        # ret = 100*(eval(user)+eval(nice)+eval(system))/(eval(user)+eval(nice)+eval(system)+eval(idle))
        # return ret

        cmd = "export LANG=en_US;sar 1 5 |grep Average"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        #15:07:20        CPU     %user     %nice   %system   %iowait    %steal     %idle
        t,_,user, nice, system, iowait, steal,idle= p.stdout.readline().split()
        value_dic = {
            'user': user,
            'nice': nice,
            'system': system,
            'iowait': iowait,
            'steal': steal,
            'idle': idle,
            'status': 0
        }
        return value_dic

    def get_mem_usage(self):

        # monitor_dic = {
        #     'SwapUsage': 'percentage',
        #     'MemUsage': 'percentage',
        # }
        cmd = "export LANG=en_US;grep 'MemTotal\|MemFree\|Buffers\|^Cached\|SwapTotal\|SwapFree' " \
              "/proc/meminfo|awk '{ print $2 }'"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        memtotal,memfree,buffers,cached,swaptotal,swapfree = p.stdout.readlines()
        swap_usage = 100*(int(swaptotal)-int(swapfree))/int(swaptotal)
        mem_usage = 100*(int(memtotal)-int(memfree)-int(buffers)-int(cached))/int(memtotal)
        value_dic = {
            'MemTotal':memtotal,
            'SwapTotal':swaptotal,
            'SwapUsage': swap_usage,
            'MemUsage': mem_usage,
        }
        return value_dic

    def get_net_use(self):
        # cmd = "grep -E '^ e|^eth|^e' /proc/net/dev |awk '{ print $2,$10 }';"
        #
        # p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # net_in, net_out = p.stdout.readline().split()
        # ret = (eval(net_in) + eval(net_out))/2
        # return ret
        value_dic = {}
        cmd = "export LANG=en_US;sar -n DEV 1 5 |grep -v veth |grep en |grep Average |awk '{ print $2,$5,$6 }'"
        # Average:        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            interface, net_in, net_out = line.split()
            value_dic[interface] = {
                'net_in': net_in,  #kB/s
                'net_out': net_out, #kB/s
            }
        return value_dic

    def get_block_usage(self):
        #获取文件系统最大使用量
        cmd = "df |grep '^/dev/sd'|awk '{ print $5 }'|sed s/%//g"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        usage_list = p.stdout.readlines()
        fs_usage = max(map(eval, usage_list))
        #get iops and throughout
        cmd = "export LANG=en_US;sar -b 1 5 |grep Average |awk '{ print $3,$4,$5,$6 }'"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        rtps, wtps, breadps, bwrtnps = p.stdout.readline().split()
        value_dic = {
            'rtps': rtps,#times/s
            'wtps': wtps,#times/s
            'breadps': breadps,  #byte/s
            'bwrtnps': bwrtnps,  #byte/s
            'fsusage': fs_usage, # %
        }
        return value_dic

    def collector(self):
        data = {
            'cpu':self.get_cpu_usage(),  #
            'memory':self.get_mem_usage(),
            'network':self.get_net_use(),
            'block':self.get_block_usage(),
        }
        return data




class DataCollector(object):
    '''
    data collector

    a = {

            cpu:{
                73f8de43fef02d34d5c95813c45f1c05c4692a72a25fa93387e8c0c674278679:{
                    cpuacct.usage:'1021',
                    cpuacct.stat:'user 0\nsystem 1'
                },
            },
            memery:{
                73f8de43fef02d34d5c95813c45f1c05c4692a72a25fa93387e8c0c674278679:{
                    memery.usage:'1024756',

                }
            }
    }
'''
    def __init__(self, container_list):
        self.container_list = container_list

    def get_from_file(self, target_dict):
        data = {}
        target_data = {}
        for target in target_dict:
            path = '/sys/fs/cgroup/' + target + '/docker'
            container_data = {}
            for container in self.container_list:
                c_dir ='/'.join([path, container])
                for parameter_file in target_dict[target]:
                    p = subprocess.Popen("cat " + c_dir+'/'+parameter_file,
                                         shell=True,
                                         stdout=subprocess.PIPE)
                    container_data[parameter_file] = p.stdout.read().strip().split()
                target_data[container] = container_data
            data[target] = target_data
            target_data = {}
        return data

    def get_from_cmd(self):
        p = subprocess.Popen("sudo docker stats --no-stream",
                                     shell=True,
                                     stdout=subprocess.PIPE)
        data = p.stdout.readlines()
        return data


    def get_from_api(self):
        import requests
        ret = requests.get("http://www.baidu.com")

        return ret.content


if __name__ == '__main__':
#     d = DataCollector(['73f8de43fef02d34d5c95813c45f1c05c4692a72a25fa93387e8c0c674278679',],
#                       )
#     a = d.get_from_file(target_dict)
#     print(a)
#     # b = d.get_from_cmd()
#     # print(b)
#     # c = d.get_from_api()
#     # print c

    h = HostCollector()
    a = h.get_cpu_usage()
    b = h.get_mem_usage()
    c = h.get_net_use()
    d = h.get_fs_usage()
    print a
    print b
    print c
    print d