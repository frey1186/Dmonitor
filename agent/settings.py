#_*_coding:utf-8_*_


configs ={
    'HostID': 2,
    "Server": "192.168.1.110",
    "ServerPort": 8000,
    "urls":{

        'get_configs' :['api/monitor/api/client/config','get'],  #acquire all the services will be monitored
        'service_report': ['api/monitor/api/client/service/report/','post'],

    },
    'RequestTimeout':30,
    'ConfigUpdateInterval': 300, #5 mins as default

}


target_dict = {
    "cpuacct":[
        'cpuacct.usage',
        'cpuacct.stat'
    ],
    "memory":[
        'memory.usage_in_bytes',
        'memory.max_usage_in_bytes'
    ],
    "blkio":[
        "blkio.io_service_bytes",
        "blkio.io_queued",
    ]
}