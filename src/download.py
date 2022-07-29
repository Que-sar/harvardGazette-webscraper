import requests
from re import findall
from bs4 import BeautifulSoup
from main import args
import threading
import queue
from pymongo import MongoClient

regs = requests.Session() # For faster requests
    #Ethics and link stored
headers = {"User-Agent": "This is my web scraping script for a University multithreading project, deadline is 17th of May, almost finished, I hope there is no inconvenience; You can contact me at kroka171@gmail.com."}
urlToUse = "https://news.harvard.edu/gazette/story/"

#Queues used, also providing thread safe lookups, as they are inherently wrapped in locks by design
allYears = queue.Queue()
allPages = queue.Queue()
allLinks = queue.Queue()

#Lock and Semaphores
fileWriteLock = threading.Lock() # To lock dictionary that is shared and constantly changed for upload.
finderSema = threading.Semaphore(0) # Semaphore that synchonise () between year and page numbers to start while crawling is still underway
uploaderSema = threading.Semaphore(0) # Semaphore that synchronise () between crawling and uploading data online, while still crawling

# Gets all years in just 1 request, meaning peak performance with only 1 thread.
def getAllYears(link):

    contents = BeautifulSoup(regs.get(link, headers=headers).content, "html.parser")
    years = [int(i) for i in findall(">(\d{4})<\/a>", str(contents.find_all("li")))]
    # results in like: [2003, 2004, 2005, 1996] etc...
    for i in years:
        allYears.put(i)

# Gets all possible page numbers on all possible years, 26 years in 2022, peak performance is 26 threads concurrently requesting
def getPossiblePages():

    while not allYears.empty(): #While there is remaining data, no need for synchronisation, because only 1 thread executed before
        year = allYears.get()
        link = urlToUse + str(year)
        contents = BeautifulSoup(regs.get(link, headers=headers).content, "html.parser")
        pages = str(contents.find("h3", attrs={"class":"archive-paging__page-text"}))
        res = [int(findall("([\d]+)<\/h3>", pages)[0]), year] 
        # regex through bs4 and request html body, results in eg: [13, 2022] meaning 13 pages in 2022

        allPages.put(res)
        #print(allPages.get())
        #print(allPages.queue) # helper to see what it displays
        finderSema.release() # Increases Semaphore to make sure other listening consumer threads are executing the now available data



# Gets all possible news links from the current page through a helper function, this only starts everything and manages
def gigaMegaFeeder():

    finderSema.acquire() # Decreases and Locks with Semaphore to make sure other listening consumer threads are executing the now available data
    #print(str(year) + " here")


    internalThreads = []
    while not allPages.empty(): # This way, semaphore does not let through threads that are not required. While thread does not get reasigned
        aller = allPages.get()  # overhead costs therefore are saved and no new threads created.
        year = aller[1]
        pages = aller[0]
        #print(year)
        #print(pages)
        for page in range(1, pages+1):
            if args.optimal == "y": # Optimal type, gets as many threads as needed. WARNING, A LOT OF THREADS WILL EXECUTE + SYNCHRONISED THREADS STILL RUN
                t = threading.Thread(target=getPageLinks, args=(urlToUse + str(year) + "/page/" + str(page), ))
                internalThreads.append(t)
                t.start()
            else:
                getPageLinks(urlToUse + str(year) + "/page/" + str(page)) # Usual execution
            print(urlToUse + str(year) + "/page/" + str(page))

        for thread in internalThreads:
            thread.join()

# Helper function on gigaMegaFeeder function, this only fetches the links and puts them in queue as list
def getPageLinks(link):
    
    contents = BeautifulSoup(regs.get(link, headers=headers).content, "html.parser")
    articleLinks = contents.find_all('h2', attrs={"class":"tz-article-image__title"})
    links = [i.find("a", href=True)["href"] for i in articleLinks]

    allLinks.put(links)
    uploaderSema.release() # Semaphore to signal to uploader listening consumer threads, that uploading now is possible
    #print("Putting links")
    # with open("tosee.txt", "a") as f:
    #     with fileWriteLock:
    #         f.write(str(allLinks.get()))
    #         f.write("\n")

# Shared variable dictionary, O(1) lookup time    
sharedDict = {"_id": 1,
                 "yearDate": "Someyear",
                 "pageNumber": "Somepage",
                 "everyLinks": "SomeLinks"}
#Unique index for all JSON like mongoDB "document" content, this evades E11000 mongoDB Error if previously freed
uniqueIndex = 1

if int(args.uploadThreads) > 0: # No small connection overhead cost if no upload was needed
    client = MongoClient("mongodb+srv://CMP205:CMP205@cluster0.obaei.mongodb.net/?retryWrites=true&w=majority") # Not actual login creds(fake)
    db = client.get_database("sites")
    records = db.websites
    records.delete_many({}) # Deletes, to avoid E11000 error when running it again
# records.create_index({ "currentIndex": 1 })

#Function that uploads links
def uploadLinks():
    global uniqueIndex # Makes variable modifiable later on in small scope too
    patternToUse = "\/story\/(\d{4})\/(\d{2})"
    uploaderSema.acquire() # Semaphore signalling new upload required
    while not allLinks.empty(): # Thread to work without losing overhead reassigning cost
        tempStoreUse = allLinks.get()
        specifics = findall(patternToUse, tempStoreUse[0])
        if not specifics: #Sometimes the first link does not contain year and page number, index 0 was used to stop unnecessary regex matches
            specifics = [["Year Not Found", "Page Number Not Found"]]
        
        with fileWriteLock: # Locks shared resource to avoid duplicates in a safe way
            print("Inserting")
            sharedDict["_id"] = uniqueIndex
            sharedDict["yearDate"] = specifics[0][0]
            sharedDict["pageNumber"] = specifics[0][1]
            sharedDict["everyLinks"] = list(tempStoreUse)
            #print(sharedDict)
            records.insert_one(sharedDict)
            uniqueIndex += 1
            print(uniqueIndex)



