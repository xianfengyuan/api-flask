# CONTRIBUTING

## How to run docker locally

```
docker run -p 5005:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```
