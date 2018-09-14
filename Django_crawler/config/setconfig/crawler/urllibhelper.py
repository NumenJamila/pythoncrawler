import random
import re
from bs4 import Comment
import requests
import sys


class SpiderApi(object):
    user_agents = [
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/43.0.2357.134 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2595.400 QQBrowser/9.6.10872.400",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko)"
        "Chrome/18.0.1025.133 Mobile Safari/535.19"
    ]
    content_type = 'application/x-www-form-urlencoded'
    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    referer = ""

    @classmethod
    def getRequestHeader(cls):
        header = {}
        header['User-Agent'] = cls.user_agents[random.randint(0, len(cls.user_agents) - 1)]
        header['Accept'] = cls.accept
        header['Content-Type'] = cls.content_type
        return header

    @classmethod
    def getBinContent(cls, url):
        """
        获取图片的二进制源码
        :param url: 图片的url
        :return: 二进制源码
        """
        headers = cls.getRequestHeader()
        content = requests.get(url, headers=headers)  # 返回一个Response对象
        print("状态码：{s}".format(s=content.status_code))
        return content

    @classmethod
    def getPageSourceCode(cls, url):
        headers = cls.getRequestHeader()
        html = ""
        try:
            start_html = requests.get(url, headers=headers)  # 返回一个Response对象
            print("状态码：{s}".format(s=start_html.status_code))
            start_html.raise_for_status()
            # response内容的编码
            header_code = start_html.encoding
            # response返回的html header标签里设置的编码
            html_header_code = requests.utils.get_encodings_from_content(start_html.text)
            if header_code == 'ISO-8859-1':
                if html_header_code:
                    html_header_code = html_header_code[0]
                else:
                    html_header_code = start_html.apparent_encoding
                encode_content = start_html.content.decode(html_header_code, 'replace').encode('utf-8', 'replace')
                html = encode_content.decode('utf-8')
            else:
                html = start_html.text
        except:
            print("class SpiderApi.getPageSourceCode()异常信息：{}".format(sys.exc_info()))
        finally:
            return html

    @classmethod
    def getPageSourceCodeByPost(cls, url, dictionary, cookie=None):
        html = ""
        headers = cls.getRequestHeader()
        try:
            if cookie is not None:
                html = requests.post(url, data=dictionary, headers=headers, cookies=cookie)
            else:
                html = requests.post(url, data=dictionary, headers=headers)
            print("状态码：{s}".format(s=html.status_code))
            html.raise_for_status()  # 响应状态码大于400将抛出异常
            content_coding = html.encoding  # 获取响应报文数据部分编码
            # 获取html页面里设置的编码
            page_encoding = requests.utils.get_encodings_from_content(html.text)
            if content_coding == 'ISO-8859-1':
                if page_encoding is not None:
                    page_encoding = page_encoding[0]
                else:
                    page_encoding = html.apparent_encoding
                    encoding_content = html.content.decode(page_encoding, 'replace').encode('utf-8', 'replace')
                    html = encoding_content.decode('utf-8')
            else:
                html = html.text
        except:
            print("异常信息：{exception}".format(exception=sys.exc_info()))
        return html

    @classmethod
    def isWebsite(cls, url):
        picture_re = re.compile(r'((http:|https:).*(png|jpg|doc|xlsx|docx))')
        t = picture_re.match(url)
        if t is not None:
            return False
        else:
            return True

    @classmethod
    def deleteNoise(cls, soup):
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()
        delete_list = ["script", "link", "style", "img", "input",
                       "base", "meta", "br", "iframe", "ul", "ol",
                       "noscript", "button"
                       ]
        item_list = soup.find_all(delete_list)
        for item in item_list:
            item.decompose()


class Urldeal(object):
    filterurls = ["http://www.sciencepublishinggroup.com",
                  "http://www.easychair.org",
                  'https://easychair.org',
                  "http://conf.cnki.net",
                  "http://mp.weixin.qq.com",
                  "http://www.engii.org/RegistrationSubmission/default.aspx"
                  ]

    @staticmethod
    def isVisitable(url):
        available = False
        headers = SpiderApi.getRequestHeader()
        statuscode = -1
        try:
            response = requests.get(url, headers=headers, timeout=10)
            statuscode = response.status_code
            if statuscode == 200:
                available = True
        except:
            print("访问url: {u} 得到状态码为 {code}".format(u=url, code=statuscode))
            print("异常信息：{}".format(sys.exc_info()))
        finally:
            return available

    @staticmethod
    def checkUrlValidity(url):
        url_re = re.compile(r'((http:|https:)//[A-Za-z0-9_/.?="]+)')
        res = url_re.match(url)
        if res is None:
            return False
        else:
            return True

    @classmethod
    def shouldbefilterout(cls, url: str):
        flag = False
        for element in cls.filterurls:
            if url.find(element) >= 0:
                flag = True
                break
        return flag
