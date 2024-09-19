ARG IMAGE=ghcr.io/nationalarchives/tna-python
ARG IMAGE_TAG=latest

FROM "$IMAGE":"$IMAGE_TAG"

ENV NPM_BUILD_COMMAND=compile
ARG BUILD_VERSION
ENV BUILD_VERSION="$BUILD_VERSION"

# Copy in the application code
COPY --chown=app . .

# Install dependencies
RUN tna-build

# Copy in the static assets
RUN mkdir /app/app/static/assets; \
    cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets/* /app/app/static/assets; \
    cp -r /app/node_modules/plyr/dist/plyr.svg /app/app/static/assets/images

# Delete source files, tests and docs
RUN rm -fR /app/src /app/test /app/docs

# Run the application
CMD ["tna-run", "ds_frontend:app"]
