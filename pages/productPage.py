import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import sqlite3

class productPage(tk.Frame):
	def __init__(self, master, app, productID):
		super().__init__(master)
		self.app = app
		self.content = ttk.Frame(self)
		self.content.grid(row=0, column=0, sticky=tk.NSEW)

		# Get the product
		self.product = self.getProduct(productID)[0]
		self.description = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

		self.createImageFrame()
		self.createProductFrame()

	# Creates fame for the product
	def createProductFrame(self):
		self.productDetails = ttk.Frame(self.content, width=50)
		self.productName = ttk.Label(self.productDetails, text=self.product[1], font=('Helvetica', 12, 'bold'), anchor="w")
		self.productName.grid(row=0, column=0, columnspan=2, pady=20, sticky="w")

		self.productPrice = ttk.Label(self.productDetails, text=("$" + str(self.product[2])), font=('Helvetica', 14))
		self.productPrice.grid(row=1, column=0, pady=20, sticky="w")

		self.description = ttk.Label(self.productDetails, font=('Helvetica', 14, 'italic'), text=str(self.description),width=80, wraplength=700, justify='left')
		self.description.grid(row=2, column=0, pady=10, sticky="w")

		# If the user isn't logged in, then the product page's add button should just take them to the login page
		if self.master.loggedinUser == None:
			self.addButton = ttk.Button(self.productDetails, text="Add to cart", command= lambda: self.master.openPage("userLogin"))
		else:
			self.addButton = ttk.Button(self.productDetails, text="Add to cart", command= lambda: self.master.CartClass.updateCartItem(self.product, 1))
			
		self.addButton.grid(row=3, column=0, sticky=tk.W)
		self.productDetails.grid(row=1, column=1, sticky=tk.N)

	def createImageFrame(self):
		self.imageFrame = ttk.Frame(self.content, relief="solid")
		image = Image.open(self.product[4])
		image = image.resize((350, 350))
		image = ImageTk.PhotoImage(image=image)
		image_label = ttk.Label(self.imageFrame, image=image)
		image_label.image = image
		image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
		self.imageFrame.grid(row=1, column=0, padx=40)


	## get product
	def getProduct(self, id):
		self.master.cursor.execute(f"SELECT * FROM items WHERE id={id}")
		product = self.master.cursor.fetchall()
		return product