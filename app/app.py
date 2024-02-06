import torch
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
import adapters

app = FastAPI()

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Device ", torch_device)
torch.set_grad_enabled(False)


tokenizer = AutoTokenizer.from_pretrained('allenai/specter2_base')
model = AutoModel.from_pretrained('allenai/specter2_base')

adapters.init(model)
adapter_name = model.load_adapter("allenai/specter2", source="hf",
                                  load_as="specter2", set_active=True)
model.set_active_adapters(adapter_name)

model = model.to(torch_device)


class EmbeddingsRequest(BaseModel):
    documents: List[str]


@app.get('/')
async def home():
    return {"message": "OK"}


@app.post("/")
async def getembeddings(request_in: EmbeddingsRequest):
    # preprocess the input
    text_batch = [text.strip() for text in request_in.documents]
    inputs = tokenizer(text_batch, padding=True, truncation=True,
                       return_tensors="pt", return_token_type_ids=False, max_length=512).to(torch_device)
    output = model(**inputs)
    # take the first token in the batch as the embedding
    embeddings = output.last_hidden_state[:, 0, :]
    return embeddings.cpu().numpy().tolist()
