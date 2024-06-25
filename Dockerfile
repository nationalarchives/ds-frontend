ARG IMAGE=ghcr.io/nationalarchives/tna-python
ARG IMAGE_TAG=latest
ARG IMAGE_VERSION

FROM "$IMAGE":"$IMAGE_TAG"

ENV NPM_BUILD_COMMAND=compile
ENV IMAGE_VERSION=${IMAGE_VERSION}

# Copy in the application code
COPY --chown=app . .

# Install dependencies
RUN tna-build

# Copy in the static assets from TNA Frontend
RUN mkdir /app/app/static/assets; \
    cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets/* /app/app/static/assets

# Delete source files and tests
RUN rm -fR /app/src /app/test

# Run the application
CMD ["tna-run", "etna:app"]
