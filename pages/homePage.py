from threading import Thread
import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3

class homePage(tk.Frame):
    def __init__(self, master, app, *args):
        super().__init__(master)
        self.master = master
        self.app = app#
        self.homePage = tkb.Text(self, bd = 10, wrap="char", borderwidth=1, highlightthickness=0,
                            state="disabled", spacing1 = 50, spacing2 = 20, insertofftime=0)
        self.homePage.pack(fill=BOTH, expand=True)

        self.products = []

        self.conn = sqlite3.connect('assets/PyProject.db')
        self.cursor = self.conn.cursor()

        if args:
            if args[0] is not None:
                self.searchProducts(args[0])
        else:
            self.getProducts()


    def createProductDisplay(self, product):
        product_card = tk.Frame(self.homePage, width=200, height=200,  highlightbackground="#eee", highlightthickness=1, padx=3, pady=2)
        imageFrame = tkb.Frame(product_card, height=120)

        response = urlopen(product[4])
        data = response.read()
        image = Image.open(io.BytesIO(data))
        image = image.resize((120, 120))
        image = ImageTk.PhotoImage(image=image)
        image_label = tkb.Label(imageFrame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
        imageFrame.pack(fill=X)

        detailFrame = tkb.Frame(product_card, height=80)

        price_label = tkb.Label(detailFrame, text=f"$ {product[2]}", font=("Helvetica", 10), width=40, anchor="w")
        price_label.grid(row=1, column=0, sticky=tk.NSEW)

        buyButton = tkb.Button(detailFrame, text="Add to cart")
        buyButton.grid(row=1, column=1, sticky=tk.NS)

        name_label = tkb.Label(detailFrame, text=product[1], font=("Helvetica", 10, 'bold'), width=40, anchor="w")
        name_label.grid(row=0, column=0, sticky=tk.NSEW)

        name_label.bind("<Button-1>", lambda e:self.master.openPage("productPage", product[0]))

        detailFrame.pack(fill=X, expand=True)
        

        self.homePage.configure(state="normal")
        self.homePage.window_create("end", window=product_card)
        
        self.homePage.configure(state="disabled")

    def thread(self, row):
            t1=Thread(target=self.createProductDisplay(row))
            t1.start()

    def searchProducts(self, searchedProduct):
        self.cursor.execute("SELECT * FROM items WHERE name LIKE ? LIMIT 12", ('%' + searchedProduct + '%',))
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            for row in rows:
                self.thread(row)
        else:
            self.emptyLabel = tkb.Label(self.homePage, text="Nothing was found.")
            self.emptyLabel.pack()

    def getProducts(self):
       self.cursor.execute("SELECT * FROM items LIMIT 12")
       rows = self.cursor.fetchall()
       for row in rows:
            self.thread(row)
        