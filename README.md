### find-keywords     
#### crawler will search given domain for web pages with certain keywords     
     
# setting new server for crawler     
sudo apt-get update     
sudo apt-get upgrade      
sudo apt-get install python python3 python-pip python3-pip python-setuptools python-dev libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev python-scrapy git      
     
pip install -r requirements.txt     
pip3 install -r requirements.txt     
     
# starting crawler     
#### step 1: crawler file for input domains      
rename output file from 2nd crawler in domains.csv       
I'm not sure what is changed here, is this input schools.txt still output from 2nd crawler?      
     
#### step 2: starting crawler      
to start the crawler step 1 should be made first, then you can run **python scrapy.py** or **python3 scrapy.py** script. Script scrapy.py can be located in first-crawler folder     
     
# crawler details    
    
#### crawler configurations   
#### coming soon    
#### results     
results_gre.csv    
     
#### log files    
     
there are three types of log files and can be found in **first-crawler/logs/**:      
**scrapy_log** records crawler status every minute for each crawler (pages crawled per minute, total pages crawled,items scraped per minute, total items scraped)     
     
**time_log** records crawler start and finish time for each domain which was crawled     
     
**error_log** records error from crawing (wrong input domains, non-existent domains...)     
     
### all past log files will be deleted every time when you start ./scrapy.py     
     
## Tips & Tricks
When crawler is running If you see that it is on the same domain for a long time, you can stop crawling that domain and start on next by pressing one time ctrl+c. Crawler will stop crawling that domain but it will start again on next one.      
      
##JSON keywords     
This means:      
      
"keywords": [       
                If crawler found any of "gre" or "gmat" keywords minimum 2 times      
        {      
            "words": ["gre", "gmat" ],      
            "min": 2      
        },      
                it will check if any of them has additional score keywords if not, page won't be picked up      
        {     
            "words": ["gre score", "gmat score"],      
            "min": 0      
        }      
        "hyperlink_check" : true,      
        "hyperlink_words": ["gre", "gmat"]      
     
**NEW** now we have hyperlink_words and hyperlink_check... Check currently mean nothing and hyperlink_words are keywords what we will search for in hyperlinks     
      
That is more for statistic than it is needed. Only is important that code need to satisfy first condition to search for second. That mean if it doesn't find min 2 "gre" of "gmat" it will stop search for keywords with score. But If you want to search only for "gre score" or "gmat score" you can add min: 0 under "gre" and "gmat".
Reason cos we do that is cos some pages has a lot of "gre" and "gmat" results but don't have "gre score" or "gmat score". How I remember, most pages which has "gre" and "gmat" keywords more than 5 has score too. If we search only for score keyword, we could pick up a lot of pages which don't have "gre" or "gmat" but has score.
