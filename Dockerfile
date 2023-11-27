FROM ghcr.io/nationalarchives/tna-python:latest

ENV NPM_BUILD_COMMAND=build

# Copy in the application code
COPY --chown=app . .

# Install the dependencies
RUN tna-build

# Delete the source files
RUN rm -fR /app/src

# Run the application
CMD ["tna-run", "my-app:app"]
