# PAD Laboratory Work nr 1.
## Checkpoint 1
Project name - Netflix Clone App
### 1. Why is necessary for the idea to build a distributed system?
    • Scalability – in case if we have large number of users or requests, a distributed system allows to scale different components independently.
    • Fault Tolerance – In distributive system, a failure will not affect the entire system.
    • Maintainability – we can maintain or update one microservice without impacting any other microservice.

A real world example is Netflix which is based on microservices.
***
### 2. Define service boundaries
![](Architecture_Diagram_PAD.png)

***
### 3. Technology stack:
For the Content Recommendation Service:
* Node.js (JavaScript):
  * Reasoning:
    *	Non-blocking, asynchronous I/O model for handling multiple concurrent requests, crucial for real-time content recommendation.
    *   Scalability with low memory usage, ideal for managing a large number of user requests.
    * Rich ecosystem of packages and libraries for content analysis, recommendation algorithms, and database management.
* Express.js (Node.js):
  * Reasoning:
    * Lightweight web application framework for building robust and scalable APIs for the Content Recommendation Service.
    * Allows for easy routing, middleware integration, and handling of HTTP requests.
* MongoDB (NoSQL):
  * Reasoning:
       * NoSQL database for flexibility in handling unstructured or semi-structured data, which aligns well with content recommendation systems.
       * Scalable, high-performance solution for managing large volumes of interaction data.
For the User Authentication Service:
* Flask (Python):
  * Reasoning:
      * Clear and concise microframework for building specialized services, making it an excellent choice for user authentication.
      * Provides essential features without the overhead of a full-featured framework, allowing for focused and efficient development.
* PostgreSQL (Relational):
    * Reasoning:
         * Reliable and robust relational database for structured user data management, including profiles, credentials, and authentication tokens.
***
### 4. Design Data Management:
TO BE MADE - Netflix business logic 

Data format that will be managed will be JSON format. User microservice will have the following endpoints:
* Register User \
Endpoint: 'POST/ api/users/register'\
Description: Register a User\
Request body:
```
{
  "email" : "ciuvak@gmail.com",
  "username": "example_user",
  "password": "secure_password"
}
```
Response body:
```
{
  "user_id": "123456789",
  "email": "ciuvak@gmail.com",
  "username": "example_user",
  "message": "User registered successfully."
}

```

* Login User\
Endpoint: 'POST/ api/users/login'\
Description: User Authentication\
Request body:
```agsl
{
  "username": "example_user",
  "password": "secure_password"
}
```
Response body:
```agsl
{
  "user_id": "123456789",
  "username": "example_user",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "message": "Login successful."
}

```
The Content Recommendation Service will have the following endpoints:
* Get recommendations\
Endpoint: 'GET api/recommendations'\
Description: Get a list of recommendations for the user\
Request body:
    * Authorization: Bearer <token> (for user authentication)

    Response body:\
Status 200 OK with a list of recommended content OR Status 401 Unauthorized if token is invalid

* Get content details
Endpoint: 'GET api/content/contentId'\
Description: Get details of a selected content\
Request body:
    * Parameters: content identifier

    Response body:\
  Status 200 OK with a list of recommended content OR Status 401 Unauthorized if token is invalid
  
* Like or Dislike Content
Endpoint: 'POST api/content/:contentId'/like\
Description: Allows a user to like or dislike a specific piece of content.\
Request body:
```
{
  "action": "like"  // or "dislike"
}
```
Response body:
    Status 200 OK if the action was successful OR
    Status 401 Unauthorized if token is invalid OR
    Status 404 Not Found if content with the specified ID does not exist


***
### 5. Deployment and Scaling:
To deploy my app I will use Docker.