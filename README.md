# TubeService
A RESTful web service for the status of Lisboa's subway lines.
Scrapes the public site of metro de Lisboa and publishes the status over a REST web service done with Flask

## Dependencies
* Python >= 3.3
* Flask
* BeautifulSoup4
* Requests

## Installation
TBD

## Usage

**Get all lines status**

    curl -X GET http://HOST/status
    
**Get single line status**

    curl -X GET http://HOST/status/<line>
    
line = [yellow | red | blue | green]
