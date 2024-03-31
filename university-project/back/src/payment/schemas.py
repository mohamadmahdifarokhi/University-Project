from pydantic import BaseModel


class PaymentVerification(BaseModel):
    authority: str
    status: str
    id: str
