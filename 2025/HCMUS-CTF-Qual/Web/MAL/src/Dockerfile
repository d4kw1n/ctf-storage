FROM node:21.5-slim@sha256:c88704924204ee6d4e9da02275a8fd27355502f7177e4175cd0d3a4375a9c9c8

RUN apt-get update && \
  apt-get install -y ca-certificates && \
  rm -rf /var/lib/apt/lists/*

ARG DEBIAN_FRONTEND=noninteractive
ENV NODE_ENV=production
ENV PORT=80
ENV USER=app

RUN ln -sf /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime
RUN dpkg-reconfigure tzdata

# Set working directory
RUN mkdir /app
RUN mkdir /archive
WORKDIR /app

# Add files
COPY --from=curlimages/curl:7.69.0 /usr/bin/curl /usr/sbin/curl
COPY --from=curlimages/curl:7.69.0 /usr/lib /usr/lib
COPY --from=curlimages/curl:7.69.0 /lib /lib

COPY --chown=root:root ./app /app/
COPY --chown=root:root ./archive /archive/

# Install dependencies
RUN npm install

EXPOSE $PORT

CMD ["node", "app.js"]