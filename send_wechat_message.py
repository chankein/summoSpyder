# -*- coding: utf-8 -*-
import requests
import json
Secret = 'vMYBuJOs2O8U_6i-ahN-lsDhkTXoaun1IkFohKTsr8w'
corpid = 'ww3611e056c6eac6e0'
url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'
#print(url.format(corpid,Secret))
def send_message(message):
    getr = requests.get(url=url.format(corpid,Secret))
    #
    # print(r.json())
    # {'errcode': 0, 'errmsg': 'ok', 'access_token': 't2HxARFMOgge-neHJwYXe4MrIXlFcu2m_Ev1pGQIAcmu-Kt1kQ7pey6jkPfdecqyvvZ9RGb3oSfjL1-lbbp1Y6UGGi8ZjNNd64AALtbR58ot1lh6VjE2ITkiWwgIftwWyryNDw_1AJAtVYYQxKU2O16a7NhHVEdcHG20u8czD-QUDUec1LqI4503OcVGzdR4Cq_4yA6a3fIkVLdQ_u3CHg', 'expires_in': 7200}
    access=getr.json()
    access_token = getr.json().get('access_token')

    print(access)
    # access_token ='t2HxARFMOgge-neHJwYXe4MrIXlFcu2m_Ev1pGQIAcmu-Kt1kQ7pey6jkPfdecqyvvZ9RGb3oSfjL1-lbbp1Y6UGGi8ZjNNd64AALtbR58ot1lh6VjE2ITkiWwgIftwWyryNDw_1AJAtVYYQxKU2O16a7NhHVEdcHG20u8czD-QUDUec1LqI4503OcVGzdR4Cq_4yA6a3fIkVLdQ_u3CHg'

    data = {
            #"touser" : "ChenQiYing|ZhouZengYu|mooncake",
            "touser" : "ChenQiYing",
            "msgtype" : "text",
            "agentid" : 1000002,
            "text" : {
                "content" : message,
                "safe":0}}
    r=requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),data=json.dumps(data))


