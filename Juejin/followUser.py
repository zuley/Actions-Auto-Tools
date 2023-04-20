import requests

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

def formatDynamicList (list):
    print('item', list)
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
                "user_id": item['target_data']['author_user_info']['user_id'],
                "user_name": item['target_data']['author_user_info']['user_name'],
                "time": item['time'],
            }
            # 如果是发布文章，添加文章标题
            if item['target_type'] == 'article':
                return_item['content'] = item['target_data']['article_info']['title']
            # 如果是发布沸点，添加沸点内容
            elif item['target_type'] == 'short_msg':
                return_item['content'] = item['target_data']['msg_Info']['content']
            return_list.append(return_item)
    return return_list


if __name__ == '__main__':
    user_list = get_user_list()
    print(user_list)