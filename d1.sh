#!/bin/bash
while true
do
a=`stat -c %s /home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w1.txt`
if (($a != 0))
then
for line1 in `cat /home/zijianan/fb_processing/Ultimate-Facebook-Scraper/w1.txt`
do 
	python /home/zijianan/fb_processing/Ultimate-Facebook-Scraper/scraper/scraper.py -dbco $line1
done
fi
sleep 1
done
