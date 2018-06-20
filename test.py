import Pin
term_type_index={'1':'search'}
print("Enter Keyword :")
term = input()
print("Enter Search Type :"
      "1 for Search By Keyword")
term_type=term_type_index[input()]
#cerate object of Pin PinSearch class using PinSearch(term, term_type)
#use term_trype "search" if you are going to search term
helloPin = Pin.PinSearch(term, term_type)

#get object Of beautifulSoup object using getSoup(url)
soup=helloPin.getSoup(helloPin.url)

#get jsonData using getJSONData(soup)
jsonData=helloPin.getJSONData(soup)

#get array of links using fetchLinks(jsonData)
links=helloPin.fetchLinks(jsonData)

#add links to database using addToDb(links,helloPin.term)
helloPin.addToDb(links,helloPin.term)

print("")
