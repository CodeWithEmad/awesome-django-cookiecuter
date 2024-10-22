# {{ cookiecutter.name }}

{{ cookiecutter.description }}

## Development

Install development requirements

```bash
make requirements.dev
```

Create .env file from sample and set your own variables

```bash
mv .env.sample .env
```

Run docker compose

```bash
make dev.up
```

For more data, checkout docs in [localhost:8010](http://localhost:8010)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
