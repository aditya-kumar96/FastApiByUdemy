### Todo App 
This branch is dedicated to the first Todo App in which we are connect with the database and then using our API's we perform action on UI side

 - Create database file to create connection for the db
 - Create Model.py which allow us to tell what kind of tables we are creating using sqlalchemy and integrate with our db , this will be the actual result which will be available in the database table
 - create main.py and integrate the Base and models and create a todos db 


## Task Done

 - create database using sqlalchemy
 - get connection with the db
 - create api to get all data
 - create api to get todo by id
 - create api to create todo
 - create api to update the todo
 - create api to delete the todo
 - update the code
 - setup the project structure 
 - add validation folder 
  - create routers using APIRouter
 - create auth file for user 
 - create class to validate user
 - update the db name
 - created hashed password
 - create api to get all user
 - create api to authenticate the login user
 - create functions to validate the jwt token shared by client 
 - create function to check the details shared in token is valid or not so allow to login into db
 - create api to read all todo by admin
 - create new user with role admin
 - delete todo by admin
 - delete user by admin




 ### Create User
  - create api to get current logged in user
  - create api to change password


### DBMS
- we are integrating PostgreSQL in the app
- having problem in connecting with database , so figuring out the root cause
- connected with database and use alembic to add new field in the table 


### Unit Testing and Integration Testing with Pytest 
 - we are integrating the pytest for unit testing and integration testing