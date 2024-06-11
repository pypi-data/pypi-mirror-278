#publish
```
poetry self update && poetry self add keyrings.google-artifactregistry-auth
poetry config repositories.gcp https://europe-west1-python.pkg.dev/htz-data/haaretz-reasearc
poetry publish --build --repository gcp

```

#install with poetry
```
poetry source add --priority=explicit gcp https://europe-west1-python.pkg.dev/htz-data/haaretz-reasearch/simple
poetry add --source gcp pyhtz

```

# install with pip

```
pip install keyring && pip install keyrings.google-artifactregistry-auth
pip install pyhtz --index-url https://europe-west1-python.pkg.dev/htz-data/haaretz-reasearch/simple
```