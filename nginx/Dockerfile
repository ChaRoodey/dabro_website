FROM node:20-alpine AS builder

WORKDIR /app

COPY dabro_frontend/package.json dabro_frontend/package-lock.json ./
RUN npm ci

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

COPY dabro_frontend ./
RUN npm run build


FROM nginx:1.27-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80