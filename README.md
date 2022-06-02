# harvardGazette-webscraper
University website scraper parallel programming project that gets all news links from harvard Gazette news site synchronised, threadsafe.

It uses BeautifulSoup4 and regex for gathering links, and MongoDB for uploading them to database, while taking commandline arguments with argparse.

1. Takes an endpoint, for eg.: "https://news.harvard.edu/gazette/story/2022/"
  - 1 thread only, as its only 1 request, meaning its the peak performance.
  - Gathers the years of logged publishments.

2. Starts specified Link-threads(default is the amount of years there are in publishment)
  - These links gather all number of pages that contain links of new articles.
  - Semaphore synchronises the next thread to start with task #3.

3. Starts link gathering threads.(default number of threads is the same as in task 2)
  - Semaphore signals to start.
  - Iterates through pages and gathers links.
  - When 1 page finished, signals with semaphores to start threads with #4.
  - Optimised thread mode: starts threads for each page, minimising IO based task time.

4. Starts link uploading thread to MongoDB server.
  - Waits for semaphore to start.
  - Starts uploading.
  - Locks shared variable to make it threadsafe.

Time with optimised threading:
  Average: 87.47159079138382 seconds 
  Median: 87.05949537330392 seconds
  
Time without multithreading:
  Average: 1448.121027455036 seconds 
  Median: 1449.7646775171445 seconds

