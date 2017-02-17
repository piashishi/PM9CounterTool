import pm9
from Tkinter import *           
import tkFileDialog


root = Tk()       

dir_opt = {}
dir_opt['initialdir'] = 'D:/'
dir_opt['mustexist'] = False
dir_opt['parent'] = root
dir_opt['title'] = 'PM 9 Counter Directory'


class counterGui:
	def __init__(self, root):
		self.startTimeLab = Label(root, text="From Time(%Y%m%d%H%M)")
		self.endTimeLab = Label(root, text="End Time(%Y%m%d%H%M)")
		self.starTimeInput = Entry(root)
		self.endTimeInput = Entry(root)
		self.counterLab = Label(root, text="Counter")
		self.counterInput = Entry(root)
		self.dirButton = Button(root, text="PM9 counter directory:", command=self.getDirectory)
		self.dirLabel = Label(root)
		self.showButton = Button(root, text="Parse", state=DISABLED, command=self.parseCounter)
		self.drawButton = Button(root, text="Draw", state=DISABLED, command=self.drawPicture)
		self.counterList = Listbox(root, width=50)
		self.counterList.bind('<<ListboxSelect>>', self.onselect)
		self.scrollbar = Scrollbar(root)
		self.counterList.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.counterList.yview)

		#should iosolate widget and vlue
		self.counterHash = {}
		self.dirName = ""
		self.specificCounter = ""
		self.counter = ""
		self.startTime = ""
		self.endTime = ""

		#layout wigets
		self.layout()

	def getDirectory(self):
		self.dirName = tkFileDialog.askdirectory(**dir_opt)
		self.dirLabel['text'] = self.dirName
		self.showButton['state'] = 'normal'

	def parseCounter(self):
		#clear previous content
		self.counterList.delete(0, END)
		self.drawButton['state'] = 'disabled'

		self.startTime = self.starTimeInput.get()
		self.counter = self.counterInput.get()
		self.endTime = self.endTimeInput.get()
		#brief validation
		if self.startTime == "" or self.endTime == "" or self.counter == "":
			print "startTime, EndTime, counter should not be empty"
			return
		self.counterHash =  pm9.parseCounter(self.dirName, self.startTime, self.endTime, self.counter)
		for key in self.counterHash.keys():
			self.counterList.insert(END, key)


	def onselect(self, evt):
	    # Note here that Tkinter passes an event object to onselect()
	    w = evt.widget
	    index = int(w.curselection()[0])
	    self.specificCounter = w.get(index)
	    self.drawButton['state'] = 'normal'


	def drawPicture(self):
		pm9.draw(self.specificCounter, self.counterHash)


	def layout(self):
		self.startTimeLab.grid(row=0)
		self.starTimeInput.grid(row=0, column=1)
		self.endTimeLab.grid(row=1)
		self.endTimeInput.grid(row=1, column=1)
		self.counterLab.grid(row=2)
		self.counterInput.grid(row=2, column=1)
		self.dirButton.grid(row=3)
		self.showButton.grid(row=3,column=1)
		self.dirLabel.grid(row=4)
		self.counterList.grid(row=5, column=0,sticky=N+S+E+W)
		self.scrollbar.grid(row=5, column=1,sticky=N+S)
		self.drawButton.grid(row=6)

gui = counterGui(root)
root.mainloop()