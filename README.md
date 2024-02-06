# AI2 SPECTER2 docker inference image

This repository contains the code for building a docker image for serving the [AI2 SPECTER2](https://github.com/allenai/SPECTER2) model for document embedding and retrieval. It provides only two endpoints on port `8080`:

- `GET /`: for checking the health of the service.
- `POST /`: for embedding a list of documents. The request body should be a JSON object with a single key `documents` that contains a list of strings. The response will be a JSON object with a single key `embeddings` that contains a list of lists of floats, where each inner list is the embedding of the corresponding document.

As of now, the image is built with `allenai/specter2_base` weights cached during the build process and `allenai/specter2` adapter weights downloaded at runtime. The image is built with the `gpu` version of `transformers`.

**Example:**

```bash
docker run -p 8080:8080 yegortokmakov/specter2

curl http://localhost:8080

> {"message":"OK"}

curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"documents": ["This is a test document", "This is another test document"]}' \
    http://localhost:8080

> {"embeddings":[[0.0,0.0,0.0,...],[0.0,0.0,0.0,...]]}
```

Image builds are available on Docker Hub at [https://hub.docker.com/r/yegortokmakov/specter2](https://hub.docker.com/r/yegortokmakov/specter2). Contributions are welcome!
