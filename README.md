# QAEngine


## Main Idea
A Questions & Answers engine which will provide users the opportunity to
ask questions in any topic they desired.
These questions can be answered by other users which can provide their own opinion/answer to the question.


## Features
- Login system
- Create new account
- Issue new question
- Answer existing questions
- Mark answer as helpful (by the owner of the question)

Nice to have features:
- Create sections for different topics.
- Support file & image uploading.
- Support 2-Factor Authentication.


## Design
![UML Final final x3](https://user-images.githubusercontent.com/85113161/194756456-a6d8ee7d-10f0-4778-ab0c-14e8afacf8c6.png)


- **User** – A person who would like to use the system.
- **UI** – The web app itself for the use of the user.
- **Server (Main)** – Manage the flow of information. Divide the work across the workers.
- **Server (Worker)** – Will execute tasks received from main server and return to it responses.
- **DB** – The database which stores the data.


## Architecture & Technology
Web application which uses a Client-Server architecture (REST).
The client will send requests to the server which will be ran as following:  
- Main server will get the request (query to search) and will split the work between the other workers.
- Each worker will search the query in the DB and will implement the search using TF-IDF algorithm.
- Each worker will send back the result to the main server which will then sort them in decreasing order.
- The main server will send the response back to the client.

Note:  
We will use ZooKeeper in order to determine on the main server across all of the other servers that will be used.  
Sharding will be used with MongoDB and each worker will run the TF-IDF algorithm on different shard.

- **Client-Server:** Flask & HTML/CSS
- **Database:** MongoDB
- **Configuration Manager:** Zoo Keeper


## Installation Requirements
This is meant to be a Web-Application.
Therefore, there is no need in any installation procedures.
As for production, this application will have its URL address and can be access via the network.
