```
poetry self update && poetry self add keyrings.google-artifactregistry-auth
poetry config repositories.gcp https://europe-west1-python.pkg.dev/htz-data/haaretz-reasearch

poetry publish --build --repository gcp

```