# News Scraper

## A REST API to retrieve daily news headlines

This is a vanity project I have put together to demonstrate my skills and knowledge in the following areas.

* Django (Django REST Framework)
* Python programmng language
* Postgres Database
* Webscraping
* Webhosting (configuration and deployment, Nginx, Gunicorn, Linux, Cloud IaaS)
* JavaScript
* HTML
* CSS
* Graphic Design

The project demonstrates how I, as a full stack engineer can develop a front end website with a functional backend.

## How it works

**I have created a backend Django project which performs two functions.**

1. Scrapes News sites for the daily headlines.

I have created an admin program which will target different news sources and using "Beautiful Soup", extracts the latest headlines from their websites. This then transfers the source, headline text and  data to a database so it can be retrieved by the REST API endpoint which will retrieve up to 10 daily headlines from the database using a GET request.

2. Provides a REST API endpoint for retreiving the headlines.

I utilise the Django REST Framework to provide an endpoint which can be used to get the latest headlines and return up to 10 in JSON format.

**Frontend**

The frontend is a static web page which runs a JavaScript function to retrieve 10 headlines and display a random one on the page. When it finishes displaying one headline, it will display a new one, selected randomly.

I have stylised the page using CSS.

All of the graphics I have created myself using free software.

**Server Configuration**

I have deployed the project to my own cloud server running Linux. The server runs a daily cron job which alls the management interface to retreive the daily headlines and remove the existing ones so that the news headlines are continually refreshed.

The server serves the REST API.

**Licensing and use of code**

The content of this repository is fully public. Please feel free to copy any content, adapt it and use it how you wish.