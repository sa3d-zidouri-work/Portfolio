FROM caddy:2-alpine

COPY Caddyfile /etc/caddy/Caddyfile

# Copy the whole site. Adding new pages, CSS, or images later needs no change
# here -- just commit them and push.
COPY . /srv/

# Build and config files must not be publicly served. (.dockerignore can't do
# this job: excluding the Caddyfile there would also hide it from the COPY above.)
RUN rm -f /srv/Dockerfile /srv/Caddyfile /srv/.dockerignore /srv/README.md

EXPOSE 80
