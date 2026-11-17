from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str = Field(..., description="User login email")
    password: str = Field(..., min_length=6, description="Plaintext password to be hashed")

class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
