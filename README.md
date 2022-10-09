# QAEngine


## Main Idea
A Questions & Answers engine which will provide users the opportunity to
ask questions in any topic they desired.
These questions can be answered by other users which can provide their own opinion/answer to the question.

**Important!**  
The [documentation](https://github.com/edenavitan90/QAEngine/tree/main/documentation) folder contains relevant installation guides & demo videos for the project.  
As well, a PDF which contains information regarding to the MongoDB data distribution.

## Features
- Login system
- Create new account
- Search a query in our DB using TF-IDF algorithm
- Create new question & answer
- Answer existing questions
- Mark answer as helpful (by like/dislike mechanism)

Nice to have features:
- Create sections for different topics.
- Support file & image uploading.
- Support 2-Factor Authentication.


## Design
![UML Final final x3](https://user-images.githubusercontent.com/85113161/194756456-a6d8ee7d-10f0-4778-ab0c-14e8afacf8c6.png)


- **User** – A person who would like to use the system.
- **Frontend - UI** – The web app itself for the use of the user.
- **Backend - Server (Leader)** – Manage the flow of information. Divide the work across the workers.
- **Backend - Server (Worker)** – Will execute tasks received from main server and return to it responses.
- **DB**:  
  - **DB.Router** – Router processes and targets the operations to shards and then returns results to the clients.
  - **DB.Config-srv** – Store the metadata and configuration information for a sharded cluster.
  - **DB.Shards** – Shards instances which stores the data.


## Architecture & Technology
Web application which uses a Client-Server architecture (REST).
**Search Engine Workflow** -  
The Frontend server will send requests to the Backend server which will be run as following:      
- Ledear server will get the request (query to search) and will split the work between the workers.
- Each worker will search the query in its Shard in the DB and will implement the search using TF-IDF algorithm.
- Each worker will send back the result to the leader server which will then sort them in decreasing order.
- The leader server will send the response back to the client.

Note:  
We will use ZooKeeper in order to determine which server will function as leader across all of the other servers.  

- **Frontend-Server:** Flask & HTML/CSS
- **Backend-Server:** Flask
- **Database:** MongoDB
- **Configuration Manager:** ZooKeeper


## Installation Procedure
First, make sure to create & activated venv:  
Create:  
  python -m venv venv
Activate:  
  source venv/bin/activate

Then, install the requirements.txt:  
  pip install -r requirements.txt  

**There is an installation guide in the [documentation](https://github.com/edenavitan90/QAEngine/tree/main/documentation) folder.**  
Order Procedure:
1. QAEngine - DB Installation.mp4
    - Open the create_db.sh which located in 'db' folder and run each command in your terminal to create our db structure.  
    - Make sure to run each command seperate from each other (some of the commands are not bash commands). 
2. QAEngine - Servers Initialization.mp4
    - Run ./db/full_data.py to insert the dataset into the DB.
3. QAEngine - WebSite Demo.mp4
    - Quick overview of the application functionallty.
4. QAEngine - DB Presentation.pdf
    - Screenshots of the DB configurations.
