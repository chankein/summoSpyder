from utils import readConf
conf, hostname =readConf()
home=conf.get(hostname, 's3_home')
print(home)
