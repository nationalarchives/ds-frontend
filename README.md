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

| Variable                | Purpose                                                       | Default |
| ----------------------- | ------------------------------------------------------------- | ------- |
| `DEBUG`                 | If true, allow debugging[^1]                                  | `False` |
| `WAGTAIL_API_URL`       | The base URL of the content API, including the `/api/v2` path | _none_  |
| `WAGTAIL_MEDIA_URL`     | The URL responsible for serving assets                        | _none_  |
| `CACHE_DEFAULT_TIMEOUT` | The number of seconds to cache pages for                      | `300`   |
| `CACHE_DIR`             | Directory for storing cached responses                        | `/tmp`  |

[^1] [Debugging in Flask](https://flask.palletsprojects.com/en/2.3.x/debugging/)
