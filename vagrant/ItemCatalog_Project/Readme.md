#Course Catalog Project
#### Author: Md Kamrul Hasan Pulok
#### This project is developed as a part of Udacity Full Stack Web Developer Nanodegree Project-5

##Instructions to run the Project:
* Need to have vagrant and virtual box installed
* clone this project in the local machine
* run the vagrant in the cmd terminal inside vagrant folder using : "vagrant up"
* Then login to vagrant machine using : "vagrant ssh"
* Then go into the Tournament folder using: "cd /vagrant/ItemCatalog_Project"
* Then run the local server using : "python server.py"
* The site can be viewed in this link "http://localhost:5000/"

##Tools used in this Project:
* python
* Flask
* sqlAlchemy
* SQL DB
* JSON API
* GOOGLE Login API
* Facebook Login API

## Feature Checklist complying Project Rubric:
* API Endpoints:
    * Does the project implement a JSON endpoint with all required content?
        * The project implements a JSON endpoint that serves the same information as displayed in the HTML endpoints for an arbitrary item in the catalog : __done__

* CRUD: Read:
    * Does the website read category and item information from a database?
        * Website reads category and item information from a database : __done__

* CRUD: Create:
    * Does the website include a form allowing users to add new items and correctly processes these forms?
        * Website includes a form allowing users to add new items and correctly processes submitted forms : __done__

* CRUD: Update:
    * Does the website include a form to update a record in the database and correctly processes this form?
        * Website does include a form to edit/update a current record in the database table and correctly processes submitted forms : __done__

* CRUD: Delete:
    * Does the website include a way to delete an item from the catalog?
        * Website does include a function to delete a current record. : __done__

* Authentication & Authorization:
    * Do create, delete, and update operations consider authorization status prior to execution?
        * Create, delete and update operations do consider authorization status prior to execution. : __done__
    * Does the website implement a third party authentication and authorization service?
        * Page implements a third-party authentication & authorization service (like Google Accounts or Mozilla Persona) instead of implementing its own, insecure authentication & authorization spec. : __done__
    * Is there a “login” and “logout” button/link in the website?
        * Make sure there is a 'Login' and 'Logout' button/link in the project. The aesthetics of this button/link is up to the discretion of the student. : __done__








====================================
# Tournament Results Project
#### Author: Md Kamrul Hasan Pulok
#### This project is developed as a part of Udacity Full Stack Web Developer Nanodegree Project-4

##Instructions to run the Project:
* Need to have vagrant and virtual box installed
* clone this project in the local machine
* run the vagrant in the cmd terminal inside vagrant folder using : "vagrant up"
* Then login to vagrant machine using : "vagrant ssh"
* Then go into the Tournament folder using: "cd /vagrant/tournament"
* Then to create tournament database schema turn on psql cmd using: "psql"
* Then create tournament database schema using: "\i tournament.sql"
* Then exit psql cmd using : "\q"
* Then run the "tournament_test.py" script using : "python tournament_test.py"
* It should test all the functions and say "Success!  All tests pass!"

##Tools used in this Project:
* python
* postgreSQL

====================================
## Feature Checklist complying Project Rubric:
* Functionality:
    * Does the module pass the included unit tests? : The module passes the included unit tests. : __done__

* Table Design:
    * Do the tables have meaningful names? : __done__
    * Are the tables normalized? : __done__

* Column Design:
    * Are the columns defined with proper data types? : __done__
    * Do the columns have meaningful names? : __done__
    * Are primary and secondary keys properly defined? : __done__

* Code Quality:
    * Does the code make use of query parameters to protect against SQL injection? : __done__
    * Is the code ready for personal review and is neatly formatted? : __done__

* Comments:
    * Are comments present and effectively explain longer code procedures? : __done__

* Documentation:
    * Is a README file included, detailing all steps required to successfully run the application? : __done__