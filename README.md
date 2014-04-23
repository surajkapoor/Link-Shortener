Link-Shortener
==============

A link shortener in Python, deployed on Heroku using a Postgres DB. Before execution, the link shortener will check if the entered URL is valid using the Requests library. Assuming so, it will generate a shortened link. 

There is also a basic load test function that tests to see how the app peforms under various loads.  

To run locally on Flask, use ```python url.py``` or ```foreman start``` 
