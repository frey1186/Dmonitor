#_*_coding:utf-8_*_
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyMonitor.settings")

import paramiko

def get_from_host(hostname, password, username='root',cmd='docker images'):
    '''
    从主机上获取docker镜像的信息
    :param hostname:主机名或ip地址
    :param username:用户名，默认root
    :param password:密码
    :return:返回images信息list
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname, 22, username, password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        ret = stdout.readlines()
    except Exception:
        ret =[]
    finally:
        ssh.close()
    return ret



def parse_stdout(out_strings_lines):
    ret_lines = []
    for line in out_strings_lines:
        ret = line.split()
        ret_lines.append(ret)
    return ret_lines



if __name__ == '__main__':

    hostname = '192.168.19.110'
    username = 'felo'
    password='felo'
    ret = get_from_host(hostname, password, username)
    print(ret)
