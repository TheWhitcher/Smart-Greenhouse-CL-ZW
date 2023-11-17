# Name:     GreenHouseGUI.py
# By:       Christophe Landry & Zacharyah Whitcher
# Date:     2023-04-28
# Version:  1.0

# Imports
from tkinter import *

# Application Class
class Application(Frame):
	def __init__(self, master):
		super(Application, self).__init__(master)
		self.grid()
		self.create_widgets()
		
	# Creates all widgets on the GUI
	def create_widgets(self):
		# Labels
		self.titleLabel = Label (self, text="Welcome to the Greenhouse!", font='Helvetica 20 bold')
		self.presetLabel = Label (self, text="Strawberry Preset Selected", font='Helvetica 16')

		self.tempLabel = Label (self, text="Temperature", font='Helvetica 10 bold')
		self.soilLabel = Label (self, text="Soil Moisture",font='Helvetica 10 bold')
		self.uvLabel = Label (self, text="UV Light", font='Helvetica 10 bold')

		self.maxLabel = Label (self, text="Max", font='Helvetica 10 bold')
		self.minLabel = Label (self, text="Min", font='Helvetica 10 bold')
		self.actualLabel = Label (self, text="Actual", font='Helvetica 10 bold')

		self.tempMax = Label (self, text="22.0", font='Helvetica 10 bold')
		self.soilMax = Label (self, text="90", font='Helvetica 10 bold')
		self.uvMax = Label (self, text="100", font='Helvetica 10 bold')

		self.tempMin = Label (self, text="21.0", font='Helvetica 10 bold')
		self.soilMin = Label (self, text="70", font='Helvetica 10 bold')
		self.uvMin = Label (self, text="30", font='Helvetica 10 bold')

		self.tempActual = Label (self, text="0.0", font='Helvetica 10 bold')
		self.soilActual = Label (self, text="0.0", font='Helvetica 10 bold')
		self.uvActual = Label (self, text="0.0", font='Helvetica 10 bold')

		# Buttons
		self.preset1 = Button (self, text="Strawberry", font='Helvetica 14 bold', bg="green", fg="#BBFF83")
		self.preset2 = Button (self, text="Cucumber", font='Helvetica 14 bold', bg="red", fg="#FFC8E9")
		self.preset3 = Button (self, text="Tomato", font='Helvetica 14 bold', bg="red", fg="#FFC8E9")

		# Component Placement
		# Labels
		self.titleLabel.grid(row=0, columnspan=5)
		self.presetLabel.grid(row=1, columnspan=5)

		self.minLabel.grid(row=4, column=1)
		self.maxLabel.grid(row=4, column=2)
		self.actualLabel.grid(row=4, column=3)

		self.tempLabel.grid(row=5, column=0)
		self.soilLabel.grid(row=6, column=0)
		self.uvLabel.grid(row=7, column=0)
		
		self.tempMin.grid(row=5, column=1)
		self.soilMin.grid(row=6, column=1)
		self.uvMin.grid(row=7, column=1)

		self.tempMax.grid(row=5, column=2)
		self.soilMax.grid(row=6, column=2)
		self.uvMax.grid(row=7, column=2)

		self.tempActual.grid(row=5, column=3)
		self.soilActual.grid(row=6, column=3)
		self.uvActual.grid(row=7, column=3)

		#Buttons
		self.preset1.grid(row=2, column=1)
		self.preset2.grid(row=2, column=2)
		self.preset3.grid(row=2, column=3)
		
		# Component Configuration
		# Buttons
		self.preset1.config(command=lambda: self.btn1(self.preset2, self.preset3, self.presetLabel, self.tempMax, self.tempMin, self.soilMax, self.soilMin, self.uvMax, self.uvMin))
		self.preset2.config(command=lambda: self.btn2(self.preset1, self.preset3, self.presetLabel, self.tempMax, self.tempMin, self.soilMax, self.soilMin, self.uvMax, self.uvMin))
		self.preset3.config(command=lambda: self.btn3(self.preset1, self.preset2, self.presetLabel, self.tempMax, self.tempMin, self.soilMax, self.soilMin, self.uvMax, self.uvMin))

		
	# Load Preset 1
	def btn1(self, button2, button3, name, tMax, tMin, sMax, sMin, lMax, lMin):
		preset = ("24.0", "15.0", "90", "70", "100", "30")

		# Set button colors
		self.preset1.config(bg="green", fg="#BBFF83")
		button2.config(bg = "red", fg = "#FFC8E9")
		button3.config(bg = "red", fg = "#FFC8E9")

		# Set preset name
		name.config(text = "Strawberries preset selected")

		# Set preset values
		tMax.config(text = preset[0])
		tMin.config(text = preset[1])
		sMax.config(text = preset[2])
		sMin.config(text = preset[3])
		lMax.config(text = preset[4])
		lMin.config(text = preset[5])
		

	# Load Preset 2
	def btn2(self, button1, button3, name, tMax, tMin, sMax, sMin, lMax, lMin):
		preset = ("29.0", "26.0", "70", "60", "100", "50")

		# Set button colors
		self.preset2.config(bg="green", fg="#BBFF83")
		button1.config(bg = "red", fg = "#FFC8E9")
		button3.config(bg = "red", fg = "#FFC8E9")

		# Set preset name
		name.config(text = "Cucumber preset selected")

		# Set preset values
		tMax.config(text = preset[0])
		tMin.config(text = preset[1])
		sMax.config(text = preset[2])
		sMin.config(text = preset[3])
		lMax.config(text = preset[4])
		lMin.config(text = preset[5])
			
	# Load Preset 3
	def btn3(self, button1, button2, name, tMax, tMin, sMax, sMin, lMax, lMin):
		preset = ("27.0", "21.0", "85", "60", "100", "50")

		# Set button colors
		self.preset3.config(bg="green", fg="#BBFF83")
		button1.config(bg = "red", fg = "#FFC8E9")
		button2.config(bg = "red", fg = "#FFC8E9")

		# Set preset name
		name.config(text = "Tomato preset selected")

		# Set preset values
		tMax.config(text = preset[0])
		tMin.config(text = preset[1])
		sMax.config(text = preset[2])
		sMin.config(text = preset[3])
		lMax.config(text = preset[4])
		lMin.config(text = preset[5])
        
# Create GUI for testing ##
#root=Tk()
#root.title('Greenhouse GUI')
#root.geometry('465x210')
#app = Application(root)
#app.mainloop()
