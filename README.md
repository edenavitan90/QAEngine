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
![image](https://user-images.githubusercontent.com/85113161/188500779-71cf247c-1720-4a76-9eca-1e73fc2fa2e2.png)

- **User** – A person who would like to use the system.
- **UI** – The web app itself for the use of the user.
- **Load Balancer** – Manage the flow of information between the server and an endpoint device.
- **Server (worker)** – Will execute tasks received from load balancer and return to it responses.
- **DB** – The database which stores the data.


## Architecture & Technology
Web application which uses a Client-Server architecture (REST).
The load balancer decides which servers can handle the traffic from the end users.
It will distribute the work to the servers (workers) & eventually, will return a response back to the client.

**Client-Server:** Flask & HTML/CSS
**Database:** MongoDB
**Load Balancer:** HAProxyund


## Installation Requirements
This is meant to be a Web-Application.
Therefore, there is no need in any installation procedures.
As for production, this application will have its URL address and can be access via the network.


