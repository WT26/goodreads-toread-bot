import requests
import sys, os, base64, datetime, hashlib, hmac, time
import urllib
import urllib.parse
import collections
from xml.etree import ElementTree
from lxml import html

def getUsedSellerNames(ISBNs):

    dictator = {}
    URL = "http://webservices.amazon.com/onca/xml?"

    f = {
        'AWSAccessKeyId': 'ACCESS KEY',
        'AssociateTag': 'ASSOCIATE TAG',
        'IdType': 'ISBN',
        'ItemId': 'ITEMID',
        'Operation': 'ItemLookup',
        'SearchIndex': 'Books',
        'Service': 'AWSECommerceService'}
    f['ItemId'] = ISBNs
    f.update({'Timestamp' : datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')})
    od = collections.OrderedDict(sorted(f.items()))
    string = urllib.parse.urlencode(od)
    stringToSign = "GET\nwebservices.amazon.com\n/onca/xml\n" + string
    signature = base64.b64encode(hmac.new(b'UFwzDXMXCEPDd47hYrn6bCyq3GF3FEvHmt2TxGYV', msg=stringToSign.encode('utf-8'), digestmod=hashlib.sha256).digest())
    signature = urllib.parse.quote_plus(signature)

    URL = URL + string + "&Signature=" + signature
    r = requests.get(URL)
    print(r)
    tree = ElementTree.fromstring(r.content)

    for elem in tree:
        if elem.tag == "{http://webservices.amazon.com/AWSECommerceService/2011-08-01}OperationRequest":
            tree = elem
            for elem in tree:
                if elem.tag == "{http://webservices.amazon.com/AWSECommerceService/2011-08-01}Arguments":
                    tree = elem
                    break
            break

    itemid = 0
    for elem in tree:
        if elem.attrib["Name"] == "ItemId":
            itemid = elem.attrib["Value"]

    page = requests.get('https://www.amazon.com/gp/offer-listing/' + itemid + '/ref=dp_olp_used?ie=UTF8&condition=used.html')
    print('https://www.amazon.com/gp/offer-listing/' + itemid + '/ref=dp_olp_used?ie=UTF8&condition=used.html')
    tree = html.fromstring(page.content)

    #This will create a list of buyers:
    buyers = tree.xpath('//*[@id="olpOfferList"]/div/div/div/div[4]/h3/span/a/text()')
    #This will create a list of prices
    prices = tree.xpath('//*[@id="olpOfferList"]/div/div/div/div[1]/span/text()')
    newprices = parsePrice(prices[1:])

    shipping = tree.xpath('//*[@id="olpOfferList"]/div/div/div/div[1]/p/span/span[1]/text()')
    newshipping = parsePrice(shipping)

    #print(buyers)
    #print(newprices)
    #print(newshipping)


    i = 0
    while i < len(buyers):
        dictator[buyers[i]] = newprices[i]
        i += 1
    return dictator

def parsePrice(prices):
    oneprice = ""
    newprices = []
    for item in prices:
        for letter in item:
            if letter == " " or letter == "$":
                pass
            else:
                oneprice += letter
        try:
            newprices.append(float(oneprice))
        except ValueError:
            newprices.append(1)
        oneprice = ""
    return newprices

