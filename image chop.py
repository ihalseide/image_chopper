#!/usr/bin/env python3
# Izak Halseide
# GUI for slicing an image into tiles

import os
import tkinter
from PIL import Image
from tkinter import Tk, Frame, Button, Label, Spinbox, Entry
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import StringVar
from tkinter.font import Font


def iter_with_space(total, size, spacing):
		full_cell = size + spacing
		cell_num = total // full_cell
		for x in range(cell_num):
			begin = x * full_cell
			end = begin + size
			yield begin, end
			
			
# takes name of image file, the tuple size of tiles, and tuple spacing
def chop(filein, path_out, tile_size, spacing):
	if type(filein) != str:
		raise ValueError('%s is no string'%filein)
	elif type(path_out) != str:
		raise ValueError('%s is no string'%path_out)
	elif type(tile_size) != tuple or len(tile_size) != 2:
		raise ValueError('%s is not a tuple of length 2'%tile_size)
	elif type(spacing) != tuple or len(spacing) != 2:
		raise ValueError('%s is not a tuple of length 2'%spacing)
		
	img = Image.open(filein)
	width, height = img.size
	size_x, size_y = tile_size
	space_x, space_y = spacing
	
	os.chdir(path_out)
	for start_x, end_x in iter_with_space(width, size_x, space_x):
		for start_y, end_y in iter_with_space(height, size_y, space_y):
			c = img.crop((start_x, start_y, end_x, end_y))
			name = '%s, %s.png'%(start_x, start_y)
			c.save(name)


class MainApp(Frame):

	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.parent.wm_title('Image Slicer')
		
		self.in_path = StringVar()
		self.out_path = StringVar()
		
		self.tile_width = StringVar()
		self.tile_height = StringVar()
		
		self.space_width = StringVar()
		self.space_height = StringVar()
		
		self.my_font = Font(family='Helvetica', size=10)
		self.my_big_font = Font(family='Helvetica', size=15)
		self.my_bold_font = Font(family='Helvetica', size=10, weight='bold')
		
		self.add_widgets()
		
	def ok(self):
		i = self.in_path.get()
		o = self.out_path.get()
		t = int(self.tile_width.get()), int(self.tile_height.get())
		s = int(self.space_width.get()), int(self.space_height.get())
		chop(i, o, t, s)
		
	def cancel(self):
		self.parent.quit()
		
	def browse(self, to_where):
		if to_where == 'in':
			name = filedialog.askopenfilename(filetypes=(("Portable Network Graphics", "*.png"),("Graphics Interchange Format", "*.gif"),("All files", "*.*")))
			self.in_path.set(name)
		elif to_where == 'out':
			loc = filedialog.askdirectory()
			self.out_path.set(loc)
		else:
			raise ValueError('%s must be "in" or "out"'%to_where)
			
	def change_entry(self):
		in_path = self.in_path.get()
		out_path = self.out_path.get()
		if os.path.isfile(in_path) and os.path.isdir(out_path):
			self.ok_button.configure(state='normal')
			return True
		else:
			self.ok_button.configure(state='disabled')
			return False
			
	def add_widgets(self):		
		# title
		title = Frame(self)
		label = Label(self, text='Image Chopper', font=self.my_big_font)
		label.grid(row=0, column=0, columnspan=4, sticky='nesw')
		
		# input
		in_label = Label(self, text='Input Image:', font=self.my_bold_font)
		in_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
		in_file = Entry(self, textvariable=self.in_path, font=self.my_font, validate='focusout', validatecommand=self.change_entry)
		in_file.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
		in_browse = Button(self, text="Browse...", command=lambda: self.browse('in'), font=self.my_font)
		in_browse.grid(row=1, column=3, padx=5, pady=5, sticky='e')
		
		# size
		size_label = Label(self, text='Tile Size:', font=self.my_bold_font)
		size_label.grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=5)
		lab = Label(self, text='Width:', font=self.my_font)
		lab.grid(row=4, column=0, padx=5, pady=5, sticky='e')
		x_size = Spinbox(self, from_=1, to=1000, textvariable=self.tile_width, font=self.my_font, width=4)
		x_size.grid(row=4, column=1, padx=5, pady=5)
		lab = Label(self, text='Height:', font=self.my_font)
		lab.grid(row=4, column=2, padx=5, pady=5, sticky='e')
		y_size = Spinbox(self, from_=1, to=1000, textvariable=self.tile_height, font=self.my_font, width=4)
		y_size.grid(row=4, column=3, padx=5, pady=5)
		
		# space
		space_label = Label(self, text='Tile Spacing:', font=self.my_bold_font)
		space_label.grid(row=5, column=0, sticky='w', padx=5, pady=5)
		lab = Label(self, text='X Gap:', font=self.my_font)
		lab.grid(row=6, column=0, padx=5, pady=5, sticky='e')
		x_spacing = Spinbox(self, from_=0, to=1000, textvariable=self.space_width, font=self.my_font, width=4)
		x_spacing.grid(row=6, column=1, padx=5, pady=5)
		lab = Label(self, text='Y Gap:', font=self.my_font)
		lab.grid(row=6, column=2, padx=5, pady=5, sticky='e')
		y_spacing = Spinbox(self, from_=0, to=1000, textvariable=self.space_height, font=self.my_font, width=4)
		y_spacing.grid(row=6, column=3, padx=5, pady=5)
		
		# output
		out_label = Label(self, text='Output Folder:', font=self.my_bold_font)
		out_label.grid(row=7, column=0, padx=5, pady=5)
		out_path = Entry(self, textvariable=self.out_path, font=self.my_font, validate='focusout', validatecommand=self.change_entry)
		out_path.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
		out_browse = Button(self, text="Browse...", command=lambda: self.browse('out'), font=self.my_font)
		out_browse.grid(row=7, column=3, padx=5, pady=5, sticky='e')

		# actions
		self.ok_button = Button(self, text='Ok', command=self.ok, font=self.my_font, state='disabled', width=8)
		self.ok_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
		cancel = Button(self, text='Close', command=self.cancel, font=self.my_font, width=8)
		cancel.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky='ew')
	
	
def main():
	root = Tk()
	MainApp(root).pack(side="top", fill="both", expand=True)
	root.mainloop()
	
	
if __name__ == '__main__':
	main()
