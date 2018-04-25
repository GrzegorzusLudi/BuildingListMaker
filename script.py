from PIL import ImageGrab, Image, ImageTk
import re
import time
import tkinter
import threading

scr_width = 1400
scr_height = 500
record_number = 10

max_height = 828
padding = 50
padding_bottom = 150

t_width = int((scr_width-padding*2)/record_number)

#copied from stackoverflow
def getter(widget,file):
    x=root.winfo_rootx()+widget.winfo_x()
    y=root.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save(file)

#returns country of a city in certain year
#All cities appearing in the top 10 in any time must be contained (in other way there's error)
#You MUST also include name of country in the line 94 and place a flag file named for example "Poland.png"
def cou(city,year):
    if(city in ['New York City','Cleveland','Chicago','Pittsburgh','San Francisco','Los Angeles','Dallas','Houston','Atlanta']):
        return 'USA'
    if(city in ['Toronto']):
        return 'Canada'
    if(city in ['Moscow']):
        if(year<1989):
            return 'USSR'
        else:
            return 'Russia'
    if(city=='Hong Kong'):
        if(year<1997):
            return 'Hong Kong, Great Britain'
        else:
            return 'Hong Kong, China'
    if(city=='Pyongyang'):
        return 'North Korea'
    if(city in ['Shenzhen','Shanghai','Tianjin','Beijing','Guangzhou']):
        return 'China'
    if(city in ['Taipei','Kaohsiung']):
        return 'Taiwan'
    if(city in ['Kuala Lumpur']):
        return 'Malaysia'
    if(city in ['Dubai']):
        return 'UAE'
    if(city=='Warsaw'):
        return 'Poland'
    if(city in ['Mecca']):
        return 'Saudi Arabia'
    if(city in ['Seoul']):
        return 'South Korea'
    if(city in ['Kuwait City']):
        return 'Kuwait'

class Record:
	def __init__(self,name,city,height,built,destroyed):
		self.name=name
		self.city=city
		self.height=float(height)
		self.built=int(built)
		self.destroyed=int(destroyed)
	def getString(self,year):
		print(self.city)
		return (self.name+'\t\t\t'+self.city+'\t'+cou(self.city,year)+'\t\t'+str(self.height)+'\t'+str(self.built))

f = open('output.txt', 'r')

#uncomment to make file where all cities to appear ever in top 10 are written, you also have to uncomment lines 140 and 155-157
#f2 = open('buildings.txt', 'w')

records = []
for line in f:
    a = line.replace('\n','').split('\t')
    if(len(a)>4):
        records.append(Record(a[0],a[1],a[2],a[3],a[4]))
    elif(len(a)>3):
        records.append(Record(a[0],a[1],a[2],a[3],"0"))


root = tkinter.Tk()
root.geometry(str(scr_width)+'x'+str(scr_height))
canvas = tkinter.Canvas(root,width=scr_width,height=scr_height)
canvas.pack()

#all flags of countries
flags = {}
for cnt in ['USA','Canada','USSR','Russia','Hong Kong, Great Britain','Hong Kong, China','North Korea','China','Taiwan','Malaysia','UAE','Poland','Saudi Arabia','South Korea','Kuwait']:
	img = Image.open(cnt+".png").resize((t_width-30,int((t_width-30)/2)), Image.ANTIALIAS)
	photo = ImageTk.PhotoImage(img)
	flags[cnt] = photo


def drawGrid(canv,max_height):
	grid_scale_y = 100


	canv.create_rectangle(0,0,scr_width,scr_height,fill="white")

	canv.create_line(padding,padding,padding,scr_height-padding_bottom,fill="black")
	canv.create_line(padding,scr_height-padding_bottom,scr_width-padding,scr_height-padding_bottom,fill="black")
	i = 0
	while i<max_height:
		i+=grid_scale_y
		if(i>max_height):
			i=max_height
		y_pos = scr_height-padding_bottom-(-padding+scr_height-padding_bottom)*i/max_height
		grid_width = 10
		canv.create_line(padding-grid_width/2,y_pos,padding+grid_width/2,y_pos,fill="black")
		canv.create_text(padding-grid_width/2-5,y_pos,anchor="e",fill="black",text=str(i))

buildings = {}
def writeRecord(canv,num,record,year,highest):
	#canv.create_text(scr_width-padding,padding,anchor="ne",text=str(year),font="Arial 20")
	y_pos = scr_height-padding_bottom
	x_pos = padding+(scr_width-padding*2)/record_number/2*(1+num*2)


	canv.create_text(x_pos,y_pos+5,anchor="n",text=record.name,width=t_width)
	canv.create_text(x_pos,y_pos+65,anchor="n",text=record.city,width=t_width)
	canv.create_text(x_pos,y_pos+50,anchor="n",text=str(record.height)+" m",width=t_width)

	canv.create_image(x_pos,y_pos+90,anchor="n",image=flags[cou(record.city,year)])

	#if(record.name not in buildings):

	img = Image.open(record.name+".png")
	scale = (scr_height-padding_bottom-padding)/img.height*record.height/highest
	img = img.resize((int(img.width*scale),int(img.height*scale)))
	photo = ImageTk.PhotoImage(img)
	buildings[record.name] = photo

	canv.create_image(x_pos,y_pos,anchor="s",image=buildings[record.name])

#actualrecords = []
def thread():

	buiinc = []
	records.sort(key=lambda x: x.height, reverse=True)
	time.sleep(2)
	for year in range(1933,2019):
		highest = 1
		print("Tallest buildings in "+str(year))
		recs = []
		i=1
		ind=0
		while(ind<len(records) and i<=record_number):
			r = records[ind]
			if(r.built<=year and (r.destroyed==0 or r.destroyed>year)):
				#if(r not in actualrecords):
				#	actualrecords.append(r)
				#	f2.write(r.name+'\t'+r.city+'\t'+r.city+'\n')
				recs.append(r)
				if i==1:
                                        #you can change it if you wanna scaling to the tallest building in the time
					highest = max_height#r.height
				print(str(i)+"\t"+r.getString(i))
				if(r not in buiinc):
					buiinc.append(r)
				i=i+1
			ind=ind+1

		#draw
		drawGrid(canvas,highest)

		canvas.create_text(scr_width-padding,padding,anchor="ne",text=str(year),font="Arial 20")
		canvas.create_text(10,10,anchor="nw",text="data sources: en.phorio.com, en.wikipedia.org/wiki/List_of_tallest_buildings")

		for i in range(0,10):
			writeRecord(canvas,i,recs[i],year,highest)

                #folder in windows, if you are working on linux, change \\ to /
		getter(canvas,"years\\"+str(year)+".png")
		#time.sleep(1)
		print("\n\n")
	for inc in buiinc:
		print(inc.getString(2017))
	#f2.close()

t = threading.Thread(target=thread)
t.start()
root.mainloop()
