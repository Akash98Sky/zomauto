# Stage 1: Build the React app
FROM node:alpine AS build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install --force

COPY frontend/. .
ENV NODE_OPTIONS="--openssl-legacy-provider"
RUN npm run build

# Stage 2: Serve the built app with Nginx
FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
        python3-pip python3-venv \
        software-properties-common wget

RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
RUN apt-get update && apt-get install -y microsoft-edge-stable

WORKDIR /app

COPY requirements.txt .
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt

ENV PATH="${PATH}:/app/venv/bin"

COPY . .
COPY --from=build /app/build frontend/build

EXPOSE 80

CMD ["fastapi", "run", "app.py", "--host", "0.0.0.0", "--port", "80"]