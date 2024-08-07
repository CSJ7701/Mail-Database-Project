
# Mail Database Project
This project is an exploration of Python, Tkinter, and SQL databases. 
Created as an assignment for a 2024 Software Engineering Class, this project aims to improve the interface for the United States Coast Guard Academy Mailroom, allowing staff to more efficiently manage packages and automatically email recipients when they have a package.

# Installation
## Prerequisites
Install [Python](https://wiki.python.org/moin/BeginnersGuide/Download) 

Install [Pip](https://pip.pypa.io/en/stable/installation/)

## Cloning the project

Open the directory you want to place this repo into.

Run ```git clone https://github.com/CSJ7701/Mail-Database-Project.git```

Open the folder that it created

run `pip install requirements.txt`

run `python main.py`

A window should appear


# Using

When the app first opens from the login screen, you will arrive at the dashboard.

![Homepage](https://github.com/CSJ7701/Mail-Database-Project/assets/113106427/768e09f9-e575-435a-9d74-36d4a5e80e24)

Navigate using the buttons on the left, which will bring you to different sections within the application.

## Home
The home screen is intended as a landing page, from which the user can get an overview of the packages which have been picked up that day, and a list of all unretrieved packages.

## Data
The data screen provides the core functionality of the application, allowing the user to search for a package based on the recipient's name, box number, or the box's tracking number. The user can also add new packages with the packages tracking number and the box number to which it is addressed.

## Manage DB
This screen is provided as an administrator functionality, and will require elevated priviledges within the app to use. 
It allows the user to directly edit information within the database, searching for entries and either deleting or modifying them.
This tab is not fully functional yet. Currently, users can search, select, and delete entries, but cannot edit them.
In the future, the system should also allow users to edit cadet data, but this feature has not been implemented yet.

## Reports
This screen allows the user to generate graphical reports in order to visualize the data outlined by the system.

## Settings
This screen allows the user to alter various visual and functional settings within the application.
Certain settings are restricted to user with administrative priviledges, such as exporting or uploading database files, or adding new users.

## Logout
This button will return the current user to the login screen

## Login Screen
Allows users to log in. 
User must first be created before they can log in.
