# ISPTwitterAnalyzer

## instructions

If you have access to root, then install the required libraries by running...
```console
> sudo pip install -r requirements.txt
```
If you do not have access to root, then install the required libraries by running...
```console
> pip install --user -r requirements.txt
```
Finally, to run the program once the libraries above are there are a variety of commands.

To re-gather the dataset collection, run ```console > python GatherTweets.py ```.
To re-gather the dataset collection for response time, run ```console > python getDataResponseTime.py ```.

*Warning:* This command will take over an hour to run. 
This is only necessary if you wish to change the date range of our current collection.

To run sentiment analysis, ```console > python SentimentAnalysis.py ```.

To run outage analysis, ```console > python ShawOutages.py ```.

To run word usage analysis, ```console > python WordFrequency.py ```.

To get the average response time, ```console > python AtShawAnalysis.py ```.
