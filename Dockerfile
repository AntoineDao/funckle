# Stage 1: Build the frontend React app
FROM node:19 as frontend-build
ENV NODE_ENV production
WORKDIR /app/frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn
COPY frontend/ ./
RUN yarn build

# Stage 2: Build the Django backend and copy the frontend build
# FROM python:3.11 as backend-build
FROM python:3.11
WORKDIR /app/backend
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY server/ ./
COPY --from=frontend-build /app/frontend/build/ /app/backend/build/

# Stage 3: Create the final image for running the Django app
# FROM backend-build as final
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]


