from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from .schemas import (
    OrderResList,
)
from .services import (
    OrderService,
)
from ..auth.models import User
from ..auth.secures import get_current_user
from ..db.db import sess_db

router = APIRouter(tags=["Orders"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=OrderResList,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Orders not found"},
    },
)
def get_orders_by_user_id_route(
        user: User = Depends(get_current_user),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
):
    """Retrieve orders by user ID with pagination."""
    orders = OrderService().get_by_user_id(user, page, page_size)
    return orders

