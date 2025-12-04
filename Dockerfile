ARG IMAGE=ghcr.io/nationalarchives/tna-python
ARG IMAGE_TAG=latest

FROM "$IMAGE":"$IMAGE_TAG"

ENV NPM_BUILD_COMMAND=compile
ARG BUILD_VERSION
ENV BUILD_VERSION="$BUILD_VERSION"
ARG CONTAINER_IMAGE
ENV CONTAINER_IMAGE="$CONTAINER_IMAGE"

# Copy in the application code
COPY --chown=app . .

# Install dependencies
RUN tna-build

# Copy in the static assets
RUN mkdir /app/app/static/assets; \
    cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets/* /app/app/static/assets;
# Delete source files
RUN rm -fR /app/src

# RUN tna-clean  # TODO: Enable once the new images have been published

# Run the application
CMD ["tna-wsgi", "ds_frontend:app"]
