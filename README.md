# TREND
### ECE Senior Design

Authors:
- Gavin Hendrix
- Rohan Rajesh
- Zack Kouba

## Project Overview
### What does TREND do?
TREND is an application that helps users make everyday decisions with a focus on restraunt suggestions, movie suggestions, and activity suggestions. Users create an account and fill out interests surveys for each of the three categories(movies, activities, and dining). Once user profile is complete users submit a query for movies we submit a query to TMDB API with their user information as parameters to recieve back a movie recommendation we can provide to the user. For dining and activity recommendations the user must allow navigator geolocation to use their location. If location use is allowed, when the user clicks for a dining or activity recommendation we use their location, preferences, and recommendation type as parameters for a Google Places API call to gather local options for the user. From here these results are sent into a OpenAI API call along with some user information to return us the best option for the user. This best option is then displayed for the user along with it's location on the map through a Google Maps API call. 

### Motivation for TREND
This project is designed to help eliminate the prevalent and rising problem of indecision, while also providing the user with unbiased and personalized options. 

## Getting Started with TREND
### Project File Structure
```
TREND
├── README.md 
├── USER_MANUAL.md 
├── app 
│   ├── __init__.py 
│   ├── src 
│   │   ├── api 
│   │   │   └── __init__.py 
│   │   └── auth 
│   │       └── __init__.py 
│   ├── static 
│   │   ├── css 
│   │   │   └── styles.css 
│   │   ├── js 
│   │   │   └── app.js 
│   │   └── media 
│   └── templates 
│       ├── auth 
│       │   └── login.html 
│       └── base.html 
├── config.py 
├── requirements.txt 
├── run.py 
├── tests
├── Dockerfile
├── run.py
├── version.txt
└── Makefile
```
Above is an overall file structure of the TREND project. For running on local host, the commands "make", followed by "make run" will allow the project to run on wsl, unix, or linux system. 
## TREND Contributers
TREND is currently maintained and updated frequently by the TREND team, Zach, Rohan, and Gavin. Trend will be hosted on a website in the near future.