import itchat
from itchat.content import *
import time, datetime
import re
import threading
from tuling import getResponse
from jinrishici import getShici


#自动回复开关
SWITCH_REPLY=True
#延迟回复开关
SWITCH_DELAY=False
#延迟时间
DELAY_TIME=120
#消息前缀开关
SWITCH_PREFIX=True
#消息前缀内容
PREFIX_CONTENT="[自动回复]"
#回复内容字典
REPLY_DICT={}
#延迟回复字典
DELAY_REPLY_DICT={}
#定时器开关
TIMER_SEND=False
#定时器时间间隔，单位：秒
TINER_INTERVAL=60
#指定好友自动回复开关
SWITCH_REPLY_SINGLE=False
#指定好友昵称
FRIEND_NAME=""



@itchat.msg_register([TEXT,PICTURE,RECORDING],isGroupChat=False)
def auto_reply(msg):
    global SWITCH_REPLY
    global SWITCH_DELAY
    global DELAY_TIME
    global SWITCH_PREFIX
    global PREFIX_CONTENT
    global REPLY_DICT
    global DELAY_REPLY_DICT
    global TIMER_SEND
    global TIMER_INTERVAL
    global SWITCH_REPLY_SINGLE
    global FRIEND_NAME

    if msg['ToUserName']=='filehelper':
        args=re.compile(' ').split(msg['Text'])
        try:
            if args[0]=='/help':
                reply_content='''
                【功能列表】
                1./help             显示功能列表
                2./switch on        打开自动回复
                3./switch off       关闭自动回复
                4./prefix on        打开消息前缀
                5./prefix off       关闭消息前缀
                6./prefix set [T]   设置前缀内容
                7./delay on         打开延迟回复
                8./delay off        关闭延时回复
                9./delay set [T]    设置延迟时间
                10./dict set [F] [T] 定制好友回复
                11./dict show [F]    显示好友回复
                12./timer on(待续)        打开消息定时器
                13./timer off(待续)       关闭消息定时器
                14./timer to [F](待续)    指定进行定时发送
                15./switch to [F]   指定好友开启自动回复
                '''

            elif args[0]=='/switch':
                if args[1]=='on':
                    SWITCH_REPLY=True
                    reply_content="【系统消息】自动回复已开启"

                elif args[1]=='off':
                    SWITCH_REPLY=False
                    reply_content="【系统消息】自动回复已关闭"

                elif args[1]=='to':
                	if not SWITCH_REPLY:
                		reply_content="请先打开自动回复开关"
                	else:
                		SWITCH_REPLY_SINGLE=True
                		FRIEND_NAME = args[2]
                		reply_content="【系统消息】指定好友自动回复已开启，如需关闭，直接使用关闭自动回复开关"

                else:
                    reply_content="【系统消息】未知指令"

            elif args[0]=='/prefix':
                if args[1]=='on':
                    SWITCH_PREFIX=True
                    reply_content = "【系统消息】回复前缀已开启"

                elif args[1]=='off':
                    SWITCH_PREFIX=False
                    reply_content="【系统消息】回复前缀已关闭"

                elif args[1]=='set':
                    PREFIX_CONTENT="["+args[2]+"]"
                    reply_content = "【系统消息】回复前缀已设置为："+PREFIX_CONTENT

                else:
                    reply_content = "【系统消息】未知指令"

            elif args[0]=='/delay':
                if args[1]=='on':
                    SWITCH_DELAY=True
                    reply_content="【系统消息】延迟回复已开启"

                elif args[1]=='off':
                    reply_content="【系统消息】延迟回复已关闭"

                elif args[1]=='set':
                    DELAY_TIME=args[2]
                    reply_content="【系统消息】延迟时间被设置为："+DELAY_TIME

                else:
                    reply_content = "【系统消息】未知指令"

            elif args[0]=='/dict':
                if args[1]=='show':
                    if REPLY_DICT.__contains__(args[2]):
                        reply_content="【系统消息】好友["+args[2]+"]的自动回复为："+REPLY_DICT[args[2]]
                    else:
                        reply_content="【系统消息】好友["+args[2]+"]的自动回复暂未设置"

                elif args[1]=='set':
                    REPLY_DICT[args[2]]=args[3]
                    reply_content="【系统消息】好友["+args[2]+"的自动回复已设置为："+REPLY_DICT[args[2]]
                else:
                    reply_content = "【系统消息】未知指令"

            elif args[0]=='/timer':
            	if args[1]=='on':
            		#定时器开启代码
            		reply_content = "【系统消息】尚未开发"
            	elif args[1]=='off':
            		#定时器关闭代码
            		reply_content = "【系统消息】尚未开发"

            else:
                reply_content = "【系统消息】未知指令"

        except:
            reply_content="【系统消息】系统异常"
            itchat.send(reply_content, toUserName='filehelper')
            raise

        itchat.send(reply_content, toUserName='filehelper')


    else:
        #获取发送消息的朋友的信息
        target_friend=itchat.search_friends(userName = msg['FromUserName'])
        if target_friend:
            #获取ta的昵称
            nickName=target_friend['NickName']
            if not REPLY_DICT.__contains__(nickName):
                #设置默认回复
                REPLY_DICT[nickName]="(•ω•`) "

            reply_content=REPLY_DICT[nickName]
            #判断自动回复开关
            if SWITCH_REPLY:

            	#判断指定好友回复开关
            	if SWITCH_REPLY_SINGLE and nickName==FRIEND_NAME:
                	print (nickName + "==========" + FRIEND_NAME)
    				#发送消息
                	itchat.send(reply_content + getResponse(msg["Text"])["text"], toUserName=msg['FromUserName'])

                #判断延时回复开关
            	if SWITCH_DELAY:
                	localtime = time.time()
                	DELAY_REPLY_DICT[nickName]=[localtime,msg['FromUserName']]
                	print (DELAY_REPLY_DICT)

            	if not SWITCH_DELAY and not SWITCH_REPLY_SINGLE:
                    #判断消息前缀开关
                	if SWITCH_PREFIX:
                		reply_content = PREFIX_CONTENT + REPLY_DICT[nickName]
                	else:
                		reply_content = REPLY_DICT[nickName]
                    #发送消息
                	itchat.send(reply_content + getResponse(msg["Text"])["text"], toUserName=msg['FromUserName'])



