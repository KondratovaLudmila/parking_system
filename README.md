# README for Developers

This type of README focuses on how other developers can set up the project locally, contribute to the codebase, and understand the project's architecture.

## Parking System

This project is a Django-based web application designed to manage a parking system. The project utilizes Docker for containerization, PostgreSQL as the database, Nginx as a reverse proxy, and Let's Encrypt for SSL certificates.

## Features

- User Authentication
- Parking Space Management
- License Plate Recognition using EasyOCR and OpenCV
- Secure HTTPS connections with Let's Encrypt
- Deployment with Docker and Docker Compose

## Prerequisites

- Docker
- Docker Compose
- Python 3.9
- PostgreSQL 13

## Project Structure

```plaintext
.
parking_system/
├── certbot-env/
│ └── Dockerfile
├── numberplate_ukr/
│ ├── init.py
│ ├── main.py
│ └── model/
│ ├── init.py
│ └── model_files
├── parking/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── migrations/
│ │ └── init.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── parking_system/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── static/
├── templates/
├── users/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── migrations/
│ │ └── init.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── nginx.conf
└── requirements.txt
```

# Getting Started

## Clone the Repository

```sh
git clone https://github.com/KondratovaLudmila/parking_system.git
cd parking_system
```

## Set Up Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```env
POSTGRES_DB=parking_system
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db

DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,your_domain.com,your_ip_address

SECRET_KEY = 'your_key'
DEBUG = True

SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@example.com
SUPERUSER_PASSWORD=password
```

## Build and Run the Project

Build and run the Docker containers:

```sh
docker-compose up --build
```

## Apply Migrations

The migrations are applied automatically each time the containers are started. When the containers are launched using Docker Compose, the `web` service executes the necessary Django migrations to ensure the database schema is up to date. 

Here is how it works:

- When you run `docker-compose up --build`, the `web` service will execute the `python manage.py migrate` command automatically.
- This ensures that all database migrations are applied without manual intervention.

This setup helps streamline the deployment process and ensures the application is always running with the latest database schema.

## Access the Application

- The web application will be available at `http://localhost:80`
- The Django admin panel can be accessed at `http://localhost:80/admin`.

## Nginx Configuration

For the development version of the project, you should use the following `nginx.conf` file. Make sure to uncomment the provided configuration:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

___
___
___

# README for AWS Deployment

This README focuses on deploying the project on AWS, including setting up the server, environment, and necessary services.

# Parking System

This project is a Django-based web application designed to manage a parking system. The project utilizes Docker for containerization, PostgreSQL as the database, Nginx as a reverse proxy, and Let's Encrypt for SSL certificates.

## Features

- User Authentication
- Parking Space Management
- License Plate Recognition using EasyOCR and OpenCV
- Secure HTTPS connections with Let's Encrypt
- Deployment with Docker and Docker Compose

## Prerequisites

- AWS EC2 Instance
- Docker installed on the EC2 instance
- Docker Compose installed on the EC2 instance
- Domain name configured to point to the EC2 instance
- Postgres 13

# Deployment Steps

## Step 1: Connect to Your AWS EC2 Instance

Connect to your AWS EC2 instance via SSH:

```sh
ssh -i /path/to/your-key.pem ec2-user@your-ec2-public-dns
```

## Step 2: Install Docker and Docker Compose

Install Docker:

```sh
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
```

Install Docker Compose:

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify the installation:

```sh
docker --version
docker-compose --version
```

## Step 3: Clone Your Project

Clone your project from GitHub:

```sh
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

## Step 4: Run the Application

Build and run the Docker containers:

```sh
docker-compose up --build
```

## Apply Migrations

The migrations are applied automatically each time the containers are started. When the containers are launched using Docker Compose, the `web` service executes the necessary Django migrations to ensure the database schema is up to date. 

Here is how it works:

- When you run `docker-compose up --build`, the `web` service will execute the `python manage.py migrate` command automatically.
- This ensures that all database migrations are applied without manual intervention.

This setup helps streamline the deployment process and ensures the application is always running with the latest database schema.

## Renew SSL Certificates (optional)

To automatically renew the SSL certificates, run the Certbot container with the following configuration in your `docker-compose.yml`:

```yaml
certbot:
  image: certbot/certbot
  volumes:
    - certbot-etc:/etc/letsencrypt
    - certbot-var:/var/www/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
  networks:
    - mynetwork
```

## Set Up SSL Certificates with Let's Encrypt

First, run Nginx with the developer settings to ensure the server is running. Use the following configuration in `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Uncomment the above configuration and start Nginx. Then, run the following command to obtain and install the SSL certificates:

```sh
sudo certbot certonly --webroot -w /var/www/certbot --email your_email@example.com -d yourdomain.com -d www.yourdomain.com
```

After obtaining the certificates, update the Nginx configuration for AWS settings (look below `Nginx Configuration`) and restart the Docker containers:

```sh
docker-compose down
docker-compose up --build
```


## Nginx Configuration

For deploying the project on AWS, you should use the following `nginx.conf` file. Make sure to uncomment the provided configuration:

Update the `nginx.conf` file with your domain name and paths to SSL certificates.

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name your_domain.com www.your_domain.com;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name your_domain.com www.your_domain.com;

        ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## Access the Application

- The web application will be available at `https://yourdomain.com`.
- The Django admin panel can be accessed at `https://yourdomain.com/admin`.