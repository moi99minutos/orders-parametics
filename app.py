import json
import os

from datetime import date, datetime
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('MONGO_DB')]

def json_serial(encoder, obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

json.JSONEncoder.default = json_serial 

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class OrderParametricModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    order_identifier: str = Field(...)
    weight: float = Field(...)
    length: float = Field(...)
    width: float = Field(...)
    height: float = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "order_identifier": "12340987123",
                "weight": 15.1,
                "length": 15.0,
                "width": 3.0,
                "height": 3.235,
            }
        }

@app.post("/", response_description="Add new order parametric", response_model=OrderParametricModel)
async def create_order(order: OrderParametricModel = Body(...)):
    order = jsonable_encoder(order)
    order['created_at'] = datetime.now()

    if (counter := await db["order-details"].find_one({'$or': [{"counter": order.get('counter')}, {"identifier": order.get('counter')}]})) is None:
        raise HTTPException(status_code=404, detail=f"Order detail {order.get('counter')} not found")
    new_order = await db["orders-parametrics"].insert_one(order)
    created_order = await db["orders-parametrics"].find_one({"_id": new_order.inserted_id})    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_order)


