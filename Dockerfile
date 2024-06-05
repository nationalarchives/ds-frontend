ARG IMAGE_TAG=latest

FROM ghcr.io/nationalarchives/tna-python:"$IMAGE_TAG"

ENV NPM_BUILD_COMMAND=compile

# Copy in the application code
COPY --chown=app . .

# Install the dependencies
RUN tna-build

RUN mkdir /app/app/static/assets; \
    cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets/* /app/app/static/assets

# Delete the source files
RUN rm -fR /app/src

# Run the application
CMD ["tna-run", "etna:app"]
