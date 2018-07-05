from tkinter import *
from tkinter import ttk,messagebox
import sqlite3

conn = sqlite3.connect('CoffeeTreeview.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS productlist (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			producttype text,
			product text,
			price integer,
			quantity integer,
			total integer
			 )""")

def insertproduct(pdt,pd,pc,qt):
	with conn:
		c.execute("""INSERT INTO productlist VALUES (?,?,?,?,?,?)""",(None,pdt,pd,pc,qt,pc*qt))
		conn.commit()
		print('Data was Inserted')

def deleteproduct(name):
	with conn:
		c.execute("""DELETE FROM productlist WHERE product = ?""",([name]))
		conn.commit()
		print('Data was deleted')


def addproduct():

	pdt = producttype.get()
	pd = product.get()
	pc = int(price.get())
	qt = int(quantity.get())

	Tea = [pdt,pd,pc,qt,pc*qt]
	TVProductList.insert('','end',values=Tea)
	insertproduct(pdt,pd,pc,qt)

	if pdt == 'Hot Drink':
		TVProduct.insert('hot','end','',text=pd)
	elif pdt == 'Cool Drink':
		TVProduct.insert('cool','end','',text=pd)
	else:
		TVProduct.insert('cake','end','',text=pd)

GUI = Tk()
GUI.geometry('700x700')
GUI.state('zoomed')
GUI.title('Coffee Shop GUI by Uncle Engineer')
#-------------SET FONT for Treeview--------------
style = ttk.Style()
style.configure("Treeview.Headings",font=('Angsana New',20,'bold'))
style.configure("Treeview", font=('Angsana New',15))
#-------------SET FONT for Combobox
combofont=('Angsana New', '15')
GUI.option_add('*TCombobox*Listbox.font', combofont)

ProductType = ['Hot Drink','Cool Drink','Cake']

LF1 = LabelFrame(GUI, text='Product')
LF1.grid(row=0, column=0, padx=5, pady=5)

#--------------Product------------------
producttype = ttk.Combobox(LF1, values = ProductType,font=('Angsana New',15))
producttype.set('Hot Drink')
producttype.grid(row=0, column=0,padx=5,pady=5, sticky='w')


LProduct = ttk.Label(LF1, text='Product',font=('Angsana New',18))
LProduct.grid(row=0, column=1, padx=5, pady=5)

product = StringVar()

EProduct = ttk.Entry(LF1, textvariable=product,font=('Angsana New',18))
EProduct.grid(row=0, column=2, padx=5, pady=5)
#--------------Price------------------
LPrice = ttk.Label(LF1, text='Price',font=('Angsana New',18))
LPrice.grid(row=0, column=3, padx=5, pady=5)

price = StringVar()

EPrice = ttk.Entry(LF1, textvariable=price,font=('Angsana New',18),width=10)
EPrice.grid(row=0, column=4, padx=5, pady=5)
#--------------Quantity------------------
LQuantity = ttk.Label(LF1, text='Quantity',font=('Angsana New',18))
LQuantity.grid(row=0, column=5, padx=5, pady=5)

quantity = StringVar()

EQuantity = ttk.Entry(LF1, textvariable=quantity,font=('Angsana New',18),width=10)
EQuantity.grid(row=0, column=6, padx=5, pady=5)

Badd = ttk.Button(LF1, text='Add',command=addproduct)
Badd.grid(row=0, column=7, padx=5, pady=5,ipady=8,ipadx=10)

def updatedata():
	#first delete all data in list
	TVProductList.delete(*TVProductList.get_children())
	TVProduct.delete(*TVProduct.get_children())

	with conn:
		c.execute("SELECT * FROM productlist")
		allproduct = c.fetchall()
		print(allproduct)

	#Tea = [pd,pc,qt,pc*qt]
	#TVProductList.insert('','end',values=Tea)
	TVProduct.insert('','end','hot',text='Hot Drink')
	TVProduct.insert('','end','cool',text='Cool Drink')
	TVProduct.insert('','end','cake',text='Cake')
	for data in allproduct:
		#data = (5,'Hot Drink','กาแฟ', 50, 100, 5000)
		TVProductList.insert('','end',values=data[1:])
		if data[1] == 'Hot Drink':
			TVProduct.insert('hot','end','',text=data[2])
		elif data[1] == 'Cool Drink':
			TVProduct.insert('cool','end','',text=data[2])
		else:
			TVProduct.insert('cake','end','',text=data[2])


Bupdate = ttk.Button(LF1, text='Update Data',command=updatedata)
Bupdate.grid(row=0, column=8, padx=5, pady=5,ipady=8,ipadx=10)


#tree.delete(*tree.get_children())
#---------------------------------------

FTV1 = Frame(GUI)
FTV1.place(x=5,y=100)

TVProduct = ttk.Treeview(FTV1, height=25)
TVProduct.grid(row=1,column=0,sticky='w',padx=5, pady=5)


###### TREEVIEW LIST #######

FTV2 = Frame(GUI)
FTV2.place(x=250,y=100)

Header = ['Product Type','Product','Price','Quantity','Total']

TVProductList = ttk.Treeview(FTV2, height=25, columns=Header, show='headings')
TVProductList.grid(row=1,column=0,sticky='w',padx=5, pady=5)
#---------Add Header--------------
for col in Header:
	TVProductList.heading(col,text=col.title())

#---------ADD DATA to TVList----------
#Tea = ['Green Tea',20,100,2000]
#TVProductList.insert('','end',values=Tea)

def TVdelete(event=None):

	yesno = messagebox.askyesno('Are You Sure?','คุณต้องการลบข้อมูลใช่หรือไม่?')
	print(type(yesno))

	if yesno == True:

		# tvslect for delete data in treeview
		tvselect = TVProductList.selection()[0]
		# first item is 'I001'
		# why we input index 0 : ('I001',)

		# tvvalue for get values of data in current treeview
		tvvalue = TVProductList.item(TVProductList.selection(),'values')
		print("TV ID",tvselect)
		print(tvvalue)
		#TVProductList.delete('I001')
		TVProductList.delete(tvselect)
		deleteproduct(tvvalue[1])
		updatedata()
	else:
		pass

TVProductList.bind('<Double-1>',TVdelete)

updatedata()


GUI.mainloop()