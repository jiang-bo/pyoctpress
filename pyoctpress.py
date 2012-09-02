#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urlparse, gzip, time, sys, getopt
from BeautifulSoup import BeautifulSoup
from xml.dom import minidom

AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.82 Safari/537.1'
CSDN_BLOG='http://blog.csdn.net'


class Post:
    def __init__(self, title, url, date, categories, content):
	self.title=title.strip()
	self.url=url
	self.date=date
	self.categories=categories.strip()
	self.content=content.strip()
	self.layout='post'
	self.tags=''
	
    def toMdDoc(self):
	mdfilename=time.strftime('%Y-%m-%d',self.date) +'-'+self.url+'.html'
	mdf=open(mdfilename,'w')

	mdcontent=u'---\n'+'layout: \'' + self.layout+'\'\n' + u'title: \'' + self.title+u'\'\n' + u'categories: \'' + self.categories+u'\'\n' + u'tags: \'' + self.tags + u'\'\n' + u'---\n' + self.content
	mdf.write(mdcontent.encode('utf-8'))
	mdf.close()

class ItemParser:
    def __init__(self, item):
	self.item=item

    def parse(self):
	title = self.__getElementByTag('title')
	date = time.strptime(self.__getElementByTag('wp:post_date'),'%Y-%m-%d %H:%M:%S')
	content = self.__getElementByTag( 'content:encoded')
	categories =self.__getElementByTag( 'category')

	return Post(title, 'post', date, categories, content)

    

    def __getElementByTag(self,tagName):
	if self.item.getElementsByTagName(tagName).length>0:
	    return self.item.getElementsByTagName(tagName)[0].firstChild.data.strip()
	else:
	    return ''


def parseFormWp():

    filename=raw_input('wordpress.xml file path: ')
    xmldoc=minidom.parse(filename)
    itemlist=xmldoc.getElementsByTagName('item')
    posts={}
    i=0
    for it in itemlist:
	if it.getElementsByTagName('wp:post_type')[0].firstChild.data.strip()=='post':
	    posts[i]=ItemParser(it).parse()
	    i +=1

    return posts

def getPostlistFormCSDN():
    username=raw_input('CSDN username: ')
    request=urllib2.Request(CSDN_BLOG + '/'+username+'/article/list/10000')
    request.add_header('User-Agent', AGENT)
    opener=urllib2.build_opener()
    f=opener.open(request)
    blist=f.read()
    f.close()
    soup=BeautifulSoup(''.join(blist),fromEncoding='UTF-8')
    postlist={}
    i=0
    for st in soup.find(id='article_list').findAll('span',{'class':'link_title'}):
	tag=st.find('a')
	postlist[i]=getPostFromCSDN(tag['href'])
	i +=1

    return  postlist

def getPostFromCSDN(url):
    request=urllib2.Request(CSDN_BLOG+url)
    request.add_header('User-Agent', AGENT)
    opr=urllib2.build_opener();
    f=opr.open(request)
    blog=f.read()
    f.close()
    soup=BeautifulSoup(''.join(blog),fromEncoding='UTF-8')

    date=time.strptime(soup.find('span',{'class':'link_postdate'}).string,'%Y-%m-%d %H:%M')
    title=soup.find('span',{'class':'link_title'}).find('a').string
    categoryTag=soup.find('span',{'class':'link_categories'})
    category=''
    if categoryTag != None:
	category = categoryTag.find('a').string
    content=soup.find('div', {'class':'article_content'}).prettify()
    url=url.split('/')[-1]

    return Post(title, url, date, category, content.decode('utf-8'))



def usage():
    print 'Usage: python '+sys.argv[0]+' -t {type}'
    print 'Args:'
    print '\t -t: type, avalialbe value is : \'csdn\' for csdn blog, \'wp\' for wordpress'

if __name__ == '__main__':
    try:
	opts, args = getopt.getopt(sys.argv[1:], 't:')
    except:
	usage()
	sys.exit(2)
    blogType='wp'
    for	a, v in opts:
	if a=='-t':
	    blogType=v
    print blogType
    posts={}
    if blogType=='wp':
	posts=parseFormWp()
    elif blogType=='csdn':
	posts=getPostlistFormCSDN()
    else:
	print 'We support wordpress and csdn blog now only!'
	usage()
	sys.exit(2)
    for p in posts:
	posts[p].toMdDoc()

