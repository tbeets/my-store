# my-store

Store lookup service given consumer coordinate and a search radius (miles)

## Store Database

Bootstrap store data is in comma-delimited (CSV) format with some double-quoted strings that may contain commas.

| Column | Value |
| ------ | ----- |
| C1 | Store code |
| C2 | Store name |
| C3 | Street address 1 |
| C4 | Street address 2 |
| C5 | City |
| C6 | State / Province |
| C7 | Postal code |
| C8 | Country |
| C9 | Telephone |
| C10 | Store site URL |
| C11 | Marketing blurb |
| C12 | Payment types |
| C13 | Store type |
| C14 | Unknown |
| C15 | Marketing graphic |
| C16 | Latitude (degrees) |
| C17 | Longitude (degrees) |
| C18 | Sunday hours |
| C19 | Monday hours |
| C20 | Tuesday hours |
| C21 | Wednesday hours |
| C22 | Thursday hours |
| C23 | Friday hours |
| C24 | Saturday hours |

Note: On startup a file named `stores.csv` in the `data` sub-directory is loaded (one copy per Python process). 

# Standalone Service Execution

## Pre-requisite steps

    virtualenv --python=python2.7 venv
    source venv/bin/activate
    pip install -r ./requirements.txt

## Application execution

Using gunicorn:

    gunicorn --workers 2 --threads 2 --bind 0.0.0.0:5000 app.main:app

Using Flask built-in:

    python app/main.py
    
Note: Use gunicorn and `workers` and `threads` to scale concurrent requests on a single server. 

# Docker Service Execution

## Application execution

    docker run -i -t -p 5000:5000 tbeets/my-store

Note: Use `--env WEB_CONCURRENCY=x` to override default 2 gunicorn workers

# Service API

| Resource | Methods | Parameters | Description |
| -------- | ------- | ----------- | ---------- |
| /stores  | GET     | none | All stores |
| /store/:id | GET   | none | Single store of known ID |
| /stores/nearest | GET | q, r, max | Zero or more stores (sorted) within a search radius (miles) from customer location 

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| q | Yes | Coordinate in format loc:latitude+longitude where latitude and longitude are in degrees, e.g. q=loc:30.4+-113.2 |
| r | No, default 25 miles | Radius (in miles) from customer location defining store search area 
| max | No, default 10 stores | Maximum number of stores returned matching search radius |

# Client API Invocation

##  Sample /stores/nearest request


    http "localhost:5000/stores/nearest?q=loc%3A30.4%2B-113.2&r=500"

Note: See [HTTPie command line HTTP client](https://httpie.org/)

## Sample /stores/nearest response

    HTTP/1.0 200 OK
    Content-Length: 976
    Content-Type: application/json
    Date: Mon, 19 Sep 2016 04:10:24 GMT
    Server: Werkzeug/0.11.11 Python/2.7.11
    
    [
        {
            "C1": "TPR - 2058",
            "C10": "http://www.t-mobile.com/store/cell-phone-phoenix-az-98.html",
            "C11": "Visit T-Mobile Phoenix cell phone stores and discover T-Mobile's best smartphones, cell phones, tablets, and internet devices. View our low cost plans with no annual service contracts.",
            "C12": "MasterCard, Visa, American Express, Cash, Checks",
            "C13": "Cell Phone Store",
            "C14": "",
            "C15": "http://www.t-mobile.com/content/dam/tmo/store-locator-images/440_360_t-mobile-logo-default.jpg",
            "C16": "33.7143033",
            "C17": "-112.109448",
            "C18": "11:00AM-06:00PM",
            "C19": "10:00AM-08:00PM",
            "C2": "T-Mobile Phoenix",
            "C20": "10:00AM-08:00PM",
            "C21": "10:00AM-08:00PM",
            "C22": "10:00AM-08:00PM",
            "C23": "10:00AM-08:00PM",
            "C24": "10:00AM-07:00PM",
            "C3": "2330 W Happy Valley Rd",
            "C4": "",
            "C5": "Phoenix",
            "C6": "AZ",
            "C7": "85085-8505",
            "C8": "US",
            "C9": "(623) 889-0500",
            "dist": 237.72859697171697,
            "map_url": "http://maps.google.com/maps?z=12&t=m&q=loc:33.7143033+-112.109448"
        }
    ]

## Sample /store/:id request

    http "localhost:5000/store/1"
    
## Sample /store/:id response
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 952
    Content-Type: application/json
    Date: Mon, 19 Sep 2016 06:00:10 GMT
    Server: gunicorn/19.6.0
    
    {
        "C1": "MD20",
        "C10": "http://www.t-mobile.com/store/cell-phone-owings_mills-md-982.html",
        "C11": "Visit T-Mobile Owings Mills cell phone stores and discover T-Mobile's best smartphones, cell phones, tablets, and internet devices. View our low cost plans with no annual service contracts.",
        "C12": "MasterCard, Visa, American Express, Cash, Checks",
        "C13": "Cell Phone Store",
        "C14": "",
        "C15": "http://www.t-mobile.com/content/dam/tmo/store-locator-images/440_360_t-mobile-logo-default.jpg",
        "C16": "39.409891",
        "C17": "-76.7683938",
        "C18": "12:00PM-05:00PM",
        "C19": "10:00AM-08:00PM",
        "C2": "T-Mobile Owings Mills",
        "C20": "10:00AM-08:00PM",
        "C21": "10:00AM-08:00PM",
        "C22": "10:00AM-08:00PM",
        "C23": "10:00AM-08:00PM",
        "C24": "10:00AM-08:00PM",
        "C3": "9914 Reisterstown Rd",
        "C4": "",
        "C5": "Owings Mills",
        "C6": "MD",
        "C7": "21117",
        "C8": "US",
        "C9": "(410) 581-2300",
        "map_url": "http://maps.google.com/maps?z=12&t=m&q=loc:39.409891+-76.7683938"
    }

