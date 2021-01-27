#! /bin/bash

pip install pandas -q
pip install beautifulsoup4 -q
pip install requests -q

echo Hello, and welcome!
apt-get update --quiet
apt-get -y install postgresql --quiet

while [ 1 ]
do
#    python /opt/scr/scraper/news-scraper.py >> /opt/scr/news.log
    sleep 1

done