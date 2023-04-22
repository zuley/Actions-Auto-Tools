import os
import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def main ():
    # 获取用户列表
    user_list = get_user_list()
    # 获取最近更新状态，必须满足一小时内发布的文章或者沸点
    latestDynamic = getLatestDynamic(user_list)
    # 如果有最新动态，发送邮件
    if latestDynamic:
        sendDynamicToEmail(latestDynamic)

def get_user_list():
    # 获取用户列表
    baseUrl = 'https://api.juejin.cn/user_api/v1/user/dynamic'
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    params = {
        "aid": 2608,
        "spider": 0,
        "user_id": 852876722177533,
        "cursor": 0,
    }
    user_list = requests.get(baseUrl, headers=headers, params=params).json()
    return formatDynamicList(user_list['data']['list'])

# 格式化数据，将复杂数据结构转化为简单可用数据
def formatDynamicList (list):
    # 遍历 list 生成新的 list
    return_list = []
    for item in list:
        # 判断是否是发布文章或者是发布沸点
        if item['action'] == 0 or item['action'] == 2:
            return_item = {
                # 0: 发布文章 1: 点赞文章，2: 发布沸点，3: 点赞沸点
                "action": item['action'],
                # article: 文章，short_msg: 沸点
                "target_type": item['target_type'],
                "time": item['time'],
                "username": item['user']['user_name'],
            }
            # 如果是发布文章，添加文章标题
            if item['target_type'] == 'article':
                return_item['content'] = item['target_data']['article_info']['title']
            # 如果是发布沸点，添加沸点内容
            elif item['target_type'] == 'short_msg':
                return_item['content'] = item['target_data']['msg_Info']['content']
            return_list.append(return_item)
    return return_list

def getLatestDynamic (DynamicList):
    # 第一条动态
    firstDynamic = DynamicList[0]
    # 当前系统时间
    osTime = time.time()
    # 判断是否是当前系统时间时间一小时内发布的文章或者沸
    # 如果是，返回这条动态，如果否，返回空
    if osTime - firstDynamic['time'] < 3600:
        return firstDynamic
    return None

# 定义一个函数，用于发送邮件
# 使用 SMTP 协议发送邮件
# 发送邮件到指定邮箱
def sendDynamicToEmail(Dynamic):
    subject = '自动化助手：掘金最新动态'
    # 获取 Github Action 里面的环境变量
    sender = os.environ.get('EMAIL_SENDER')
    receiver = os.environ.get('EMAIL_RECEIVER')
    password = os.environ.get('QQ_MAIL_PASSWORD')
    # 设置邮件正文
    message = MIMEText('%s 最近一小时内发布了 %s' % (Dynamic['username'], Dynamic['content']), 'plain', 'utf-8')
    # 设置邮件主题
    message['Subject'] = Header(subject, 'utf-8')
    # 设置发件人
    message['From'] = sender
    # 设置收件人
    message['To'] = Header(receiver, 'utf-8')

    try:
        # 连接SMTP服务器
        smtpObj = smtplib.SMTP('smtp.qq.com', 587)
        # 发送SMTP邮件
        smtpObj.starttls()
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receiver, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)

if __name__ == '__main__':
    main()