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

4. Build and run the Docker containers:

```bash
docker-compose up -d --build
```

5. Access the Django application:

You can access the Django application running on `127.0.0.1:8000` in your web browser.
