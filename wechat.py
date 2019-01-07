#coding=utf-8
import itchat
import requests as rq

msgReply=False

@itchat.msg_register(['Text','Recording','Map','Card','Note','Sharing','Picture','Attachment','Video','Voice','Friends'])
def reply_msg(msg):
    global msgReply
    if msg['Type'] != "Text" :
        if not msg['FromUserName'] == myUserName:
            msg['Text']("tmp/"+msg['FileName'])
            itchat.send_msg(u'%s 发来: \n%s' %(msg['User']['NickName'],msg['FileName']), toUserName=userName)
            if msg['Type'] == "Picture":
                itchat.send_image("tmp/"+msg['FileName'], toUserName=userName)
            elif msg['Type'] == "Video":
                itchat.send_video("tmp/"+msg['FileName'], toUserName=userName)
            else:
                itchat.send_file("tmp/"+msg['FileName'], toUserName=userName)
        return
    if 'start' in msg['Text'] and msg['FromUserName']==userName:
        msgReply=True
        itchat.send_msg(u'自动回复已开启', toUserName=userName)
        return
    elif 'stop' in  msg['Text'] and msg['FromUserName']==userName:
        msgReply=False
        itchat.send_msg(u'自动回复已关闭', toUserName=userName)
        return 
    elif "order" in msg['Text'] and msg['FromUserName'] == orderuserName:
        itchat.send_msg(u'可点菜单: \n' , toUserName=orderuserName)
        return
    elif 'reply' in msg['Text'] and msg['FromUserName']==userName:
        theEnd=msg['Text'].split(" ")[1]
        theNr=msg['Text'].split(" ")[2]
        ReplyUsers=itchat.search_friends(name=theEnd)
        ReplyName=ReplyUsers[0]['UserName']
        itchat.send_msg(theNr,toUserName=ReplyName)
    elif msgReply == False :
        if not msg['FromUserName'] == myUserName:
            itchat.send_msg(u'%s 发来: \n%s' %(msg['User']['NickName'],msg['Text']), toUserName=userName)
    else:
        api_url = 'http://openapi.tuling123.com/openapi/api/v2'
        data = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": str(msg['Content'].encode('utf8'))
                }
            },
            "userInfo": {
                "apiKey": "yourkey",
                "userId": "123"
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'Host': 'openapi.tuling123.com',
            'User-Agent': 'Mozilla/5.0 (Wi`ndows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 '
                          'Safari/537.36 '
        }
        result = rq.post(api_url, headers=headers, json=data).json()
        itchat.send_msg(result['results'][0]['values']['text'], msg['FromUserName'])
        
if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2,hotReload=True)
    orderusers=itchat.search_friends(name=u'Cookie')
    orderuserName=orderusers[0]['UserName']
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    users=itchat.search_friends(name=u'爱吃cookie的猪')
    userName= users[0]['UserName']
    itchat.run()
