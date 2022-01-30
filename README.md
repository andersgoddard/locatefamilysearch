The LocateFamily website is one where a person can search their surname and try to find the phone numbers of family members
It is essentially a telephone directory but it is not possible to search by address, hence this little project

I approached this with a completely test-driven mindset, with only a basic high-level idea of what I wanted as an end result 
The test suite and code has been refactored to make for easier reading but, in effect, the steps to final solution were:

1. Navigate the pages for a particular postcode and return the correct number of pages with results (this originally used a method that kept a count but I refactored it)
2. Scrape a page of the locatefamily website into a Pandas DataFrame and confirm that each column is pulled in correctly
3. I decided once I was scraping multiple pages that I would store a local cache of one DataFrame for a particular postcode to speed up the tests - at the time of this writing, I haven't stored a cache of the earlier single-page searches
4. Once I have a search term and a dataframe of all addresses, I apply a similarity score to each address. I have used Ratcliff/Obershelp Pattern Recognition but it will be easy to change to something else
5. With the dataframe reordered by the highest similarities, I then return either all results where the similarity is 100% or up to 10 results where the similarity is over 85%

The final element is to have a web page that serves up a form and displays the results. I'm going to do this using Flask and Google App Engine.

Lastly, the web app will scrape the locatefamily website in real-time, which means it will take a while to return results. 
This would be easy to rectify by scraping the whole website once and storing a dataframe locally. The dataframe variable in get_results() could use pd.read_csv().