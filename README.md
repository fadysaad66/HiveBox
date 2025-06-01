# HiveBox
Using Ubuntu as Os 
----------------------------------------
Phase 1

   Install Docker 

     sudo apt update

     Sudo apt install docker.io

  Check docker version

     docker --version

 Inside the system go to the folder which contain the app and the docker file 

    cd Hivebox

 Run the docker now to up the app 

    docker build -t hivebox .

    docker run -p 5000:5000 hivebox
   
The result now should out like this (The Current Version Of The App Is: V0.0.1)



  
