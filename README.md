# <h1>harvardGazette-webscraper</h1>
</h3>University website scraper parallel programming project that gets all news links from harvard Gazette news site synchronised, in a threadsafe manner.

### Presentation can be found in the repository.(5 mins read)

It uses BeautifulSoup4 and regex for gathering links, and MongoDB for uploading them to database, while taking commandline arguments with argparse.</h3>

<h4>1. Takes an endpoint, for eg.: "https://news.harvard.edu/gazette/story/2022/"</h4>
  - 1 thread only, as its only 1 request, meaning its the peak performance.<br>
  - Gathers the years of logged publishments.<br>

<h4>2. Starts specified Link-threads(default is the amount of years there are in publishment)</h4>
  - These links gather all number of pages that contain links of new articles.<br>
  - Semaphore synchronises the next thread to start with task #3.<br>

<h4>3. Starts link gathering threads.(default number of threads is the same as in task 2)</h4>
  - Semaphore signals to start.<br>
  - Iterates through pages and gathers links.<br>
  - When 1 page finished, signals with semaphores to start threads with #4.<br>
  - Optimised thread mode: starts threads for each page, minimising IO based task time.<br>

<h4>4. Starts link uploading thread to MongoDB server.</h4>
  - Waits for semaphore to start.<br>
  - Starts uploading.<br>
  - Locks shared variable to make it threadsafe.<br>

<h5>Time with optimised threading algorithms:</h5>
  Average: 87.47159079138382 seconds <br>
  Median: 87.05949537330392 seconds<br>
  
<h5>Time without multithreading:</h5>
  Average: 1448.121027455036 seconds <br>
  Median: 1449.7646775171445 seconds<br>
  
  ## Requirements
  
  The running of the program requires the:
- argparser module, pip3 install argparse # parsing command line arguments
- the pymongo module, pip3 install pymongo #connecting to database
- regular expressions,
- bs4(beautiful soup), pip3 install beautifulsoup4 #parsing HTML
- queue,
- requests,
- date,
- time,
- threading modules.

## Usage

with pyinstaller the main.py was made executable(main). This is located inside the main zip folder or the dist folder, tested and is working properly with the flags too.

example: ./main -y 1 -p 1 -u 1 
Using 1 thread for every function
More below:
        
if used with python, the main.py and download.py need to be in the same folder, or can be just copy pasted if needed.

example useage:
python3 main.py -y 10 -u 17 -p 23 -o y
-y flag for amount of yearThreads
-u for amount of uploadThreads
-p for amount of pageThreads
-o for optimised page scraping strategy(WARNING) this creates a lot of threads

with the help of the -h flag, this is all displayed


