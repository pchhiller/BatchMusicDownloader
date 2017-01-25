from __future__ import print_function
from tinytag import TinyTag
import os
import urllib, re
from bs4 import BeautifulSoup
import urllib2
#os.chdir("F:/Scripts python")
#print (os.getcwd())
file = open("songs.txt", "r")
songs=[]
for line in file:
    line=line.replace(" ","+")
    songs.append(line)
print (songs)   
for name in songs:
    
    name=name.replace("\n","")
    url="http://search.chiasenhac.vn/search.php?s="
    url=url+name
    name=name.replace("+"," ")
    #print (url)
    response = urllib.urlopen(url)
    page_source = response.read()
    soup = BeautifulSoup(page_source,'html.parser')
    #print (soup)
    mydivs = soup.findAll("a", { "class" : "musictitle" })
    #print (mydivs)
    a=mydivs[0]
    a=a.get('href')
    url2="http://chiasenhac.vn/"+a
    url3=url2[:-5]+"_download.html"
    #print(url3)
    response = urllib.urlopen(url3)
    page_source = response.read()
    soup = BeautifulSoup(page_source,'html.parser')
    mydivs = soup.findAll("div", { "id" : "downloadlink" })
    x = (mydivs[0])
    #print x.prettify()
    pattern = re.compile('http:\/\/data[0-9]*\.chiasenhac\.com\/downloads.*(?=mp3)')
    results = re.findall(pattern, str(x))
    #print(results[1])
    try:
        down_link=results[1]+"mp3"
        #print(down_link)
        file_name=name+".mp3"
        #urllib.urlretrieve(down_link,file_name)
        
        
        u = urllib2.urlopen(down_link)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print ("Downloading: %s KiloBytes: %s" % (file_name, file_size/1024))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"  [%3.2f%%]" % ( file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print (status,end=" ")

        f.close()
        tag = TinyTag.get('./'+file_name)
        #print(tag.title)
        directory='./Downloaded/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        name=tag.title+'-'+tag.artist+'.mp3'
        os.rename('./'+file_name,'./Downloaded/'+name)
    except:
       print("Not Found")
