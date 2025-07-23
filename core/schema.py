from datetime import datetime

from pydantic import BaseModel


class JWTManagerSchema(BaseModel):
    token: str
    expires_at: datetime
    jti: str
    