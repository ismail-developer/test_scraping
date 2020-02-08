import requests,sys,os

from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText 
from PIL import ImageTk,Image 

def site_code(url):
	i=1
	while i==1:
		try :
			page=requests.get(url)
			i=2
		except:
			print("cant connect the link"+str(url))
			print("try to connect")
			i=1

	if page.status_code !=200:
		print("error response with site you can't continue")
		sys.exit()
	else :
		print("response good you can continue\n")
	return page.content



def info_site_update(source_code):
	if "data" not in os.listdir():
		os.mkdir("data")
	file=open("data/info_product.txt","w")
	url="https://webscraper.io"
	bs=BeautifulSoup(source_code,"html.parser")
	all_item=bs.find_all('div',class_=["col-sm-4","col-lg-4","col-md-4"])
	for i in range(0,len(all_item)):
		img=all_item[i].find_all("img")[0]
		cap=all_item[i].find_all("div",class_="caption")[0]
		cap_a=cap.find_all("h4")
		price_p=str(cap_a[0].text).replace("\n","")
		name_p=str(cap_a[1].text).replace("\n","")
		cap_b=cap.find("p")
		desc_p=str(cap_b.text).replace("\n","")
		src_img_p=str(url+str(img["src"])).replace("\n","")
		print("product number {0}".format(str(i+1)))
		print("\t"+"pic >:"+str(src_img_p))
		print("\t"+"name >:"+str(name_p))
		print("\t"+"price >:"+str(price_p))
		print("\t"+"description >:"+str(desc_p))
		file.write("product number {0}".format(str(i+1))+"\n")
		file.write("\t"+"pic >:"+str(src_img_p)+"\n")
		file.write("\t"+"name >:"+str(name_p)+"\n")
		file.write("\t"+"price >:"+str(price_p)+"\n")
		file.write("\t"+"description >:"+str(desc_p)+"\n")
		
		try:
			req_pic=requests.get(src_img_p)
			print("good requests product"+str(i))
			print(req_pic.status_code)
		except :
			print("no download image product"+str(i))
			print(req_pic.status_code)
		picture=open("data/pic_product_{0}.png".format(str(i+1)),"wb") 
		picture.write(req_pic.content)
		picture.close()
	file.close()

def setup_cmd(url):
	source=site_code(url)
	info_site_update(source)

def setup_gui():
	global url
	global lab_u
	initialize_parameter()
	url=input_url.get()
	if url=="":
		lab_u.config(text="! url not found")
	else :
		lab_u.config(text=url)
		input_url.delete(0,END)
		source=site_code(url)
		info_site_update(source)
		print("-----------------------------")
		res_up()

def res():
	file=open("data/info_product.txt","r").read()
	f=Frame(win)
	area_text=ScrolledText(f,wrap=WORD,height=70,width=120)
	area_text.insert(INSERT,file)
	f.grid()
	area_text.grid()
def res_up():
	global scrollbar
	global frame_a_a_p,area_text
	frame_a_a_p=[]
	area_text=[]
	cnt=0
	file=open("data/info_product.txt","r")
	while True:
		text=file.readline()
		if "product number "in text and text.index('product number ')==0:
			cnt=cnt+1
			frame_a_a_p.append(Frame(frame_a_a))
			frame_a_a_p[-1].grid(column=0,columnspan=10,rowspan=10,sticky=W,pady=6)
			print("podduct number")
		elif "\t"in text and "\tpic >:"in text:
			print("pic")
			name="data/pic_product_{0}.png".format(str(cnt))
			#name="data/bigger.png"
			print(name)
			create_img(frame_a_a_p[-1],name)
		elif "\t"in text and "\tname >:"in text:
			print("name")
			name=text.replace("\t","")
			name=name.replace("name >:","")
			area_text.append(ScrolledText(frame_a_a_p[-1],wrap=WORD,width=50,height=10))
			area_text[-1].insert(INSERT,name)
			area_text[-1].grid(column=3,row=0,columnspan=5,rowspan=3,sticky=W)
		elif "\t"in text and "\tprice >:"in text:
			print("price")
			name=text.replace("\t","")
			name=name.replace("price >:","")
			area_text[-1].insert(INSERT,name)
		elif "\t"in text and "\tdescription >:"in text:
			print("description")
			name=text.replace("\t","")
			name=name.replace("description >:","")
			area_text[-1].insert(INSERT,name)
		else :
			print("break")
			canv.config(yscrollcommand=scrollbar.set)
			scrollbar.config(command=canv.yview)
			frame_a.grid(row=5,column=0,columnspan=5,rowspan=5,pady=10)
			break
def create_img(wind,name):
	global img_c
	#canvas = Canvas(wind, width =200, height=100) 
	#canvas.grid()  
	#img_c.append(ImageTk.PhotoImage(Image.open(name))) 
	#canvas.create_image(20,20, anchor=NW, image=img_c[-1]) 
	img_c.append(PhotoImage(file=name))
	l=Label(wind,image=img_c[-1])
	l.grid(column=0,row=0,columnspan=2,rowspan=2,sticky=N+W)
def initialize_parameter():
	global img_c
	global scrollbar
	global frame_a_a_p,area_text
	frame_a_a_p=[]
	area_text=[]
	img_c=[]
	for i in frame_a_a.winfo_children():
		i.destroy()
	


win=Tk()
win.geometry("800x800+0+0")
#create frame 1  contain 1enter+1button+2result master win
frame=Frame(win)
var_a=StringVar()
var_a.set("https://webscraper.io/test-sites/e-commerce/allinone")
lab_url=Label(frame,text="url",bg="#CBCBCB")
input_url=Entry(frame,textvariable=var_a,width=100)
butt=Button(frame,text="click",command=setup_gui)
lab_u=Label(frame,text="result")

#create frame 2 contain canvas and scrollbar master win
frame_a=Frame(win)
canv=Canvas(frame_a)
scrollbar=Scrollbar(frame_a,orient=VERTICAL,width=16)

#create frame 3 contain result  master canv
frame_a_a=Frame(canv)






# grid frame 1 
frame.grid(column=0,row=0,columnspan=5,rowspan=5,padx=100)
lab_url.grid(column=0,row=0)
input_url.grid(column=1,row=0)
butt.grid(column=1,row=1)
lab_u.grid(column=1,row=2)

#grid frame 2

canv.grid(row=0,column=0,columnspan=3,rowspan=3)
#scrollbar.grid(pady=1,sticky=E)

#grid frame 3
frame_a_a.grid(column=0)

#test

#main gui
win.mainloop()





















#function expired

"""
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
	
	#test dta
	for i in range(0,len(dta)):
		if dta[i].name!=None:
			print("index is >:"+str(i)+" must not none>:"+str(dta[i].name))
		else:
			print("index is "+str(i)+" must none>:"+str(dta[i].name))
			print(dta[i].encode("UTF8"))

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
					src="https://webscraper.io"+j["src"]
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
"""
