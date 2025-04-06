from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


# по доке будет работать только если будет выше, чем параметризированный путь, иначе нет
@app.get("/products/search")
def search_products(keyword: str, category: str | None = None, limit: int = 0) -> list[Product]:
    return_json_list = []
    i_limit = 0
    for dict_item in sample_products:
        if keyword.lower() in dict_item["name"].lower() and (category is None or category.lower() == dict_item["category"].lower()):
            if limit == 0 or i_limit < limit:
                return_json_list.append(Product(**dict_item))
                i_limit += 1
            else:
                break
    return return_json_list

@app.get("/products/{product_id}")
def get_product_info(product_id: int) -> Product | str:
    if product_id < len(sample_products):
        return Product(**sample_products[product_id])
    else:
        return "Product not found"