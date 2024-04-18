# encoding:utf-8
import random
import re
import requests
import json
from bot.bot import Bot
from bridge.reply import Reply, ReplyType
from datetime import datetime
from config_xyy import WX_URL  # 微信机器人去请求拿到链接数据

def get_shortvideo(search_key):
    url = "{}/rtb_search/search/an_interesting_short_play/".format(WX_URL)  # 公网
    # url = "http://192.168.31.95:5000/rtb_search/search/an_interesting_short_play/"

    payload = {'keyword': search_key}
    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)
    result_list = response.json().get("data", [])
    # result_list = [
    #     {
    #     "title": "某个剧的标题1",
    #     "url": "testulr1",
    #     },
    #     {
    #     "title": "某个剧的标题2",
    #     "url": "testulr2",
    #     },
    #
    # ]
    # result_list = []
    string = "\n点击夸克网盘链接后app打开,转存后观看完整版\n共计找到相似剧目：{} 部\n".format(len(result_list))
    if result_list:
        for each in result_list:
            justring = "\n{title}\n{url}\n".format(title=each["title"], url=each["url"])
            string = string+justring
    else:
        string = string + "\n抱歉，剧名「{}」未找到相关资源，请尝试其他的吧.".format(search_key)
    return string

# 转换时长
def get_duration_str(seconds: float, like: str = "%02d:%02d:%02d"):
    """
    71  -> 01:11
    """
    m, s = divmod(float(seconds), 60)
    h, m = divmod(m, 60)
    # print(like % (h, m, s))
    if not seconds:
        return ""
    return like % (h, m, s)


def get_shipinghao(video_id,pass_ticket):

    url = "https://mp.weixin.qq.com/recweb/videolistapi?action=getvideoinfo&feed_id=finder_{video_id}&channelid=699001&pass_ticket={pass_ticket}".format(video_id=video_id,pass_ticket=pass_ticket)

    payload = {}
    headers = {
        'Host': 'mp.weixin.qq.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/5{}.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) MacWechat/3.8.5(0x13080510) XWEB/1100 Flue'.format(random.choice(range(10,90))),
        'x-requested-with': 'XMLHttpRequest',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'zh-CN,zh;q=0.9',
        'Cookie': 'pac_uid=0_42dfe723d711d'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    inf = response.json()
    description = inf.get("data", {}).get("description", "").replace("'","[").replace('"',"[").replace('“',"[").replace('”',"]")
    publish_time = datetime.fromtimestamp(inf.get("data", {}).get("publish_time", "")).strftime("%Y-%m-%d %H:%M:%S")
    source = inf.get("data", {}).get("source", "")
    if inf.get("data", {}).get("resolution_list", []):
        play_url = inf.get("data", {}).get("resolution_list", [])[0]["url"]
        duration = get_duration_str(inf.get("data", {}).get("resolution_list", [])[0]["duration"]/1000)
    else:
        play_url = "该视频无法获取播放地址"
        duration = ""
    wx_url = "https://mp.weixin.qq.com/recweb/clientjump?feed_id=finder_{video_id}&tag=getvideolist&channelid=699001".format(video_id=video_id)
    return description, publish_time, source, play_url, duration,wx_url


# ZHIDINGYIBot Unit对话接口 (可用, 但能力较弱) # 自己定义的对话
class ZHIDINGYIBot(Bot):
    def reply(self, query, context=None, pass_ticket=""):
        vid = "".join(re.findall(r'<objectId><!\[CDATA\[(\d*)\]',context.kwargs.get("msg",{})["Content"])) or "".join(re.findall(r'<objectId>(\d*)</objectId>',context.kwargs.get("msg",{})["Content"]))
        # reply = Reply(ReplyType.TEXT,vid)

        if vid:
            print("vid--->",vid)
            description, publish_time, source, play_url, duration, wx_url = get_shipinghao(video_id=vid,pass_ticket=pass_ticket)
            string = "标题:{description}\n发布时间:{publish_time}\n作者:{source}\n时长:{duration}\n可播放地址:{play_url}\n微信可打开地址:{wx_url}".format(description=description, publish_time=publish_time, source=source,
                                                   play_url=play_url, duration=duration, wx_url=wx_url)
            reply = Reply(ReplyType.TEXT, string)
        else:
            string = get_shortvideo(context)
            reply = Reply(ReplyType.TEXT, string)
        return reply

    def get_token(self):
        access_key = 'YOUR_ACCESS_KEY'
        secret_key = 'YOUR_SECRET_KEY'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + access_key + '&client_secret=' + secret_key
        response = requests.get(host)
        if response:
            print(response.json())
            return response.json()['access_token']

if __name__ == '__main__':
    inf = get_shortvideo("sadfadf")
    print(inf)