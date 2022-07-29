# <h1>harvardGazette-webscraper</h1>
</h3>University website scraper parallel programming project that gets all news links from harvard Gazette news site synchronised, in a threadsafe manner.

Presentation can be found in the repository.(5 mins read)

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

