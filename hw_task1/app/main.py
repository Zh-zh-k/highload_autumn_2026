from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Items Service")


class Item(BaseModel):
    name: str
    description: str | None = None


items: dict[int, Item] = {}
next_id = 1


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/items", status_code=201)
async def create_item(item: Item):
    global next_id

    item_id = next_id
    items[item_id] = item
    next_id += 1

    return {"id": item_id, **item.model_dump()}


@app.get("/items/{id}")
async def get_item(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"id": id, **items[id].model_dump()}


@app.put("/items/{id}")
async def update_item(id: int, item: Item):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    items[id] = item
    return {"id": id, **item.model_dump()}
