FROM node:21.5-bookworm-slim as frontend
RUN mkdir -p /app
WORKDIR /app
COPY ./ /app
WORKDIR /app/chatbot-frontend
RUN npm install
RUN npm run build


FROM python:3.11-slim-bookworm as backend

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

RUN mkdir -p /app
WORKDIR /app
COPY ./ /app
RUN pip install -r requirements.txt
COPY --from=frontend /app/llm_server/build /app/llm_server/build

ENV FLASK_ENV production
EXPOSE 5000
CMD ["flask", "--app", "llm_server", "run", "--host=0.0.0.0"]

