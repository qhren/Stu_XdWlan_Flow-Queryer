import os
import time
import requests
import settings


url = "%s" % settings.Web_Url

#  添加可能需要的header
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


def validation_code_getter(Size):
    #  得到随机的验证码
    for i in range(Size):
        print("正在获取第%d张图片" % (i+1))
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
        img_path = os.path.join("%s" % (settings.Project_Path + settings.Validation_code_path),
                                "verify_code%d.png" % (i + 1))
        with open(r"%s" % img_path, 'wb') as f:  # 写入二进制图片文件
            f.write(img)
        print("第%d张图片保存完毕" % (i + 1))
        time.sleep(1)  # 等待1s


if __name__ == "__main__":
    # 爬取500张图片作为图片分割测试集备用
    size = 500
    validation_code_getter(size)
