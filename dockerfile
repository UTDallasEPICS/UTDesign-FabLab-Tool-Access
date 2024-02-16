ARG NODE_VERSION=20.9.0

FROM node:${NODE_VERSION}-alpine

# Set the working directory in the container
WORKDIR /app

# Install the MySQL client
RUN apk add --no-cache mariadb-client

# Copy package.json and package-lock.json to leverage Docker cache
COPY package*.json ./

# Install app dependencies
RUN npm ci --only=production

ENV DOCKER=true

# Bundle app source
COPY . .

# Expose the port that the application listens on
EXPOSE 3000

# Run the application only if the database is reachable
CMD ["sh", "-c", "node Docker/healthcheck.js && node server.js"]

