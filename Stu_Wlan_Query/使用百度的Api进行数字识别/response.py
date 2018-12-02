import re
import os
# import math
import requests
from aip import AipOcr
# import cv2
# from Recognization.recognization import FigureRecognization
# import numpy as np
import settings


url = "%s" % settings.Web_Url
#  模拟登录需要的信息
post_data = {
    "LoginForm[username]": "%s" % settings.User_Name,
    "LoginForm[password]": "%s" % settings.Pass_Word
}
#  添加需要的header
header = {
    "Referer": "https://zfw.xidian.edu.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Cookie": "UM_distinctid=1670b30bf1a0-04ce5786f381ee-4313362-e1000-1670b30bf1c1d8; "
              "PHPSESSID=pqi3qsjkpnn0ppcb7cs1fp52u0; _"
              "csrf=ff19e8342fb7a3c780dfcd0960c3adb6dd492feffced24974e417237db5aa3cfa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_"
              "csrf%22%3Bi%3A1%3Bs%3A32%3A%22UjtrbfcCipdNDL3ip34CHLbFndwRWnzE%22%3B%7D; "
              "BIGipServerzyzfw.xidian.edu.cn=19726090.24610.0000"
}

#  得到随机的验证码 为了模拟登录 需要请求对话
captcha_url = "%s" % settings.Web_Url + "site/captcha?refresh=1&_="
#  异常捕捉
try:
    response = requests.get(captcha_url, headers=header)
except ConnectionError as e:
    print(e)
#  解析content中的内容
img_url = response.json()["url"]

# 匹配验证码的图片并下载
img_url = "%s" % settings.Web_Url + img_url

# 下载图片到本地并保存
img = requests.get(img_url, headers=header).content
img_path = os.path.join(os.getcwd(), "verify_code.png")
with open(r"%s" % img_path, 'wb') as f:
    f.write(img)

# 调用百度的OCR-api识别图片中的数字
APP_ID = "%s" % settings.App_Id
API_KEY = "%s" % settings.API_KEY
SECRET_KEY = "%s" % settings.Secure_Key

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content():
    '''
    读取图片
    :return:
    '''
    with open(img_path, 'rb') as f:
        return f.read()


# 解析出相应的数字
image = get_file_content()
results = client.numbers(image)["words_result"][0]["words"]
if len(results) != 4:
    raise Exception("Validation Code False.")

# # 利用opencv的开源库实现字符的分割 对于粘连的情况仍然不好处理 并且自动的分割方法无法考虑到顺序 不过具有的普遍性更强
# validation_code_gray = cv2.imread("verify_code.png", 0)  # 按灰度图片读取
# # 阈值分割 threshold = 200, 返回 门限ret和处理过后的图片
# ret, validation_code_binarization = cv2.threshold(validation_code_gray, 200, 255, cv2.THRESH_BINARY)
# validation_code_binarization = (255 - validation_code_binarization)
# image, contours, hierarchy = cv2.findContours(validation_code_binarization, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_NONE)
# flag = 0
# for cnt in contours:
#     # 最小的外接矩形
#     x, y, w, h = cv2.boundingRect(cnt)
#     if w*h >= 500:
#         print((x, y, w, h))
#         # 显示图片
#         cv2.imwrite("%sexample%d.jpg" % (settings.Project_Path + settings.Cutout_Path, flag), validation_code_binarization[y:y+h, x:x+w])
#         flag += 1

