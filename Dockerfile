FROM huggingface/transformers-pytorch-gpu:4.35.2

RUN python3 -m pip install pydantic==1.10.5
RUN python3 -m pip install adapters==0.1.0
RUN python3 -m pip install gunicorn uvicorn
RUN python3 -m pip install fastapi

# Set the environment variable for the Hugging Face cache directory
ENV TRANSFORMERS_CACHE=/hf_cache
WORKDIR /hf_cache
RUN python3 -c "from huggingface_hub import snapshot_download;snapshot_download(repo_id='allenai/specter2_base',cache_dir='/hf_cache');"

WORKDIR /app

COPY app .

CMD ["gunicorn","-b","0.0.0.0:8080","app:app","--workers","1","-k","uvicorn.workers.UvicornWorker"]
