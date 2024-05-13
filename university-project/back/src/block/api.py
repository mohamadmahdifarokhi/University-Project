
from fastapi import APIRouter, Depends, Body
from src.db import db
from .schemas import *
from .services import *


router = APIRouter(
    prefix="/blocks",
    tags=["Blocks"],
)

@router.get("/blocks", summary="Get all blocks of an apartment")
def blocks_list_all(
    apartment_id: str
):
    return service_list_apartment_blocks(
        apartment_id=apartment_id
    )

@router.post("/blocks", summary="adds a block to a user")
def block_add(
    block: BlockSchemaCreate,
    user: User = Depends(get_current_user)
):
    return service_add_block(
        block=block,
        user_id=user["_id"]
    )

@router.delete("/blocks", summary="deletes a block from a user")
def power_record_delete(
    block_id: str,
    user: User = Depends(get_current_user)

):
    return service_delete_block(
        block_id
    )


