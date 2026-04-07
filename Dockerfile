# ==== Stage 1: Build the Launcher Frontend ====
FROM node:20 AS launcher-builder
WORKDIR /app
COPY Games/Launcher/package*.json ./Games/Launcher/
WORKDIR /app/Games/Launcher
RUN npm install
COPY Games/Launcher/ ./
COPY SharedAssets/ /app/SharedAssets/
RUN npm run build

# ==== Stage 2: Build the DrawJudge Frontend ====
FROM node:20 AS drawjudge-builder
WORKDIR /app
COPY Games/DrawJudge/package*.json ./Games/DrawJudge/
WORKDIR /app/Games/DrawJudge
RUN npm install
COPY Games/DrawJudge/ ./
COPY SharedAssets/ /app/SharedAssets/
RUN npm run build

# ==== Stage 3: Build the FastAPI Backend ====
FROM python:3.11-slim
WORKDIR /app

# Copy the compiled React assets from the Node containers
COPY --from=launcher-builder /app/Games/Launcher/dist /app/Games/Launcher/dist
COPY --from=drawjudge-builder /app/Games/DrawJudge/dist /app/Games/DrawJudge/dist

# Setup backend
COPY Server/ /app/Server/
WORKDIR /app/Server
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
