FROM node:22-slim AS development

WORKDIR /app

COPY package*.json ./

RUN npm ci --development
RUN rm -rf .npmrc

COPY tsconfig*.json ./
COPY nest*.json ./
COPY src/ src/

RUN npm run build

FROM node:22-slim AS builder

WORKDIR /app

ENV MONGOMS_VERSION=7.0.14

COPY package*.json ./

RUN npm install

FROM node:22-slim AS production

WORKDIR /app

RUN apt-get update \
  && apt-get install wget gdebi-core libcurl4 -y \
  && wget http://ftp.us.debian.org/debian/pool/main/o/openssl/libssl1.1_1.1.1n-0+deb10u3_amd64.deb \
  && gdebi --non-interactive libssl1.1_1.1.1n-0+deb10u3_amd64.deb \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && rm libssl1.1_1.1.1n-0+deb10u3_amd64.deb

RUN mkdir data

ENV MONGOMS_DISABLE_POSTINSTALL=true
ENV MONGOMS_SYSTEM_BINARY=/app/node_modules/.cache/mongodb-memory-server/mongod-x64-debian-7.0.14
ENV user=dat2phit

RUN adduser --disabled-password $user
RUN chown -R $user:$user /app/data

COPY flag /flag
RUN openssl rand -hex 16 | xargs -I {} mv /flag /{}

COPY --from=builder /app/node_modules ./node_modules
COPY --from=development /app/dist ./dist

EXPOSE 3000

USER $user

CMD ["node", "dist/main"]