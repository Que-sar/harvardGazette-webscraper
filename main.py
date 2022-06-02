from download import *
import time
from datetime import date
import threading
import argparse

# Parser for more functionality and to be able to vary the number of threads used.

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--yearThreads", help="[?] Amount of threads to use, to retrieve amount of pages in years.", default=date.today().year - 1996)
parser.add_argument("-p", "--pageThreads", help="[?] Amount of threads to use, to retrieve amount of links in pages.", default=date.today().year - 1996)
parser.add_argument("-u", "--uploadThreads", help="[?] Amount of threads to use, to upload links found.", default=date.today().year - 1996)
parser.add_argument("-o", "--optimal", help="[?] Amount of threads to use, to retrieve amount of links in pages, 'y' if yes, 'n' if no.", default="n")

args = parser.parse_args()

def main():

    # Arrays that store the used threads -> to easily join and use them as a group

    allYearThreads = []
    allPageThreads = []
    uploadThreads = []

    start = time.time()

    #1 call, to get all years, as this is one request, it can not be more efficient
    getAllYears(urlToUse + "1996")

    # print(list(allYears.queue)) # Left here, for easier code checking
    # allPages.put([13, 2022])
    # allPages.put([7, 2021])
    #allPages.put([1, 1996])

    # Starting threads that parse through the years, to get the pages
    for i in range(int(args.yearThreads)):
        t = threading.Thread(target=getPossiblePages, name = "thread{}".format(i))
        #print(t)
        allYearThreads.append(t)
        t.start()

    # Starting threads that parse through years acquired and get the amount of pages
    for i in range(int(args.pageThreads)):
        t = threading.Thread(target=gigaMegaFeeder, name = "thread{}".format(i))
        allPageThreads.append(t)
        t.start()
    

    # Starting threads that upload the parsed links from all the pages
    for i in range(int(args.uploadThreads)):
        t = threading.Thread(target=uploadLinks, name = "thread{}".format(i))
        t.daemon = True
        uploadThreads.append(t)
        t.start()

    # Joining all 3 threadgroups back to the main thread
    for i in allYearThreads:
        print(t)
        i.join()

    for i in allPageThreads:

         i.join()

    for i in uploadThreads:

        i.join()
        
    end = time.time()
    print(end-start)

    


if __name__ == "__main__":
    main()