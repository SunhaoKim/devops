#实用于二进制装置的kubernetes集群，记得写计划任务（保证kube-apiserver不宕机）
import os,subprocess
apiserver = ('172.18.1.16', '172.18.1.6', '172.18.1.10')
for apiserver_host in apiserver:
    keeplived_status=subprocess.Popen("ssh {apiserver_hosts} sh keeplived.sh".format(apiserver_hosts=apiserver_host),shell=True,stdout=subprocess.PIPE)
    out,err = keeplived_status.communicate()
    for status in out.splitlines():
        print (status)
        if status == '':
            os.system("ssh {apiserver_hosts} docker restart k8s-keepalived".format(apiserver_hosts=apiserver_host))
            os.system("ssh {apiserver_hosts} systemctl start kube-apiserver".format(apiserver_hosts=apiserver_host))
            print("{apiserver_hosts} is down soon restart kubenetes and keepalived".format(apiserver_hosts=apiserver_host))
        else:
            print(apiserver_host + "is UP")
            continue

#keeplived.sh内容：apiserverpid=`ps -ef|grep apiserver|grep -v grep|awk  '{print $2}'`
#echo $apiserverpid
#crontab写法 0 8 * * * /usr/bin/python /root/kube-apiserver-status.py >> /dev/null