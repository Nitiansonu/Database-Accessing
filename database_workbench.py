from Tkinter import *
import ttk
import tkMessageBox


import mysql.connector
from mysql.connector import errorcode

#import psycopg2

from pymongo import MongoClient
import pymongo

class Application:

	def __init__(self,parent):

		self.parent=parent		
		self.parent.minsize(width=690,height=600)
		self.parent.geometry("%dx%d+%d+%d"%( 800,600, (self.parent.winfo_screenwidth()-800)/2, (self.parent.winfo_screenheight()-600)/2) )

		self.parent_frame=Frame(self.parent,width=800,height=600,bg="red")
		self.parent_frame.pack(fill=BOTH,expand =YES)
		self.parent_frame.bind('<Configure>',self.resize_handler)		
		
		
		self.initialize_widgets()

	def initialize_widgets(self):

#-----------------------------------------------------------------------------------------------

		self.top_frame=Frame(self.parent_frame,bg="cyan")
		self.top_frame.pack(side=TOP)		
		
		self.top_sub_frame1=Frame(self.top_frame,height=30,width=self.parent_frame["width"],bg="blue")
		self.top_sub_frame1.pack(fill= X,expand = YES,side=TOP)

		self.top_sub_frame2=Frame(self.top_frame,height=25,width=self.parent_frame["width"],bg="grey")
		self.top_sub_frame2.pack(fill= X,expand = YES,side=BOTTOM)
		
#-------------------------------------------------------------------------------------------------
		self.bottom_frame=Frame(self.parent_frame,bg="yellow")
		self.bottom_frame.pack(fill=BOTH,side=BOTTOM,expand=YES)
		
		self.bottom_sub_frame_parent=Frame(self.bottom_frame,bg="blue")
		self.bottom_sub_frame_parent.pack(side=TOP)
		
		self.bottom_sub_frame1=Frame(self.bottom_sub_frame_parent,bg="green",relief="sunken",height=self.parent_frame["height"]-70,width=self.parent_frame["width"]-16) 	#update in resize_handler() also if update in height here		
		self.bottom_sub_frame1.pack_propagate(False)    	# propagate stops from strecthing the frame
		self.bottom_sub_frame1.pack(side=LEFT)
		
		self.bottom_sub_frame2=Frame(self.bottom_sub_frame_parent)
		self.bottom_sub_frame2.pack(side=RIGHT,expand=True,fill=Y)
		
#-------------------------------------------------------------------------------------------------
		
#-----------------------top_sub_frame1 content-----------------------------------------------------

		self.server_options=('---select server---','MySQL','MongoDB','PostgreSQL')

		self.server_combo=ttk.Combobox(self.top_sub_frame1,width=20,justify="center")

		self.server_combo['values']=self.server_options
		self.server_combo.current(0)	

		self.server_combo.place(x=0,y=4)

		self.server_combo.bind("<<ComboboxSelected>>",self.server_selection)
		self.server_combo.unbind_class("TCombobox","<MouseWheel>")
		
		self.database_options=('---select database---',)	# Here at last , is given because tuple should have a comma if there is only one element
		
		self.database_combo=ttk.Combobox(self.top_sub_frame1,width=20,justify="center")

		self.database_combo['values']=self.database_options
		self.database_combo.current(0)

		self.database_combo.place(x=155,y=4)

		self.database_combo.bind("<<ComboboxSelected>>",self.select_database)
		self.database_combo.unbind_class("TCombobox","<MouseWheel>")
		self.database_combo.configure(state=DISABLED)
		
		self.table_options=('---select table---',)

		self.table_combo=ttk.Combobox(self.top_sub_frame1,width=20,justify="center")
		self.table_combo['values']=self.table_options
		self.table_combo.current(0)

		self.table_combo.place(x=305,y=4)

		self.table_combo.bind("<<ComboboxSelected>>",self.show_data_button_reset) #use << >> for events with ttk widgets
		self.table_combo.unbind_class("TCombobox","<MouseWheel>")
		self.table_combo.configure(state=DISABLED)

		self.show_data_button=Button(self.top_sub_frame1,text="Show Data",width=8,justify="center",state=DISABLED,command=self.show_data)
		self.show_data_button.place(x=460,y=2,height=25)

		self.display_clear_button=Button(self.top_sub_frame1,text="Clear",width=8,justify="center",state=DISABLED,command=self.clear_display)
		self.display_clear_button.place(x=540,y=2,height=25)

		self.log_out_button=Button(self.top_sub_frame1,text="Log out",justify="center", state=DISABLED,width=8,command=self.reset_all)
		self.log_out_button.place(x=self.top_sub_frame1["width"]-68,y=2,height=25)
		
