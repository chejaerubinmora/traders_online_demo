## Prerequisites

Before using this template, ensure that you have the following dependencies installed on your system:

- Docker: [Install Docker](https://www.docker.com/get-started)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

To start a new project using this template, follow these steps:

1. Clone this repository to your local machine:

```bash
git clone https://github.com/chejaerubinmora/traders_online_demo.git
```

2. Navigate into the `traders_online_demo` directory:
   
```bash
cd traders_online_demo
```

3. Set environment variables:

```bash
cp .env.example .env
```
Open the `.env` file and set the value of all environment variables.

- Note: the POSTGRES_HOST in the .env should use the docker container service name e.g in the docker-compose.yml service name is db, then my POSTGRES_HOST=db, this will allow you to connect to the docker container db

4. Build and run the Docker containers:

```bash
docker-compose up -d --build
```

5. Access the Django application:

You can access the Django application running on `127.0.0.1:8000` in your web browser.

6. Endpoints

- Register
  ```
  endpoint: /api/traders/users/
  method: post
  payload: {
    "first_name": "",
    "last_name": "",
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testuser123",
    "confirm_password": "testuser123"
   }
  ```
- Login
  ```
  endpoint: /api/token/login
  payload: {"username": "testuser", "password": "testuser123"}
  method: post
  response: {
    "refresh": "eyJhbGciOiJIU...",
    "access": "eyJhbGciOiJIUzI1NiIsI..."
   }
  ```
- Create product
  ```
  endpoint: /api/traders/products/
  method: post
  header: Authorization: Bearer <login access token>
  payload: {
    "quantity": 10,
    "name": "Papaya Soap",
    "currency": "$",
    "price": 5
  }
  response: {
    "id": 14,
    "quantity": 10,
    "name": "Papaya Soap",
    "currency": "$",
    "price": 5
  }
  ```
- Order
  ```
  endpoint: /api/traders/products/order/
  method: post
  header: Authorization: Bearer <login access token>
  payload: {
    "product": 1,
    "quantity": 1
  }
  response: {
    "id": 8,
    "product": 1,
    "quantity": 2
  }
  ```
- Revenue per stock
  ```
  endpoint: /api/traders/products/<product id>/revenue/
  method: get
  header: Authorization: Bearer <login access token>
  response: {
    "id": 1,
    "name": "Papaya Soap",
    "price": "$5",
    "revenue": "$60"
  }
  ```
  
