import requests,sys

from bs4 import BeautifulSoup
from tkinter import *

def site_code(url):
	page=requests.get(url)
	if page.status_code !=200:
		print("error response with site you can't continue")
		sys.exit()
	else :
		print("response good you can continue\n")
	return page.content


def info_site(source_code):
	bs=BeautifulSoup(source_code,"html.parser")
	dta=[]
	ii=[]
	try :
		a=bs.html.body
		#print(a.prettify)
	except:
		print("you cant access nav")
	contain=a.select(".wrapper")
	contain=contain[0]
	#print(contain)
	for i in contain.children:
		dta.append(i)
	#print(dta)
	#print("len data is >: "+str(len(dta)))
	"""
	#test dta
	for i in range(0,len(dta)):
		if dta[i].name!=None:
			print("index is >:"+str(i)+" must not none>:"+str(dta[i].name))
		else:
			print("index is "+str(i)+" must none>:"+str(dta[i].name))
			print(dta[i].encode("UTF8"))
	"""
	n=0
	m=0
	while n==0:
		if dta[m].name!=None:
			if m==len(dta)-1:
						n=1
			break
			#print(dta[m].name)
			m=m+1
		else :
			#print("delet>:"+str(dta[m].name),end=" ")
			del dta[m]
			#print("deleted")
			m=0
			n=0
	#print("len data is >: "+str(len(dta)))
	#print(dta)
	for i in dta:
		if i.name=="div" and i["class"]==["container","test-site"]:
			s=i
	dta=[]
	for i in s.children:
		dta.append(i)
	for i in dta:
		if i.name=="div" and i["class"]==["row"]:
			s=i
	dta=[]
	for i in s.children:
		dta.append(i)
	for i in dta:
		if i.name=="div" and i["class"]==["col-md-9"]:
			s=i
	dta=[]
	for i in s.children:
		dta.append(i)
	for i in dta:
		if i.name=="div" and i["class"]==["row"]:
			s=i
	dta=[]
	dta_a=[]
	for i in s.children:
		dta.append(i)
	hh=1
	for i in dta:
		if i.name=="div" and i["class"]==["col-sm-4","col-lg-4","col-md-4"]:
			s=i.div
			print("product "+str(hh)+">:")
			hh=hh+1
			for j in s.children:
				if j.name=="img":
					src="https://webscraper.io/test-sites/e-commerce/allinone/"+j["src"]
					print("\t",end="")
					print("pic>:"+str(src))
				if j.name=="div" and j["class"]==["caption"]:
					for h in j.children:
						if h.name!=None:
							dta_a.append(h)
						for k in dta_a:
							try :
								if k.name=="h4" and k["class"]==["pull-right","price"]:
									pass
							except:
								k["class"]=["name"]
							if k.name=="h4" and k["class"]==["name"]:
								name_p=k.a.string
								link_p="https://webscraper.io/test-sites/e-commerce/allinone/"+str(k.a["href"])
								print("\t",end="")
								print("name product is >:"+str(name_p))
								print("\t",end="")
								print("link is>:"+str(link_p))
							if k.name=="h4" and k["class"]==["pull-right","price"]:
								price_p=k.string
								print("\t",end="")
								print("price of product >:"+str(price_p))
							if k.name=="p" and k["class"]==["description"]:
								desc_p=k.string
								print("\t",end="")
								print("desc this product>:"+str(desc_p))
						dta_a=[]

source=site_code("https://webscraper.io/test-sites/e-commerce/allinone")
info_site(source)
