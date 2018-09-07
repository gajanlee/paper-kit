import logging, os, time
import threading
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR,    #控制台打印的日志级别
                    filename='error.log',
                    filemode='w',   #模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )


def reference_parser(acm_id):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',}
    resp = requests.get("https://dl.acm.org/tab_references.cfm?id=3041126&type=article&usebody=tabbody&_cf_containerId=cf_layoutareareferences&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=B3784D84B18E700C2A1B3F5D025EF4A6&_cf_rc=1", headers=headers)  # ACM will return HTML code by this url
    trs = BeautifulSoup(resp.text, "html").find_all("tr")
    # tr's last td.div.text is reference text
    MIN, MAX = 81, 133
    with open("papers.txt", "w") as fp:
        for i, tr in enumerate(trs, 1):
            if not MIN <= i <= MAX: continue
            fp.write(tr.find_all("td")[-1].text.strip() + "\n")


def downloader(urls, save_path, paper_name, num=""):
    logger = logging.getLogger("download_log")

    done = False
    for url in urls:
        try:
            resp = requests.get(url)
            with open(os.path.join(save_path, (str(num)+"." if num else "")+paper_name+".pdf"), "wb") as fp:
                fp.write(resp.content)
            # logger.info("%s done" % (paper_name))
            print("%s done" % (paper_name))
            done = True; break
        except:
            pass
    
    if not done:
        # logger.error("%s download error!" % paper_name)
        logger.error("{num}, {name}, {url_count}".format(num=num, name=paper_name, url_count=len(urls)))

def download(paper_names):
    threadings = []

    for i, name in enumerate(paper_names):
        t = Download_Threading(name, 81+i)
        threadings.append(t)
        t.start()

class Download_Threading(threading.Thread):
    def __init__(self, paper_name, paper_num=0):
        super(Download_Threading, self).__init__()
        self.paper_name = paper_name
        self.paper_num = paper_num
    
    def run(self):
        spider = BaiduPaperSpider("./data")
        spider.download(self.paper_name, self.paper_num)


class BaiduPaperSpider:

    def __init__(self, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        self.save_dir = dest_dir
    
    def download(self, paper_name, num=0):
        download_links = self.get_links(paper_name)
        downloader(download_links, self.save_dir, paper_name, num)
    
    def get_links(self, paper_name):
        resp = requests.get("http://xueshu.baidu.com/s?wd=" + paper_name + "&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=1&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=2")
        tags = BeautifulSoup(resp.text, "html").find_all("span", class_="dl_item_span")
        return [tag.a["href"].strip() for tag in tags if ".pdf" in tag.a["href"]]


#reference_parser(0)
#BaiduPaperSpider("./data").download("Lexicalized Markov grammars for sentence compression.")
def start():
    with open("paper_names.txt") as fp:
        download([line.strip() for line in fp])

start()
