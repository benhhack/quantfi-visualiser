# Quant Fi Visuliser - Read me to be updated
The purpose of this app is to create a visualiser for some quant fi concepts coded in Python. The template repository can be found at 
https://github.com/yaojiach/docker-dash. 


The original README is below with the run instructions. This README will be updated when the project has some more legs.



# Docker Dash (Plotly)

Dockerize a Python Dash app for quick prototyping.

## Build and run

`prod` version is served by `gunicorn` instead of the `flask` dev server.

```sh
# dev
docker build -f Dockerfile.dev -t docker-dash-example-dev .
docker run -p 8050:8050 -v "$(pwd)"/app:/app --rm docker-dash-example-dev

# prod
docker build -f Dockerfile -t docker-dash-example-prod .
docker run -p 8050:8050 -v "$(pwd)"/app:/app --rm docker-dash-example-prod
```

## Access the page

Go to `http://localhost:8050` in browser.

## Switch debug mode in Dockerfile

```dockerfile
ENV DASH_DEBUG_MODE True # False
```

## Development

Install the app requirements for development to get better editor support.

```sh
poetry install
```

Optional: clean initialization of `poetry`:

```sh
poetry init
cat app/requirements.txt | xargs poetry add
```
