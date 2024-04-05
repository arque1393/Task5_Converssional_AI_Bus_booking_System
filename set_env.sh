#!/bin/bash
touch .env
echo "GOOGLE_API_KEY=$GOOGLE_API_KEY" > .env
echo "GROQ_API_KEY=$GROQ_API_KEY" >> .env
echo "LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY" >> .env
echo "LANGCHAIN_TRACING_V2=true" >> .env
echo "LANGCHAIN_ENDPOINT=https://api.smith.langchain.com" >> .env
echo "DATABASE_USER=$DATABASE_USER" >> .env
echo "DATABASE_NAME=$DATABASE_NAME" >> .env
echo "DATABASE_PASSWORD=$DATABASE_PASSWORD" >> .env
echo "DATABASE_HOST=$DATABASE_HOST" >> .env
echo "DATABASE_PORT=$DATABASE_PORT" >> .env
echo "JWT_AUTH_SECRET_KEY=$JWT_AUTH_SECRET_KEY" >> .env
echo "ALGORITHM=HS256" >> .env