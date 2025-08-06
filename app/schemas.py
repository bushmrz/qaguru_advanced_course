from pydantic import BaseModel

# Пользователи
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# Токен
class Token(BaseModel):
    access_token: str
    token_type: str

# Предметы
class ItemCreate(BaseModel):
    title: str
    description: str = None

class ItemOut(BaseModel):
    id: int
    title: str
    description: str = None

    class Config:
        orm_mode = True