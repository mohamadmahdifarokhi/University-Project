# from pydantic import UUID4, BaseModel, PositiveFloat
#
#
# class ReviewReq(BaseModel):
#     is_reply: bool = False
#     head: str
#     body: str
#     rating: PositiveFloat
#     user_id: UUID4
#     product_id: UUID4
#     reply_id: UUID4 = None
#
#
# class ReviewUpdate(BaseModel):
#     is_reply: bool = None
#     head: str = None
#     body: str = None
#     rating: PositiveFloat = None
#     user_id: UUID4 = None
#     product_id: UUID4 = None
#     reply_id: UUID4 = None
#
#
# class ReviewRes(BaseModel):
#     id: UUID4
#     is_reply: bool
#     head: str
#     body: str
#     rating: PositiveFloat
#     user_id: UUID4
#     product_id: UUID4
#     reply_id: UUID4 | None = None
