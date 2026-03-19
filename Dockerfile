# Stage 1: Build the React Frontend
FROM node:20-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

# Stage 2: Configure the FastAPI Backend
FROM python:3.11-slim
WORKDIR /app

# Copy the built React assets
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Copy and setup the backend
COPY backend /app/backend
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