#-------------------------------------------------------------------------------------------------------------------------------------------
		
		
#-----------------------top_sub_frame2 content---------------------------------------------------------------------------------------------
		
		self.table_search_var=StringVar()
		self.table_search_var.set("search table")

		self.table_search_text_box=Entry(self.top_sub_frame2,width=23,justify="center",textvariable=self.table_search_var)
		self.table_search_text_box.place(x=0,y=1)
		self.table_search_text_box.bind('<Button-1>',lambda e: self.table_search_var.set(""))

		self.table_search_button=Button(self.top_sub_frame2,text="search",width=8,justify="center")
		self.table_search_button.place(x=155,y=0,height=25)

#---------------------bottom_sub_frame contents ------------------------------------------------------------------------------
		
		self.xscrollbar=Scrollbar(self.bottom_frame,orient=HORIZONTAL,width=15)
		self.xscrollbar.pack(fill=X,expand=True,side=BOTTOM)		

		self.display_area=Text(self.bottom_sub_frame1,wrap=NONE,padx=0,pady=0,font=("Courier new",10))
		self.display_area.pack(fill= BOTH, expand=True)
		
		self.yscrollbar=Scrollbar(self.bottom_sub_frame2,orient=VERTICAL)
		self.yscrollbar.pack(fill=Y,expand=True)
		
		self.xscrollbar.config(command=self.display_area.xview)		
		self.yscrollbar.config(command=self.display_area.yview)

		self.display_area.config(xscrollcommand=self.xscrollbar.set,yscrollcommand=self.yscrollbar.set)
		
		self.server_combo.focus_set()
		
	def resize_handler(self,event):

		self.parent_frame.configure(width=event.width,height=event.height)
		self.top_sub_frame1.configure(height=30,width=self.parent_frame["width"])
		self.top_sub_frame2.configure(height=25,width=self.parent_frame["width"])

		self.log_out_button.configure(self.log_out_button.place(x=self.top_sub_frame1["width"]-68,y=2))
				
		self.bottom_sub_frame1.configure(height=self.parent_frame["height"]-70,width=self.parent_frame["width"]-16)
		

	def user_authentication(self):

		starting_x_pos=self.parent.winfo_rootx()
		starting_y_pos=self.parent.winfo_rooty()

		self.server_combo.configure(state=DISABLED)

		self.username_var=StringVar()
		self.username_var.set("")

		self.password_var=StringVar()						
		self.password_var.set("")

		self.auth_window=Toplevel()		

		self.auth_window.geometry("%dx%d+%d+%d"%( 250,140, (self.parent_frame["width"]-250)/2+starting_x_pos, (self.parent_frame["height"]-140)/2+starting_y_pos) )

		self.auth_window.wm_title("User Autentication")
		self.auth_window.protocol('WM_DELETE_WINDOW',self.cancel_authentication)

		self.login_label=Label(self.auth_window,text="Login")
		self.login_label.grid(columnspan=2,row=0,column=0)

		self.username_label=Label(self.auth_window,text="User Name")
		self.username_label.grid(row=1,column=0,padx=10,pady=12)

		self.username_entry=Entry(self.auth_window,width=25,textvariable=self.username_var)
		self.username_entry.grid(row=1,column=1)

		self.password_label=Label(self.auth_window,text="password")
		self.password_label.grid(row=2,column=0,padx=10)

		self.password_entry=Entry(self.auth_window,width=25,show="*",textvariable=self.password_var)
		self.password_entry.grid(row=2,column=1)
		self.password_entry.bind('<Return>',self.connection_process)

		self.ok_button=Button(self.auth_window,text="Ok",width=8,command=self.connection_process)
		self.ok_button.grid(row=3,column=1,sticky="W",pady=15)

		self.cancel_button=Button(self.auth_window,text="Cancel",width=8,command=self.cancel_authentication)
		self.cancel_button.grid(row=3,column=1,sticky="E",pady=15)	

		self.auth_window.focus_set()

		self.username_entry.focus_set()
		
	def server_selection(self,event):

		self.selected_server=None

		if self.server_combo.current()!=0:
			self.selected_server=self.server_options[self.server_combo.current()]
			self.user_authentication()

	def connection_process(self,*args):
		if self.make_connection():
			self.after_authentication()

	def after_authentication(self):
		self.auth_window.destroy()
		self.server_combo.configure(state=DISABLED)
		self.log_out_button.configure(state=NORMAL)
		self.database_combo.configure(state=NORMAL)
		self.update_database_combo()
		self.database_combo.focus_set()	

	def cancel_authentication(self):
		self.auth_window.destroy()
		self.reset_server_combo()
		self.server_combo.configure(state=NORMAL)	
		self.server_combo.focus_set()	


	def authentication_err_handler(self):

		if tkMessageBox.askretrycancel("Error","Something is wrong with your user name or password"):
			self.auth_window.focus_set()
			self.username_entry.focus_set()
		else:
			self.cancel_authentication()

	

	def make_connection(self):

		self.conn=None
		
		if self.selected_server=='MySQL':
			try:
				self.conn=mysql.connector.connect(host='localhost',user=self.username_var.get(),password=self.password_var.get())
				return True
			except:
				self.authentication_err_handler()
		elif self.selected_server=='MongoDB':
			self.conn_uri="mongodb://"+self.username_var.get().strip()+":"+self.password_var.get().strip()+"@localhost/admin?authMechanism=SCRAM-SHA-1"
			self.conn=pymongo.MongoClient(self.conn_uri)
			try:
				self.conn.database_names()
				return True
			except:
				self.authentication_err_handler()
		elif self.selected_server=='PostgreSQL':
			try:
				self.conn=psycopg2.connect(host='localhost',user=self.username_var.get(),password=self.password_var.get())				
			except:
				self.authentication_err_handler()

	def reset_server_combo(self):
		self.server_combo.current(0)


	def reset_database_combo(self):

		self.database_options=self.database_options[:1] # remove all previous values except on index 0.
		self.database_combo.configure(values=self.database_options)
		self.database_combo.current(0)

	def update_database_combo(self,*args):

		self.reset_database_combo()

		if self.selected_server=='MySQL':
			self.cursor=self.conn.cursor()
			self.cursor.execute("show databases")
			rows_of_databases=self.cursor.fetchall() 				# Here fetchall return a list of tuples of database names
			for r in rows_of_databases: 							# Here r contains a tuple having single element which is database name
				self.database_options=self.database_options+r 		# Here this loopsmakes a tuple of all database using concatenation +
		elif self.selected_server=='MongoDB':
			self.database_options=self.database_options+ tuple(self.conn.database_names()) # here tuple is used because temp_dbs is a list
		self.database_combo.configure(values=self.database_options)
		self.database_combo.current(0)

	def select_database(self,event):

		self.selected_database=None

		if self.database_combo.current()!=0:
			if self.selected_server=='MySQL':
				self.selected_database=self.database_options[self.database_combo.current()]				
			elif self.selected_server=='MongoDB':
				self.selected_database=self.conn[self.database_options[self.database_combo.current()]]

			self.table_combo.configure(state=NORMAL)
			self.update_table_combo()

	def reset_table_combo(self):

		if self.selected_server=='MySQL':
			self.table_options=('---select table---',)
		elif self.selected_server=='MongoDB':
			self.table_options=('---select collection---',)

		self.table_combo.configure(values=self.table_options)
		self.table_combo.current(0)

	def update_table_combo(self,*args):

		self.reset_table_combo()

		if self.selected_server=='MySQL':
			self.cursor.execute("use "+self.selected_database)
			self.cursor.execute("show tables")	
			rows=self.cursor.fetchall()
			for r in rows:
				self.table_options=self.table_options+r 	# Here + operator is used because self.table_options is a tuple and r is also a tuple
		elif self.selected_server=='MongoDB':
			self.table_options=self.table_options+tuple(self.selected_database.collection_names())

		self.table_combo.configure(values=self.table_options)
		self.table_combo.current(0)

	def show_data_button_reset(self,*args):
		self.show_data_button.configure(state=NORMAL)
		self.show_data_button.focus_set()

	def show_data(self,*args):

		if self.table_combo.current()!=0:
			if self.selected_server=='MySQL':
				table=self.table_options[self.table_combo.current()]
				query="desc "+table
				self.cursor.execute(query)
				raw_fields=self.cursor.fetchall() 	#returns the list of tuples of fields
				fields=[]

				for i in range(0,len(raw_fields)):
					fields.append(raw_fields[i][0])

				query="select * from "+table
				self.cursor.execute(query)
				rows=self.cursor.fetchall() # now rows contains the list of tuples of data

				#self.display_area.insert(END,self.selected_server+" "+self.selected_database+" "+table+"\n")				

				self.display_area.configure(state=NORMAL) 		# changing the state to normal because it is disabled for avoiding the user input

				for i in fields:
					self.display_area.insert(END,i+"\t\t")

				self.display_area.insert(END,"\n")
				
				for data_tuple in rows:
					for data in data_tuple:
						self.display_area.insert(END,str(data)+"\t\t")						
					self.display_area.insert(END,"\n")

				self.display_area.configure(state=DISABLED) 		# changing the state to disabled for avoiding the user input
				
			elif self.selected_server=='MongoDB':
				col=self.selected_database[self.table_options[self.table_combo.current()]]
				datas=col.find()
				
				self.display_area.configure(state=NORMAL) 		# changing the state to normal for programatic input because it is disabled for avoiding the user input

				self.display_area.insert(END,str(self.selected_server+"\n\n"))
				
				for data in datas:					
					columns=data.keys()
					for col in columns:
						self.display_area.insert(END,col+"\t"+str(data[col])+"\n")					
					self.display_area.insert(END,"\n")
					
			self.display_area.insert(END,"\n\n")

			self.display_area.configure(state=DISABLED) 		# changing the state to disabled for avoiding the user input

		self.display_clear_button.configure(state=NORMAL)

		self.display_area.focus_set()

	def clear_display(self,*args):
		self.display_area.configure(state=NORMAL) 		# changing the state to normal for programatic input because it is disabled for avoiding the user input
		self.display_area.delete(1.0,END)
		self.display_area.configure(state=DISABLED) 		# changing the state to disabled for avoiding the user input

		self.display_clear_button.configure(state=DISABLED)

	def reset_all(self):
		self.display_area.configure(state=NORMAL) 		# changing the state to normal for programatic input because it is disabled for avoiding the user input
		
		self.display_area.delete(1.0,END)

		self.display_area.configure(state=DISABLED) 		# changing the state to disabled for avoiding the user input

		self.reset_server_combo()
		self.reset_database_combo()
		self.reset_table_combo()

		self.database_combo.configure(state=DISABLED)
		self.table_combo.configure(state=DISABLED)
		self.log_out_button.configure(state=DISABLED)
		self.show_data_button.configure(state=DISABLED)

		self.server_combo.configure(state=NORMAL)
		


		self.server_combo.focus_set()		
		self.close_connections()

	def close_connections(self):
		self.conn.close()

	def __del__(self):
		print "sonu"
		self.close_connections()

	"""	if conn.ping():
						print "server is active"
					else:
						print "serevr is dead"
	"""
			
if __name__=='__main__':
	root=Tk()
	app=Application(root)
	root.mainloop()
