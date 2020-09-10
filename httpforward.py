#coding=utf-8
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import urllib
from urllib import request

host = ('localhost', 8888)

def myRequest(url):
    #这是代理IP
    # proxy = {'http':'1.1.1.1:18118'}
    # proxy_support = request.ProxyHandler(proxy)
    # opener = request.build_opener(proxy_support)
    opener = request.build_opener()
    #添加User Angent
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36')]
    request.install_opener(opener)
    response = request.urlopen(url)
    html = response.read().decode("utf-8")
    return html

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/favicon.ico":
            url=""
            if '?' in self.path:#如果带有参数
                self.queryString=urllib.parse.unquote(self.path.split('?',1)[1])
            params=urllib.parse.parse_qs(self.queryString)
            url=params["url"][0] if "url" in params else None

            if url:
                html=myRequest(url)
                # print(html)
                self.protocal_version = 'HTTP/1.1'  #设置协议版本
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                if sys.version_info >= (3, 0):
                    html = html.encode("utf-8")
                self.wfile.write(html)   #输出响应内容

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting http server, listen at: %s:%s" % host)
    server.serve_forever()
