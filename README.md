4ChanCrawler
============

Crawls the front page of a 4Chan imageboard for a list of trigger-words, then grabs the image that the trigger post was replying to. 

For example, if someone replies to a thread with a picture of a BMW, which you want. You set the script to crawl for instances of the words "BMW", "Bavarian Motor Works" and "beamer". Someone replies to that picture, saying, "Nice beamer." The script flags that post, locates the original image and downloads it.

*Made for collecting original unlicensed photos for digitally-generated mosaics in Jython.*

To Do
---
*   Argument input rather than setting values in the file.
*   Case insensitivity
*   Replace index selection with attribute selection in XPATHs
*   Detect purged threads
*   Utilize MD5 for when threads are purged mid-crawl