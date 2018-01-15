from tkinter import *
import json
import io
import requests

import grapi
import awsapi

import time

class MyFirstGUI:
    LABEL_TEXT = [
        "This is our first GUI!",
        "Actually, this is our second GUI.",
        "We made it more interesting...",
        "...by making this label interactive.",
        "Go on, click on it again.",
    ]
    def __init__(self, master):


        self.master = master
        master.title("A simple GUI")
        self.label_index = 0
        self.greet_button = Button(master, text="Generate Json File", command=self.load)
        self.greet_button.grid(row=1, column=3, columnspan=2, sticky=W+E+N+S)



        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.grid(row=2, column=3, columnspan=2, sticky=W+E+N+S)



        e1 = Entry(master)
        e2 = Entry(master)
        e1.insert(0, "account")

        e1.grid(row=1, column=2, columnspan=2, sticky=W+E+N+S)
        e2.grid(row=2, column=2, columnspan=2, sticky=W+E+N+S)


    def createJsonFile(self):
        key = "GOODREADS ACCESS KEY"
        user_id = "GOODREADS USER ID"

        title_list, isbn_list, isbn13_list = grapi.getToreadIsbnList(key, user_id)

        title_price_dict = {}
        sellers = []
        i = 0
        total_count = len(isbn_list)
        for isbn in isbn_list:
            print(isbn)
            if isbn != None:
                title_price_dict[title_list[i]] = awsapi.getUsedSellerNames(isbn)
                for elemme in title_price_dict[title_list[i]]:
                    sellers.append(elemme)
            time.sleep(2)
            print(str(i) + "/" + str(total_count))
            i += 1

        sellerdict = {}
        for seller in sellers:
            if sellers.count(seller) > 1:
                sellerdict[seller] = sellers.count(seller)

        jsonDict = {}
        booksDict = {}

        i = 0
        while i < len(title_list):
            tempID = str(i + 1)
            newbookdict = {}
            newbookdict["Id"] = tempID
            newbookdict["ISBN"] = isbn_list[i]
            newbookdict["ISBN13"] = isbn13_list[i]

            tempdict = {}
            try:
                for elemme in title_price_dict[title_list[i]]:
                    print(elemme)
                    tempdict2 = {elemme : title_price_dict[title_list[i]][elemme]}
                    print(tempdict2)
                    tempdict.update(tempdict2)
            except KeyError or ValueError:
                pass

            newbookdict["Sellers"] = tempdict
            booksDict[title_list[i]] = newbookdict
            i += 1
        jsonDict["Books"] = booksDict
        jsonDict["Common Sellers"] = sellerdict

        with open('books.txt', 'w') as outfile:
            json.dump(jsonDict, outfile, sort_keys=True, indent=4)

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()