FROM node:alpine
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install
# Le COPY est remplacé par un volume dans docker-compose.yml
CMD ["yarn", "dev", "--host"]
