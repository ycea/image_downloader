import requests
from bs4 import BeautifulSoup
from threading import Thread
import re
from time import sleep


class PictureDetective(Thread):
    def  __init__(self, url_on_page: str, base_url, pattern_for_posts,):
        super().__init__()
        # target to collect posts 
        self.url_on_page = url_on_page
        self.pattern_for_posts = pattern_for_posts    
        self.base_url = base_url
    def collect_posts(self):
        soup = make_soup(self.url_on_page)
        posts_list = []
        for post in soup.find_all(href=re.compile(self.pattern_for_posts)):
            post = post.get("href")
            post = absolute_link(post, self.base_url)
            if post is not None:
                posts_list.append(post)
        return posts_list


class ImageGrabber(Thread):
    def __init__(self, list_of_urls, base_url, pattern_for_content, filepath, num=1, attr="href"):
        super().__init__()
        # list of urls to collect image from them 
        self.list_of_urls = list_of_urls
        # special path on site for content, link, that helps to find content
        self.pattern_for_content = pattern_for_content
        # base url to make relative link absolute
        self.base_url = base_url
        # path where conent is will be saved
        self.filepath = filepath
        # num is special id for content files
        self.num = num
        # special attribute to collect  
        slef.attr = attr
    def run(self): # run is method to use threads
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"}
        content_list = []
        for post in self.list_of_urls:
            soup = make_soup(post)
            image = soup.find(href=re.compile(self.pattern_for_content))
            image = image.get("href")
            image = absolute_link(image, self.base_url)
            if image is not None:
                content_list.append(image)
        spec_num = 1
        for i in self.list_of_urls:
            spec_num += self.num
            request = requests.get(i,headers=headers)
            if request.status_code != 200:
                print("SOMETHING WRONG")
            content = request.content
            name = re.sub(r"http\w?://|/", "", i)
            with open(f"{self.filepath}\{spec_num}{name}", "wb") as f:
                f.write(content)
def absolute_link(relative_url: str, base_url: str) -> str:
    if relative_url is not None:
        if not relative_url.startswith('http'):
            absolute_url = base_url + relative_url
            return absolute_url
    return base_url


def delete_duplicates(arr):
    new_arr = []
    for i in arr:
        if i not in new_arr:
            new_arr.append(i)
    return new_arr


def make_soup(url_to_prepare: str):
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"}
    request = requests.get(url_to_prepare, headers=headers)
    html_page = request.content
    html_page = html_page.decode("utf-8")
    soup = BeautifulSoup(html_page, "html.parser")
    return soup

    
