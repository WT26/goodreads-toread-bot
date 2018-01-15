import requests
from xml.etree import ElementTree

def getToreadIsbnList(key, user_id):


    key = key
    user_id = user_id


    review_list_URL = "https://www.goodreads.com/review/list/"
    r = requests.get(review_list_URL + user_id + ".xml?key="+ key + "&shelf=to-read&per_page=200&page=1")
    tree = ElementTree.fromstring(r.content)

    all_books = tree.find("books").findall("book")

    ISBN_list = []
    ISBN13_list = []
    title_list = []

    index = 0
    for book in all_books:
        ISBN_list.append(book.find("isbn").text)
        ISBN13_list.append(book.find("isbn13").text)
        title_list.append(book.find("title").text)
        print("Title: " + str(title_list[index])
              + "     ISBN: " + str(ISBN_list[index])
              + "    ISBN13: " + str(ISBN13_list[index]))
        index += 1
    return (title_list, ISBN_list, ISBN13_list)