# # 投影法统计纵向上的像素点个数 因为数字大多按纵向排列 投影法截取出的数字的图片的效果并不好
# # 原因可能是：
# # 1.Mnist的训练集和验证码分割出的图片有差别 分割出的图片大多处于图片的边缘而非中心 二是相邻的字符之间 粘连可能比较大
# # 2.分割出的单张字符多数表现为倾斜
# # 改进方向
# # 1.自建对于验证码的训练集 除了数字外 最好还要有英文字符
# # 2.不对图片进行分割 直接对整个的验证码图片进行目标检测 检测的目标是背景中的数字 字母等字符
# # （检测方法可参考 https://www.zhihu.com/search?type=content&q=%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E5%8F%91%E5%B1%95）
# # #  纵向投影 vertical_projection
# # vertical_projection = [list(validation_code_binarization[..., i]).count(255) for i in range(validation_code_binarization.shape[1])]
# #
# # #  提取验证码中字符的Index stop_flag_list代表间断的index
# # index_list = []
# # for i in range(len(vertical_projection)):
# #     if vertical_projection[i] != 0:
# #         index_list.append(i)
# #     else:
# #         continue
# # flag = 0
# # stop_flag = []
# # for i in range(len(index_list)-1):
# #     if index_list[i] + 1 == index_list[i+1]:
# #         continue
# #     else:
# #         stop_flag.append(index_list[i])
# # stop_flag.insert(0, index_list[0])
# # stop_flag.append(index_list[-1])
# # #  字符切割 根据横向的字符之间的间距来分割字符 宽度分割 高度取整个图片的高度 每个字符的宽度大致相等
# # index = []
# # for i in range(len(stop_flag)-1):
# #     if i == 0:
# #         index.append((stop_flag[0], stop_flag[1]))
# #     else:
# #         index.append((stop_flag[i] + 1, stop_flag[i+1]))
# # #  根据切割出的字符的块数 进行下一步操作
# # width_of_char = []
# # average_threshold = 24
# # if len(index) == 4:
# #     for i in range(len(index)):
# #         # 5*5的卷积核 作高斯平滑
# #         dst = cv2.GaussianBlur(validation_code_binarization[..., index[i][0]:index[i][1]], (5, 5), 0, 0)
# #         image = cv2.resize(dst, (28, 28), interpolation=cv2.INTER_CUBIC)  # 立方插值
# #         cv2.imwrite("%schar%d.png" % (settings.Project_Path + settings.Cutout_Path, i), image)
# # else:
# #     k = 0
# #     for i in range(len(index)):
# #         width_of_char.append(index[i][1]-index[i][0] + 1)
# #     for i in range(len(width_of_char)):
# #         char_count = math.ceil(width_of_char[i] / average_threshold)
# #         width = width_of_char[i]
# #         if char_count > 1:
# #             for j in range(char_count):
# #                 # dst = cv2.GaussianBlur(validation_code_binarization[..., index[i][0] +
# #                 #  j * math.floor(width/char_count)-1:index[i][0] + (j+1)*math.floor(width/char_count)-1], (5, 5), 0, 0)
# #                 image = cv2.resize(validation_code_binarization[..., index[i][0] +
# #                  j * math.floor(width/char_count)-1:index[i][0] + (j+1)*math.floor(width/char_count)-1], (28, 28),
# #                                    interpolation=cv2.INTER_CUBIC)  # 立方插值
# #                 cv2.imwrite("%schar%d.png" % (settings.Project_Path + settings.Cutout_Path, k), image)
# #                 k = k + 1
# #         else:
# #             # dst = cv2.GaussianBlur(validation_code_binarization[..., index[i][0]:index[i][1]], (5, 5), 0, 0)
# #             image = cv2.resize(validation_code_binarization[..., index[i][0]:index[i][1]], (28, 28), interpolation=cv2.INTER_CUBIC)  # 立方插值
# #             cv2.imwrite("%schar%d.png" % (settings.Project_Path + settings.Cutout_Path, k), image)
# #             k = k + 1
# #  字符保存完毕 进行字符的识别
# # for i in range(k):
# #     temp_image = cv2.imread("%schar%d.png" % (settings.Project_Path + settings.Cutout_Path, i), 0)
# #     Input = np.reshape(temp_image, (784, 1))/255
# #     Object = FigureRecognization(Input)
# #     results = Object.result

response_html = requests.get("%s" % settings.Web_Url, headers=header)
html = response_html.text
_csrf = re.findall(r"<meta name=\"csrf-token\" content=\"(.+?)\"", html)[0]

# Post_data中添加_csrf验证
post_data["_csrf"] = _csrf
post_data['LoginForm[verifyCode]'] = results
# 需要进行用户的id和密码的验证 用Post连接比较安全
response_login = requests.post("%s" % settings.Web_Url, data=post_data, headers=header)
html_path = os.path.join(os.getcwd(), "html.txt")
with open(r"%s" % html_path, 'w', encoding='utf-8') as f:
    f.write("%s" % response_login.text)
try:
    package_name = re.findall(r"<td data-col-seq=\"1\">([\u4e00-\u9fa5]*?[A-Za-z0-9]+?)<", response_login.text)[0]
    flow_used = re.findall(r"<td data-col-seq=\"3\">([A-Za-z0-9.]+?)<", response_login.text)[0]
    flow_remained = re.findall(r"<td data-col-seq=\"7\">([A-Za-z0-9.]+?)<", response_login.text)[0]
    charged_remained = re.findall(r"<td data-col-seq=\"8\">([A-Za-z0-9.]+?)<", response_login.text)[0]
    print("套餐名称为：%s 已用流量为：%s\n套餐内剩余流量为：%s 充值流量剩余为：%s" % (package_name, flow_used,
                                                        flow_remained, charged_remained))
except IndexError as e:
    print(e)

