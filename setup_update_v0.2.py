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
	global lab_r_u
	initialize_parameter()
	url=input_url.get()
	if url=="":
		lab_r_u.config(text="! url not found")
	else :
		lab_r_u.config(text=url)
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
	f.pack()
	area_text.pack()
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
			frame_a_a_p.append(Frame(frame_canv_i))
			frame_a_a_p[-1].pack(pady=10,expand=TRUE,padx=2)
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
			area_text[-1].pack(side="left")
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
			frame_a.pack()
			break
def create_img(wind,name):
	global img_c
	#canvas = Canvas(wind, width =200, height=100) 
	#canvas.pack()  
	#img_c.append(ImageTk.PhotoImage(Image.open(name))) 
	#canvas.create_image(20,20, anchor=NW, image=img_c[-1]) 
	img_c.append(PhotoImage(file=name))
	l=Label(wind,image=img_c[-1])
	l.pack(side="left")
def initialize_parameter():
	global img_c
	global scrollbar
	global frame_a_a_p,area_text
	frame_a_a_p=[]
	area_text=[]
	img_c=[]
	for i in frame_canv_i.winfo_children():
		i.destroy()
	


win=Tk()
win.geometry("800x800+0+0")
#create frame  about label,entry,button and result
frame=Frame(win)
frame_url=Frame(frame)
frame_butt=Frame(frame)
frame_r_u=Frame(frame)

var_a=StringVar()
var_a.set("https://webscraper.io/test-sites/e-commerce/allinone")
lab_url=Label(frame_url,text="url",bg="#CBCBCB")
input_url=Entry(frame_url,textvariable=var_a,width=100)
butt=Button(frame_butt,text="click",command=setup_gui)
lab_r_u=Label(frame_r_u,text="result")



#create frame 2 contain canvas and scrollbar master win
frame_a=Frame(win)

frame_a_scr=Frame(frame_a)
scrollbar=Scrollbar(frame_a_scr,orient=VERTICAL,width=16)

frame_a_canv=Frame(frame_a)
canv=Canvas(frame_a_canv)
scrollbar.config(command=canv.yview)

#create frame 3 contain result  master canv
frame_canv_i=Frame(canv)










# pack frame 1 
frame.pack()
#pack frame url
frame_url.pack(fill="x",expand="true",padx=10,pady=10)
#pack frame button
frame_butt.pack(fill="x",expand="true",padx=10,pady=10)
#pack frame result about url
frame_r_u.pack(fill="x",expand="true",padx=10,pady=10)

lab_url.pack(side="left")
input_url.pack(side="left")
butt.pack()
lab_r_u.pack()

#pack frame 2
frame_a.pack(fill="both",expand="true")

#pack frame scroll
frame_a_scr.pack(side=RIGHT,fill=Y,expand=TRUE)

#pack frame canv 
frame_a_canv.pack(side="left",fill="both",expand="true")

scrollbar.pack(fill="y",expand="true")
canv.pack(fill="both",expand="true")
frame_canv_i.pack(fill="both",expand=TRUE)

frame_canv_i.bind("<Configure>",
	lambda e: canv.configure(scrollregion=canv.bbox("all")
	))

canv.create_window((0,0),window=frame_canv_i)
canv.configure(yscrollcommand=scrollbar.set)


#test

#main gui
win.mainloop()





