# HiveBox
Using Ubuntu as Os 
----------------------------------------
Phase 1

   Install Docker 

     sudo apt update

     Sudo apt install docker.io

  Check docker version

     docker --version

 Inside the system go to the folder which contain the app file name (hivebox-phase1.py) and the docker file name (phase1.Dockerfile)

    cd Hivebox

 Run the docker now to up the app 

    docker build -t hivebox .

    docker run -p 5000:5000 hivebox
   
The result now should out like this (The Current Version Of The App Is: V0.0.1)

------------------------------------------------------------------------
# Phase 2

All files using inside hivebox/phase2

tools using:

VS code 

Pylint 

Pylint for python code ckeck

Hadolint for Docker check

Hadolint 

------------------------------------------------
# Work steps:

## Development:

 1- create an app with 2 function 

   first one to retrive the app version 

   second one to get the average Temperature data from (openSenseMap API).

 2- Create a unit test for both functions.

 3- Create a docker file and requirements file.

## Test

1- On VS code terminal run :

      pylint hivebox_v2.py  # to check quality of the python app

      python hivebox_v2.py  # to run the app locally

U can check the ruslt of the app 

      http://127.0.0.1:5000/version # will return the app version
   
      http://127.0.0.1:5000/temperature  # will return the average temperature 

2- Now to check Docker file stracture qulity run:

     hadolint dockerfile

3- Now you can run the app into Docker container:

     docker build -t hivebox .

     docker run -d -p 5000:5000 --name hivebox hivebox

4- Now we can test same like  step 2 


## Github work

1- Upload your work to Github repo for the project.

2-  To create a workflow action for the work go to:

   Actions -----> New workflow -----> Setup you work flow.

3- Inside the work flow (python_ci.yml) will create these steps:

  1- checkout repo files.

  2- checkout python.

  3- Install Python dependencies (flask, requests, python-dateutil, pylint, unittest-xml-reporting).

  4- pylint check.

  5- install hadolint (as a lint for docker).

  6- build docker and run docker. 

  7- Test /version endpoint.

  8- Publish Test Report.

4- now go to workflow actions and see the build report and Junit test report.
 


   





  



  
