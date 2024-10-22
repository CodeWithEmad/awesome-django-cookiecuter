# Development Setup

This guide will help you set up the development environment.

## Prerequisites

- Docker
- Docker Compose
- Python 3.x
- virtualenv

## Setup Steps

1. Clone the repository:

   ```bash
   git clone [repository_url]
   cd {{ cookiecutter.slug }}
   ```

2. Create and activate a virtual environment:

   ```bash
   virtualenv -p python3 .venv
   source .venv/bin/activate
   ```

3. Install development requirements. This will help you with the local development:

   ```bash
   make requirements.dev
   ```

4. Set up environment variables:

   ```bash
   cp backend/.env.sample backend/.env
   ```

   Edit the `.env` file with your specific configuration.

5. Build the image and start the development environment:

   ```bash
   make build.dev
   make up.dev
   ```

   This command will start all necessary services (API, database, Redis, etc.) using Docker Compose.

6. Create a superuser for the Django admin:

   ```bash
   make superuser.dev
   ```

7. Access the development services:
   - API Documentation: [http://localhost:8000](http://localhost:8000){:target="_blank"}
   - MailHog (email testing): [http://localhost:8025](http://localhost:8025){:target="_blank"}
   - Flower (celery monitoring): [http://localhost:5555](http://localhost:5555){:target="_blank"}
   - pgAdmin (database management): [http://localhost:5050](http://localhost:5050){:target="_blank"}

## Useful Commands

- Start the development environment: `make up.dev`
- Stop the development environment: `make down.dev`
- Rebuild Docker images: `make build.dev`
- Run tests: `make test`
- Format code: `make format`
- Start documentation server: `make doc`
- Execute a command in a running container: `make exec.dev <service_name> <command>`
- View logs for a specific service: `make logs.dev <service_name>`

## Debugging

The development setup includes remote debugging capabilities:

- Django API: Use port 5678 for remote debugging
- Celery Worker: Use port 6789 for remote debugging

Configure your IDE to connect to these ports for step-through debugging.

## Documentation

To work on the project documentation:

1. Start the documentation server:

   ```bash
   make doc
   ```

2. Access the documentation at [http://localhost:8010](http://localhost:8010){:target="_blank"}

3. Make changes to the Markdown files in the `docs/` directory. The server will automatically reload with your changes.

## Additional Notes

- The `Makefile` contains many useful commands for development. Run `make help` to see all available commands.
- Always run `make test` before submitting a pull request to ensure your changes pass all tests and meet the code style requirements.
