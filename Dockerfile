FROM python:3.11.9-slim
WORKDIR /app
COPY . .
RUN python -m venv ./out

RUN apt-get update && apt-get install -y cmake protobuf-compiler libprotobuf-dev 
RUN chmod +x ./out/bin/activate
RUN ./out/bin/activate
RUN pip install -r requirements/base.txt
RUN ./out/bin/activate
EXPOSE 8000
CMD ["./out/bin/python", "-m", "src.main"]