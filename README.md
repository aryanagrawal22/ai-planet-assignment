# AI-Planet-Assignment

## Contents
- [Problem Statement](#problem-statement)
- [Steps to run](#steps-to-run)
- [API endpoints](#api-endpoints)

## Problem Statement
Create a submissions app where one can submit their hackathon submissions & see the list. 

This is a internship task for a Backend Developer Internship where the task given is to create a simple Hackathon hosting application.

## Steps to run

### Requirements
python, pip, bash
#### NOTE: Make sure to setup the `.env` files from the given link below.
LINK: https://easyupload.io/rymzac

Follow these commands to setup the project.
1) Create a virtual env. ``python3 -m venv venv``
2) Activate the environment. ``source venv/bin/activate``
3) Install the requirements. ``pip3 install -r requirements.txt``
4) Make migrations. ``python3 manage.py makemigrations``
5) Apply migrations. ``python3 manage.py migrate``
6) Run server. ``python3 manage.py runserver``

## API endpoints

#### 1. `Running Server Check`
```
URL: /
Request type: GET
Authorization: False

Response:
"Welcome to AI-Planet-Assignment"
```

#### 2. `User`

- #### 2.1. `Register`
    ```
    Task: Register Users to the application.
    URL: /users/register
    Request type: POST
    Authorization: False
    
    Sample Request Data:
    {
      "name":"Mohan",
      "email":"mohan@gmail.com",
      "password":"abcd"
    }
    
    Response:
    {
      "message": "USER_REGISTER"
    }
    ```


- #### 2.2. `Login`
    ```
    Task: Login the user to get token
    URL: /users/login
    Request type: POST
    Authorization: False
    
    Sample Request Data:
    {
      "email":"mohan@gmail.com",
      "password":"abcd"
    }
    
    Response:
    {
      "user_id": "ec3c816a-17f3-46d9-aab5-637e440e0217",
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZWMzYzgxNmExN2YzNDZkOWFhYjU2MzdlNDQwZTAyMTciLCJleHAiOjE2ODQ4MzQzNzF9.JhUUGX_4z2CaOIeWHM9fp_0PRRnA9xGhmS4yi24kbTk"
    }
    ```
    Save this ``access_token``, and use it in headers having value of key ``Authorization`` to be logged in as a secure user

- #### 2.3. `Current user profile check`
    ```
    Task: Check currently logged in user profile
    URL: /users/check_profile
    Request type: GET
    Authorization: True
    Response:
    
    "aryan@gmail.com - Aryan - (7a9d5052-ffc0-46a7-b6d3-9ec50426d32f)"
    ```

#### 3. `Hackathon`

- #### 3.1. `Create Hackathon`
    ```
    Task: Staff members only can create hackathon.
    URL: /hackathons/create
    Request type: POST
    Authorization: True
    
    Sample Request Data:
    {
      "title":"Trial5",
      "start_time":"23-04-28 09:00:00",
      "end_time":"23-04-29 09:00:00",
      "description":"Trial Hackathon",
      "reward_prize":"10000 Rupees"
    }
    
    Response:
    {
      "message": "HACKATHON_CREATED"
    }
    ```
    
 - #### 3.2. `Get All Hackathon`
    ```
    Task: Get all hackathons with filters **ALL (Default), FINISHED, ONGOING, INCOMING**
    URL: /hackathons/get_hackathons
    Query Parameter: filter= [ALL, FINISHED, ONGOING, INCOMING]
    Request type: GET
    Authorization: True
    
    Response:
    [
      {
        "id": "81a1d103-1fa9-498f-9d6b-4036e12723b3",
        "title": "Trial3",
        "description": "Trial Hackathon",
        "background_image": null,
        "hackathon_image": null,
        "start_time": "2023-04-20T09:00:00Z",
        "end_time": "2023-04-27T09:00:00Z",
        "reward_prize": "10000 Rupees"
      }
    ]
    ```
    
- #### 3.3. `Register in Hackathon`
    ```
    Task: Users can enroll in hackathons
    URL: /hackathons/hackathon_register
    Request type: POST
    Authorization: True
    
    Sample Request Data:
    {
      "hackathon_id":"6c3e7ba2-63ff-40ca-bec9-d9a5ae99e494"
    }
    
    Response:
    {
      "message": "USER REGISTERED FOR HACKATHON"
    }
    ```

- #### 3.4. `Get User Enrolled Hackathons`
    ```
    Task: Get hackathons list where user is enrolled
    URL: /hackathons/get_registered_hackathons
    Request type: GET
    Authorization: True
    
    Response:
    [
      {
        "id": "81a1d103-1fa9-498f-9d6b-4036e12723b3",
        "title": "Trial3",
        "description": "Trial Hackathon",
        "background_image": null,
        "hackathon_image": null,
        "start_time": "2023-04-20T09:00:00Z",
        "end_time": "2023-04-27T09:00:00Z",
        "reward_prize": "10000 Rupees"
      }
    ]
    ```
    
#### 4. `Submissions`

- #### 4.1. `Create Submission`
    ```
    Task: User can submit for enrolled hackathon.
    URL: /submissions/create_submission
    Request type: POST
    Authorization: True
    
    Sample Request Data:
    {
      "title":"submission1",
      "summary":"test",
      "hackathon_id":"81a1d103-1fa9-498f-9d6b-4036e12723b3",
      "submission_link":"www.google.com"
    }
    
    Response:
    {
      "message": "Submission Created"
    }
    ```
    
- #### 4.2. `Get user submissions`
    ```
    Task: User can get their submissions
    URL: /submissions/get_submissions
    Request type: GET 
    Authorization: True
    
    Response:
    [
      {
        "id": "f48d0c51-2a49-4464-95a3-4a9740feeaa2",
        "title": "submission1",
        "summary": "test",
        "created_at": "2023-04-23T08:52:20.522498Z",
        "user": {
            "user_id": "7a9d5052-ffc0-46a7-b6d3-9ec50426d32f",
            "name": "Aryan",
            "email": "aryan@gmail.com"
        },
        "hackathon": {
            "id": "81a1d103-1fa9-498f-9d6b-4036e12723b3",
            "title": "Trial3",
            "description": "Trial Hackathon",
            "background_image": null,
            "hackathon_image": null,
            "start_time": "2023-04-20T09:00:00Z",
            "end_time": "2023-04-27T09:00:00Z",
            "reward_prize": "10000 Rupees"
        },
        "details": {
            "submission_link": "www.google.com",
            "submission_type": "LINK"
        }
      }
    ]
    ```
