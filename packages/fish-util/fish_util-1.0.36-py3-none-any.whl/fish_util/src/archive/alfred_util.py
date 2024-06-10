#coding:utf-8

import time,sys
from workflow import Workflow


# 写入文本到文件
def write_str(val,path):
    file=open(path,"w")
    file.write(val)
    file.flush()
    file.close()
    print("写入文本到文件成功："+path)

print("hello workflow")

path="/Users/yutianran/Documents/MyObsidian/Cache"
ctime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
ctime_path=time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
str="当前时间为:"+ctime
print(str)
write_str(str,path+"/"+ctime_path+".md")


def say_wf(wf):
     # the list of results for Alfred
     for post in range(10):
         wf.add_item(title=post['description-01'],
                     subtitle=post['href-01'])
     # Send the results to Alfred as XML
     wf.send_feedback()

wf = Workflow()
say_wf(wf)
sys.exit()