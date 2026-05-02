<h1>Car Database (Standalone)</h1>

<h2>What is this project?</h2>

This repo contains a database system that holds a large set of car information. Through running the system, the user can filter search cars, add cars, and search a car by its ID. It is the standalone version of my [Original Car Database](https://github.com/JacobCampau/CarDatabase.git) project. This version was made so I could learn SQLite in python and learn how to make a web GUI using Flask. The combination of these two goals resulted in a final project that works better than the original project.

<h2>How to Run</h2>

There are two ways to access the 'Car Filter Database'

1) Through the following link: https://carinformationdatabase.onrender.com

This is a read only website for the database. All added information will not be saved after you leave the website.

2) Through the bat file provided in the repository

Upon the download of all files in this repository, running the bat file will run the database through your local host instead of through render.com

<h2>Components of The System</h2>
<h3>(1) Filter Option</h3>
The filter option will allow the user to sort through the cars by their components (ie make, color, price, etc.). The user can use any number of filters based on their inputs. The system will the print our the car id, make, model, and year of the car. 

<h3>(2) Add Car Option</h3>
The add car option will allow the user to add a car of their choosing. By default the values of the car are set to either 0 or NA. The user can choose to fill these values with new ones, but does not need to. The user only needs to specift a make, model, and year for the car.

<h3>(3) Search by ID Option</h3>
The search by ID option will allow the user to search for the car's full specs and information by its database id. This id can be found in the database filter search.

<h3>(4) Extra Details</h3>
The user will interact with the system as instructed using numbers to choose menu or filter choices and pressing enter when at the end of a temporary display.
