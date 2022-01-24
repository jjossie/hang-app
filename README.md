# HangApp

## Overview

HangApp is a web application meant to help groups of people make decisions as a group. It allows users to pose a question meant for the group, such as:

* Where should we go eat?
* What movie should we watch?
* Where are we hanging out next?

One user will begin by creating a session, then entering a decision they want the group to help make. Users then begin suggesting options which the group votes on by selecting yes, no, or neutral for each option. The results are then tallied and the winning option is presented to the group in true utilitarian fashion.

[Software Demo Video](http://youtube.link.goes.here)

## Web Pages

1. *hangapp/start* This is where users first enter their name to identify themselves to the group.
2. *hangapp/join*  Here users can add decisions to be made as a group. After at least one decision has been added, an invite link is generated so multiple users can join the session.
3. *hangapp/suggest* Here users suggest options for a particular decision.
4. *hangapp/vote* After all suggestions are in, each user is presented with each option one at a time, where they will select whether they are in favor, against, or for that option.
5. *hangapp/results* This is where the final results of the decision are displayed.

## Development Environment

* Python 3.9.2 64-bit
* Django version 4.0.1
* VSCode version 1.63 with Django extension version 1.8.0
* Database: Django built-in model for SQLite3

## Useful Websites

* [Django Documentation](https://docs.djangoproject.com/en/4.0/intro)
* [Python Documentation](https://docs.python.org/)
* [W3Schools](https://www.w3schools.com/)
* [GeeksForGeeks](https://www.geeksforgeeks.org/)

## Future Work

### Short-term Improvements

* Improve handling of POST data and database interactions
* Revamp user interface, especially for mobile
* Utilize Django's session features
* Enable real-time updates of database between users

### Long-term Improvements

* Include default suggested decisions, such as the ones listed in the overview above
* Automatically generate options for certain decisions using Google Maps API
* Allow more rich data to be used with each option, such as pictures
* Host web app on IaaS or PaaS, such as GCP Cloud Run
