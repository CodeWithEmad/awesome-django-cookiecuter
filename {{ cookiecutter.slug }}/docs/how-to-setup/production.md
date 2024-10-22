# Production Deployment Guide

This guide will walk you through setting up the project for production deployment.

## Prerequisites

- A server with Docker and Docker Compose installed
- Domain name pointing to your server's IP address
- SSL certificate for your domain (Let's Encrypt recommended)

## Steps

1. Clone the repository on your production server:

   ```bash
   git clone {{ cookiecutter.repository }}
   cd {{ cookiecutter.slug }}
   ```

2. Create a `.env` file in the `backend` directory with production settings:

   ```bash
   DEBUG=False
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=postgres://user:password@db:5432/dbname
   REDIS_URL=redis://redis:6379/0   ```

3. Build and start the Docker containers:

   ```bash
   docker-compose up -d --build
   ```

4. Create a superuser for the Django admin:

   ```bash
   docker-compose exec api python manage.py createsuperuser
   ```

5. Collect static files:

   ```bash
   docker-compose exec api python manage.py collectstatic --no-input
   ```

## Installing and Configuring Nginx

1. Install Nginx on your server:

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. Create a new Nginx configuration file:

   ```bash
   sudo nano /etc/nginx/sites-available/{{ cookiecutter.slug }}
   ```

3. Add the following configuration, replacing `your-domain.com` with your actual domain:

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /path/to/your/fullchain.pem;
       ssl_certificate_key /path/to/your/privkey.pem;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static/ {
           alias /path/to/your/static/files/;
       }

       location /media/ {
           alias /path/to/your/media/files/;
       }

       location /flower/ {
           proxy_pass http://127.0.0.1:5555;
           proxy_set_header Host $host;
           proxy_redirect off;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

4. Create a symbolic link to enable the site:

   ```bash
   sudo ln -s /etc/nginx/sites-available/{{ cookiecutter.slug }} /etc/nginx/sites-enabled/
   ```

5. Test the bashNginx configuration:

   ```bash
   sudo nginx -t   ```

6. If the test is successful, restart Nginx:

   ```bash
   sudo systemctl restart nginx
   ```

7. Set up SSL with Let's Encrypt:

   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Final Steps

1. Update your firewall to allow traffic on ports 80 and 443:

   ```bash
   sudo ufw allow 'Nginx Full'
   ```

2. Ensure all services are running:

   ```bash
   docker-compose ps
   ```

3. Monitor the logs for any issues:

   ```bash
   docker-compose logs -f
   ```

## Sentry Integration for Error Tracking

This project uses Sentry to collect errors and monitor application performance.
Follow these steps to set up Sentry:

1. Sign up for a Sentry account at [sentry.io](https://sentry.io/){:target="_blank"}
if you haven't already.

2. Create a new project in Sentry for your application. Choose "Django" as the platform
and select the appropriate options for your project.

3. Once the project is created, you'll be provided with a DSN (Data Source Name).
Add this to your `.env` file:

   ```bash
   SENTRY_DSN=https://your-sentry-dsn@sentry.io/your-project-id
   ```

4. Restart your Docker containers to apply the changes:

   ```bash
   docker-compose down
   docker-compose up -d
   ```

With Sentry configured, you'll now receive error reports and performance data in your Sentry dashboard.

Your production environment should now be set up and running securely with Nginx as a reverse proxy and Sentry for error tracking.
