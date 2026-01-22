ARG BUILD_IMAGE=ghcr.io/nationalarchives/tna-python-dev
ARG BUILD_IMAGE_TAG=multistage-builds

ARG IMAGE=ghcr.io/nationalarchives/tna-python
ARG IMAGE_TAG=multistage-builds



FROM "$BUILD_IMAGE":"$BUILD_IMAGE_TAG" AS build

ENV NPM_BUILD_COMMAND=compile

# Copy in the application code
COPY . .

# Install dependencies
RUN tna-build

# Copy in the static assets
RUN mkdir /app/app/static/assets; \
    cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets/* /app/app/static/assets;



FROM "$IMAGE":"$IMAGE_TAG" AS runtime

ARG BUILD_VERSION
ENV BUILD_VERSION="$BUILD_VERSION"
ARG CONTAINER_IMAGE
ENV CONTAINER_IMAGE="$CONTAINER_IMAGE"

# Copy in the application code
COPY . .

# Install dependencies
RUN tna-build

# Copy in the built assets
COPY --from=build /app/app/static /app/app/static

# Clean up build dependencies
RUN tna-clean

# Run the application
CMD ["tna-wsgi", "main:app"]
