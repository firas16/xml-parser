# xml-parser

This project aims to ease the parsing of XML files.
It provides methods to extract managers and performances.
It also encapsultes the code into a google cloud function.

## Install

`git clone https://github.com/firas16/xml-parser.git`

`cd xml-parser`

Then, install requirements:

## Requirements
* python 3.6+
* matplotlib 3.3.4 => to plot performances
* pandas 1.1.5
* google-cloud-storage 1.38.0 => needed in,ocal only to detect errors
* pytest 6.2.4 => for unit tests


## Question 4

To handle a lot of files 350k files, I suggest two approaches:

### Cloud function

#### Advantages
using cloud function is suitable when you have real time contraints and when you recieve files individually which appears to be the case.

It also gives horizantal scalability. So you can scale up to millions of files in a matter of seconds.

It's also failure tolerant. When the parsing if one file fails, it doesn't affect parsing the others.

#### Cost
First two million instances are free each month.
Cost of computing:
* $0.000000231 for 100ms of computing with a machine(128Mb memory, 200MH CPU)
* compute Time for one XML file: ~5sec
 
 => $5.7 for 500.000 xml file per month
 
#### Monitoring and Alerting
For monitoring, we can use cloud logging to debug any errors and we can setup email notification when there is an error.

Cloud function presents a dashboard which recapitulates errors, response time and many other metrics.

### Apache Spark
The second option is to use Apache Spark.

This solution is suitable for batch processing. If we recieve all files from an ETL. 

If we have a lot more data (millions of XML), it can be more suitable since it's scalable horizontally. It's drawback compared to cloud function is when failure happen. If there is a problem with one XML, it will affect the computing of others.
We can overcome this by having a filtering stage in the beginning to screen out bad XMLs.

This solution can be more efficient when we have a lot of data and will be probably cheaper.

regarding bad XML, I suggest to add a validation step using DTD (Document type Definition). A possible library: https://lxml.de/ 
or catch exceptions in the code.

