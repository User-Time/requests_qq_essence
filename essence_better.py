import requests
from lxml import etree
import sys
import random
import os
import time


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


def download_image(url, count, index):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if not os.path.exists('img'):
                os.makedirs('img')
            
            ext = url.split('.')[-1]
            filename = f'img/{count}.{ext}'
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
        return False
    except Exception as e:
        print(f"Download failed: {e}")
        return False


if __name__ == "__main__":
    start_count = 1
    end_count = 1000 #qq群精华上限为1000条，不会更多了
    
    with open('JH.txt', 'w', encoding='utf-8') as f:
        for current_count in range(start_count, end_count + 1):
            count = str(current_count)
            
            group_id = '******'
            url = 'https://qun.qq.com/essence/indexPc?gc=' + group_id + '&seq=' + str(random_len(8)) + '&random=' + str(random_len(10))
            
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) QQ/9.6.5.28778 '
                              'Chrome/43.0.2357.134 Safari/537.36 QBCore/3.43.1298.400 QQBrowser/9.0.2524.400',
                'Host': 'qun.qq.com',
                'Cookie': 'p_skey=*****; p_uin=o{qq号}; uin=o{qq号}; skey=*****'
            }
            
            try:
                response = requests.get(url, headers=header, timeout=10)
                response.encoding = 'UTF-8'
                data = etree.HTML(response.text)
                
                # 获取QQ账号
                try:
                    qq_account = data.xpath('//*[@id="app"]/div[2]/div[' + count + ']/div[1]/@style')[0][10:-2].split('/')[5]
                except:
                    qq_account = "Unknown"
                
                # 写入文件
                f.write(f"=== count={count} ===\n")
                f.write(f"QQ Account: {qq_account}\n\n")
                
                type_list = []
                div_bool = False
                
                try:
                    elements = [str(i) for i in data.xpath('//*[@id="app"]/div[2]/div[' + count + ']/div[last()-1]/*')]
                    for i in elements:
                        if i[9] in ['i', 's']:
                            type_list.append(i[9])
                        elif i[9:12] == 'div':
                            div_bool = True
                            break
                    
                    if div_bool:
                        sub_elements = [str(i) for i in data.xpath('//*[@id="app"]/div[2]/div[' + count + ']/div[last()-1]/div/*')]
                        for i in sub_elements:
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
                    
                    image_urls = []
                    
                    if div_bool:
                        for i in [_type_div(type_sequence[i][0], type_sequence[i][1]) for i in range(len(type_list))]:
                            try:
                                content = data.xpath(i)[0]
                                if len(content) < 11:
                                    f.write(content + "\n")
                                else:
                                    if content[-10:] == "/thumbnail" and content[:8] == "https://":
                                        cleaned_content = content[0:-10]
                                        f.write(cleaned_content + "\n")
                                        image_urls.append(cleaned_content)
                                    else:
                                        f.write(content + "\n")
                            except Exception as e:
                                f.write(f"Error processing element: {e}\n")
                    else:
                        for i in [_type(type_sequence[i][0], type_sequence[i][1]) for i in range(len(type_list))]:
                            try:
                                content = data.xpath(i)[0]
                                if len(content) < 11:
                                    f.write(content + "\n")
                                else:
                                    if content[-10:] == "/thumbnail" and content[:8] == "https://":
                                        cleaned_content = content[0:-10]
                                        f.write(cleaned_content + "\n")
                                        image_urls.append(cleaned_content)
                                    else:
                                        f.write(content + "\n")
                            except Exception as e:
                                f.write(f"Error processing element: {e}\n")
                    
                    # 下载图片
                    for idx, img_url in enumerate(image_urls):
                        success = download_image(img_url, count, idx+1)
                        if success:
                            print(f"Downloaded image {idx+1} for count {current_count}")
                        else:
                            print(f"Failed to download image {idx+1} for count {current_count}")
                            
                    f.write("\n")
                    
                except Exception as e:
                    f.write(f"=== count={count} 处理失败 ===\n")
                    f.write(f"错误信息: {str(e)}\n\n")
                    print(f"count={count} 处理失败: {str(e)}")
                
                # 随机延迟防止被封
                time.sleep(random.uniform(0.1, 0.2))
                
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
                continue