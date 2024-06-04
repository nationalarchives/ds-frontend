# beta.nationalarchives.gov.uk frontend

## Quickstart

```sh
npm install
npm run build
mkdir app/static/assets
cp -r node_modules/@nationalarchives/frontend/nationalarchives/assets/* app/static/assets
docker-compose up -d
```

## Environment variables

In addition to the [base Docker image variables](https://github.com/nationalarchives/docker/blob/main/docker/tna-python/README.md#environment-variables), this application has support for:

| Variable                | Purpose                                                       | Default                                               |
| ----------------------- | ------------------------------------------------------------- | ----------------------------------------------------- |
| `CONFIG`                | The configuration to use                                      | `config.ProductionConfig`                             |
| `DEBUG`                 | If true, allow debugging[^1]                                  | `False`                                               |
| `WAGTAIL_API_URL`       | The base URL of the content API, including the `/api/v2` path | _none_                                                |
| `SEARCH_API_URL`        | The base URL of the search API                                | _none_                                                |
| `CACHE_DEFAULT_TIMEOUT` | The number of seconds to cache pages for                      | `300`                                                 |
| `CACHE_DIR`             | Directory for storing cached responses                        | `/tmp`                                                |
| `SEARCH_DISCOVERY_URL`  | The URL that accepts form posts to search discovery           | `https://discovery.nationalarchives.gov.uk/results/r` |
| `SEARCH_WEBSITE_URL`    | The URL that accepts form posts to search the website         | `https://www.nationalarchives.gov.uk/search/results`  |

[^1] [Debugging in Flask](https://flask.palletsprojects.com/en/2.3.x/debugging/)
