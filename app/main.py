from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import engine, SessionLocal
import models
import schemas
import auth
from users import create_user, authenticate_user, get_user_by_username


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if await auth.is_token_blacklisted(db, token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is revoked")
    username = await auth.verify_token(token)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/register/", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_username(db, user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = create_user(db, user_in)
    return user

@app.post("/login/", response_model=schemas.Token)
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_in.username, user_in.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/items/", response_model=schemas.ItemOut)
def create_item(item: schemas.ItemCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_item = models.Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[schemas.ItemOut])
def read_items(skip: int=0, limit: int=10, db: Session=Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=schemas.ItemOut)
def read_item(item_id: int, db: Session=Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=schemas.ItemOut)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session=Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.title = item.title
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session=Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

@app.post("/logout/")
def logout(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    auth.blacklist_token(db, token)
    return {"detail": "Successfully logged out"}
