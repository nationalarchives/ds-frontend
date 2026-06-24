ARG IMAGE=ghcr.io/nationalarchives/tna-python
ARG IMAGE_TAG=1.16@sha256:80e944d81ef2dad20c0ff803a1513f2434fca8a9a59d841fcbc0fbf1a5d3be04

FROM "$IMAGE":"$IMAGE_TAG"

ENV NPM_BUILD_COMMAND=compile
ARG BUILD_VERSION
ENV BUILD_VERSION="$BUILD_VERSION"
ARG CONTAINER_IMAGE
ENV CONTAINER_IMAGE="$CONTAINER_IMAGE"

ENV COOLDOWN_PERIOD=0

# Copy in the application code
COPY --chown=app . .

# Install dependencies
RUN tna-build

# Copy in the static assets
RUN mkdir /app/app/static/assets; \
    cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets/* /app/app/static/assets;

# Delete source files
RUN rm -fR /app/src

# Clean up build dependencies
RUN tna-clean

# Run the application
CMD ["tna-wsgi", "main:app"]
