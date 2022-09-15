import requests
from lxml import etree
import sys
import random


def _type(a, pages="1"):
    span = "/span[" + pages + "]/text()"
    img = "/img[" + pages + "]/@src"
    if a == "s":
        return '//*[@id="app"]/div[2]/div[' + count + ']/div[last()-1]' + span
    elif a == "i":
        return '//*[@id="app"]/div[2]/div[' + count + ']/div[last()-1]' + img


def _type_div(a, pages="1"):
    span = "/div/span[" + pages + "]/text()"
    img = "/div/img[" + pages + "]/@src"
    if a == "s":
        return '//*[@id="app"]/div[2]/div[' + count + ']/div[last()-1]' + span
    elif a == "i":
        return '//*[@id="app"]/div[2]/div[' + count + ']/div[last()-1]' + img


def random_len(length):
    return random.randrange(int('1' + '0' * (length - 1)), int('9' * length))


count = sys.argv[1]
group_id = ''
url = 'https://qun.qq.com/essence/indexPc?gc=' + group_id + '&seq=' + str(random_len(8)) + '&random=' + str(random_len(10))

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) QQ/9.6.5.28778 '
                  'Chrome/43.0.2357.134 Safari/537.36 QBCore/3.43.1298.400 QQBrowser/9.0.2524.400',
    'Host': 'qun.qq.com',
    # cookie 只需要 p_skey p_uin uin skey
    # p_uin 和 uin QQ号前面有个o不要认成0更不要漏掉
    # cookie样例: p_skey=************************; p_uin=o{qq号}; uin=o{QQ号}; skey=********
    'Cookie': ''
}

response = requests.get(url, headers=header)
response.encoding = 'UTF-8'
data = etree.HTML(response.text)  # 解析

qq_account = data.xpath('//*[@id="app"]/div[2]/div[' + count + ']/div[1]/@style')[0][10:-2].split('/')[5]
print(qq_account)  # 如果只是想要获取 精华信息 将此处注释即可

type_list = []
div_bool = False

for i in [str(i) for i in data.xpath('//*[@id="app"]/div[2]/div[' + count + ']/div[last()-1]/*')]:
    if i[9] in ['i', 's']:
        type_list.append(i[9])
    elif i[9:12] == 'div':
        div_bool = True
        break
if div_bool:
    for i in [str(i) for i in data.xpath('//*[@id="app"]/div[2]/div[' + count + ']/div[last()-1]/div/*')]:
        if i[9] in ['i', 's']:
            type_list.append(i[9])

type_sequence = []
span_sequence, img_sequence = 0, 0

for i in range(len(type_list)):
    if type_list[i] == 's':
        span_sequence += 1
        type_sequence.append("s" + str(span_sequence))
    else:
        img_sequence += 1
        type_sequence.append("i" + str(img_sequence))

if div_bool:
    for i in [_type_div(type_sequence[i][0], type_sequence[i][1]) for i in range(len(type_list))]:
        content = data.xpath(i)[0]
        if len(content) < 11:
            print(content)
        else:
            if content[-10:] == "/thumbnail" and content[:8] == "https://":
                print(content[0:-10])
            else:
                print(content)
else:
    for i in [_type(type_sequence[i][0], type_sequence[i][1]) for i in range(len(type_list))]:
        content = data.xpath(i)[0]
        if len(content) < 11:
            print(content)
        else:
            if content[-10:] == "/thumbnail" and content[:8] == "https://":
                print(content[0:-10])
            else:
                print(content)
