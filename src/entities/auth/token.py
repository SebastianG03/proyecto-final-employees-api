from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    class Config:
        from_attributes=True
        arbitrary_types_allowed=True


class TokenData():
    username: str = "Anon" #Anonimus
    scopes: list[str] = []