def delay_reply():
    print("开始执行")
    global DELAY_REPLY_DICT
    if SWITCH_DELAY:
        while len(DELAY_REPLY_DICT)>0:
            localtime = time.time()
            # print (localtime)
            # print (DELAY_REPLY_DICT[item][0])
            # print (int(DELAY_TIME))
            for item in list(DELAY_REPLY_DICT.keys()):
                if SWITCH_REPLY:
                    reply_content = item + "," + str(round(int(DELAY_TIME) / 60, 1)) + "分钟过去了，" + REPLY_DICT[item]
                    itchat.send(reply_content, toUserName=DELAY_REPLY_DICT[item][1])
                    # print ("发送消息")
                    del DELAY_REPLY_DICT[item]
            print (DELAY_REPLY_DICT)

    global timer1
    timer1=threading.Timer(DELAY_TIME,delay_reply)
    timer1.start()


def keep_alive():
    text="保持登录"
    itchat.send(text, toUserName="filehelper")
    global timer2
    timer2 = threading.Timer(60*60,keep_alive)
    timer2.start()

# 定时发送信息
# 可以添加指定好友，也可以群发好友
# def timer_send():
#     shici = getShici()
#     users = itchat.search_friends(name='ZWT')
#     userName = users[0]['UserName']
#     itchat.send("今日诗词：" + shici, toUserName = userName)
#     global timer3
#     timer3 = threading.Timer(60, timer_send)
#     timer3.start()

if __name__ == '__main__':
    timer1 = threading.Timer(DELAY_TIME, delay_reply)
    timer1.start()
    timer2=threading.Timer(60*60,keep_alive)
    timer2.start()
    # timer3 = threading.Timer(60, timer_send)
    # timer3.start()
    itchat.auto_login(hotReload=True)
    itchat.send("【系统消息】系统已开启，默认是全部好友就自动回复，指定好友时将关闭全部好友回复", toUserName='filehelper')
    itchat.run()









