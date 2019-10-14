import requests
from lxml import etree
import time


class TieBa:
    def __init__(self):
        self.tiebaName = input('请输入要爬取的贴吧名字:')
        self.start = int(input('请输入起始页'))
        self.end = int(input('请输入结束页'))
        self.url = 'http://tieba.baidu.com/f?'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

    def loadInfo(self, url):
        # 负责发送请求，返回响应
        response = requests.get(url, headers=self.headers)
        return response

    def get_link_list(self, text, path):
        #负责根据提供的xpath路径获取下一步的链接
        html = etree.HTML(text)
        link_list = html.xpath(path)
        return link_list

    def loadPage(self, url):
        #获取帖子的链接 并发送请求
        text = self.loadInfo(url).text
        link_list = self.get_link_list(text, '//div[@class="t_con cleafix"]/div[2]/div[1]/div[1]/a/@href')
        for link in link_list:
            fullLink = 'http://tieba.baidu.com' + link
            self.loadImage(fullLink)

    def loadImage(self, url):
        #获取图片的链接，并发送请求
        text = self.loadInfo(url).text
        link_list = self.get_link_list(text, '//img[@class="BDE_Image"]/@src')

        for link in link_list:
            if not link.startswith('http://fc-feed'):
                self.writeImage(link)

    def writeImage(self, link):
        #下载图片 保存本地
        image = self.loadInfo(link).content
        filename = link[-10:]
        #以图片链接的后10位作为图片名字
        with open('./images/' + filename, 'wb') as f:
            f.write(image)
            print(filename + '已下载完成')

    def tiebaSpider(self):
        #根据用户的输入爬取指定贴吧的指定页
        for page in range(self.start, self.end + 1):
            pn = (page - 1) * 50
            fullUrl = self.url + f'kw={self.tiebaName}&pn={pn}'
            self.loadPage(fullUrl)


if __name__ == '__main__':
    mySpider = TieBa()
    mySpider.tiebaSpider()
