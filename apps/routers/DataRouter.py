import json
from fastapi import APIRouter, Body, Response
from main import PARAMS
from apps.controllers.DataController import ControllerData as c

APPS_INFORMATION = PARAMS.APPS_INFORMATION
router = APIRouter()

@router.get("/get_contents")
async def get_contents():
    contents = c.get_contents()
    return contents

@router.post('/save_to_db')
async def save_to_db(response:Response):
    result = c.save_to_db()
    return result

@router.put('/update_author')
async def update_author(response:Response):
    result = c.update_author()
    return result

@router.delete("/delete_publisher")
async def delete_publisher(response: Response, publisher=None):
    result = c.delete_publisher(publisher=publisher)
    return result