from bs4 import BeautifulSoup
import requests
from StringIO import StringIO
from PIL import Image
import errno
import os
import sys
import urllib
import easygui
from time import sleep
from lxml import html


### CONFIG
nGrab = 10 #Number of threads from the front page to search.
nWait = 60 #Seconds between each crawl.
board = "p"#Which imageboard to use.


triggers = [# Triggerwords searched for.
"NY",
"NYC",
"new york",
"big apple",
"manhattan",
"empire state",
"bronx",
"brooklyn",
"queens",
"wall street",
"staten",
"shaolin",
"forgotten borough",
"long island"
]
### END CONFIG


class CaseIns(object):#todo
    def __init__(self, s):
        self.__s = s.lower()
    def __hash__(self):
        return hash(self.__s)
    def __eq__(self, other):
        try:
           other = other.__s
        except (TypeError, AttributeError):
          try:
             other = other.lower()
          except:
             pass
        return self.__s == other

def getThread(page):
    r = requests.get(page)
    data = r.text
    soup = BeautifulSoup(data)
    return soup

def createFilename(url, name, folder):
    dotSplit = url.split('.')
    if name == None:
        slashSplit = dotSplit[-2].split('/')
        name = slashSplit[-1]
    ext = dotSplit[-1]
    file = '{}{}.{}'.format(folder, name, ext)
    return file

def getImage(url, name=None, folder='./'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file = createFilename(url, name, folder)
    if not os.path.isfile(file):
        with open(file, 'wb') as f:
            r = requests.get(url, stream=True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)
        return True
    else:
        return None
def getThreadImages(thread):
    page = requests.get(thread)
    tree = html.fromstring(page.text)
    images = tree.xpath('//div[@class="postContainer replyContainer"]/div[2]/div[3]/a/@href')
    threadID = tree.xpath('//div[@class="post op"]/@id')
    for i in images:
        getImage("https:"+i,None,threadID[0]+'/')


def searchPosts(soup,link):
    tCount = 0
    for i in soup.find_all('blockquote'):
        if any(trigger in str(i.contents) for trigger in triggers):
            print("triggerword located in post "+i.get('id'))
            tCount = tCount + 1
            if i.a is not None:
                print("Quotelink found!")
                quotelink = i.a
                target = quotelink.get('href')
                target = target.replace('#p','')
                target = soup.find("div", id="fT"+target)
                if target is not None:
                    target = target.a
                    target = target.get('href')
                    target = "http:"+target 
                    print("Image found! Attempting to download "+target)
                    if getImage(target) is not None:
                        global count
                        count = count+1
                        global history
                        history.append(link)#Todo
                    else:
                        print("Fail: File already grabbed!")
                else:
                    print("Fail: Referenced post has no image!")
            else:
                print("Fail: Post has no quotelink!")
    if tCount > 2:
        print("3 or more trigger words were located! Grabbing all images...")
        getThreadImages(link)
#        print("Storing thread for next time...") actually unnecessary
#        stored.append(link)


history = []#TODO

stored = []# Stores threads that have multiple instances of trigger words.

def getLinks(n):
    links = []
    home = requests.get('https://boards.4chan.org/'+board+'/')
    tree = html.fromstring(home.text)
    posts = tree.xpath('//div[@class="thread"]/div/div/div[3]/span[4]/span/a/@href')
    for i in posts:
        links.append('https://boards.4chan.org/'+board+'/'+i)
        if posts.index(i) == n-1:
            break
    return links

while True:
    count = 0
    print("Grabbing first "+str(nGrab)+" threads from 4Chan...")
    links = getLinks(nGrab)
    for i in links:
        thread = getThread(i)
        print("Thread "+str(links.index(i)+1)+" retrieved.")
        sleep(1)
        print("Searching its posts...")
        sleep(1)
        searchPosts(thread,i)
    print("Searched first "+str(nGrab)+" threads with "+str(count)+" download attempts.")
    print("Waiting "+str(nWait)+" seconds...")
#    for i in stored:              unnecessary
#        getThreadImages(i)
    sleep(nWait)