#_*_coding:utf-8_*_
import time
import json

class DataProcessor(object):
    def __init__(self, host_id, type_of_data, data, REDIS_OBJ):
        self.host_id = host_id,
        self.type_of_data = type_of_data
        self.data = data
        self.REDIS_OBJ = REDIS_OBJ


    def data_save(self):
        if self.type_of_data == "host":
            '''
            data = {
            'cpu':self.get_cpu_usage(),  #
            'memory':self.get_mem_usage(),
            'network':self.get_net_use(),
            'block':self.get_block_usage(),
        }
            '''
            for service_name in self.data:
                redis_key = 'RawData_%s_%s_%s' % (self.host_id, self.type_of_data,service_name)
                redis_value = '%s,%s' % (time.time(), json.dumps(self.data[service_name]))
                self.REDIS_OBJ.lpush(redis_key, redis_value)

        elif self.type_of_data == "container":
            '''
            {'blkio':
                {'23aed474e6b0281f491c0e598f57a9667f879b1d16c2601f9de588b0347ae55a':
                    {'blkio.io_queued': ['Total', '0'],
                    'blkio.io_service_bytes': ['Total', '0']},
                 '2483ed35e92d0f10e509ca4cdacf263f05cabf69c09495798af8edf4cd59d43e':
                    {'blkio.io_queued': ['Total', '0'],
                    'blkio.io_service_bytes': ['Total', '0']}},
             'cpuacct':
                {'23aed474e6b0281f491c0e598f57a9667f879b1d16c2601f9de588b0347ae55a':
                    {'cpuacct.stat': ['user', '2', 'system', '0'],
                    'cpuacct.usage': ['34860616']},
                '2483ed35e92d0f10e509ca4cdacf263f05cabf69c09495798af8edf4cd59d43e':
                    {'cpuacct.stat': ['user', '2', 'system', '0'],
                    'cpuacct.usage': ['34860616']}},
             'memory':
                {'23aed474e6b0281f491c0e598f57a9667f879b1d16c2601f9de588b0347ae55a':
                    {'memory.max_usage_in_bytes': ['835584'],
                    'memory.usage_in_bytes': ['516096']},
                '2483ed35e92d0f10e509ca4cdacf263f05cabf69c09495798af8edf4cd59d43e':
                    {'memory.max_usage_in_bytes': ['835584'],
                    'memory.usage_in_bytes': ['516096']
            }}}

            '''
            for service_name in self.data:
                redis_key = 'RawData_%s_%s_%s' % (self.host_id, self.type_of_data,service_name)
                redis_value = '%s,%s' % (time.time(), json.dumps(self.data[service_name]))
                self.REDIS_OBJ.lpush(redis_key, redis_value)

        elif self.type_of_data == "basic":
            for service_name in self.data:
                redis_key = 'BasicData_%s_%s_%s' % (self.host_id, self.type_of_data,service_name)
                redis_value = '%s,%s' % (time.time(), json.dumps(self.data[service_name]))
                self.REDIS_OBJ.lpush(redis_key, redis_value)

        else:
            pass


class DataOptimization(object):
    def __init__(self, host_or_container_id, settings, REDIS_OBJ):
        self.host_or_container_id = host_or_container_id,
        self.settings = settings,
        self.REDIS_OBJ = REDIS_OBJ

    def get_data(self):
        pass


    def optimize_data(self):
        pass

    def save_data(self):
        pass


    def optimize_avg(self):
        pass
    def optimize_max(self):
        pass
    def optimize_min(self):
        pass