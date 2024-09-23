import urllib.request
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
# 定义请求的URL
url = 'https://d1.weather.com.cn/dingzhi/101280102.html'
url2 = 'http://d1.weather.com.cn/sk_2d/101280102.html'

data1=""
data2=""

# 定义请求头
headers = {
    'Cookie': 'f_city=%E5%8C%97%E4%BA%AC%7C101010100%7C',
    'Host': 'd1.weather.com.cn',
    'Referer': 'http://www.weather.com.cn/'
}

# 创建Request对象
req = urllib.request.Request(url, headers=headers)

# 发送GET请求
with urllib.request.urlopen(req) as response:
    # 读取响应内容
    content = response.read().decode('utf-8')
    c1 = str(content).split("=")[1].split(";")[0]
    cjson = json.loads(c1)
    cs = cjson["weatherinfo"]["cityname"]
    wd = cjson["weatherinfo"]["temp"]
    tq = cjson["weatherinfo"]["weather"]
    fx = cjson["weatherinfo"]["wd"]
    fs = cjson["weatherinfo"]["ws"]
    
    data1 = f"今天天气预报：城市:{cs} 平均温度:{wd} 预计天气:{tq} 风向:{fx} 风速:{fs}"

# 创建Request对象
req2 = urllib.request.Request(url2, headers=headers)
# 发送GET请求
with urllib.request.urlopen(req2) as response:
    # 读取响应内容
    content = response.read().decode('utf-8')
    c1 = str(content).split("=")[1]
    cjson = json.loads(c1)
    wd = cjson["temp"]
    tq = cjson["weather"]
    sd = cjson["SD"]
    pm25 = cjson["aqi_pm25"]
    
    data2 = f" 现在温度:{wd}℃ 现在天气:{tq} 湿度:{sd} PM2.5:{pm25}"


# 定义请求的URL和数据
url = "http://localhost:11434/api/chat"
data = {
    "model": "qwen2.5:1.5b",
    "stream": False,
    "messages": [
        {"role": "system", "content": "你的身份是全能AI助理，你的名字叫缤纷，可以为用户解决任何疑问。"},
        {"role": "user", "content": f"{data1+data2}\n请根据这段数据，不用回应我，直接写一段专业天气预报，并提供贴心的提示"}
    ]
}

# 将数据转换成JSON格式，并编码为字节
json_data = json.dumps(data).encode('utf-8')

# 创建请求对象
req = Request(url, data=json_data, headers={'Content-Type': 'application/json'})

try:
    # 发送请求
    with urlopen(req) as response:
        # 读取响应内容
        the_page = response.read().decode()
        print("Response:", the_page)
        # 尝试解析JSON响应
        try:
            response_data = json.loads(the_page)
            message = response_data.get('message', {}).get('content', '没有找到消息内容')
            print("Message:", message)
        except json.JSONDecodeError:
            print("无法解析响应为JSON格式")
except HTTPError as e:
    # 如果发生HTTP错误，输出错误信息
    print('HTTP Error:', e.code, e.reason)
except URLError as e:
    # 如果发生URL错误（如网络问题），输出错误信息
    print('URL Error:', e.reason)
