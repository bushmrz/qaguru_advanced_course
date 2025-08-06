from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime
from models import BlacklistedToken


SECRET_KEY = "IkPrVBpGluzodSyP-EnjevDkt7XJqP49gBNPzw4IgqY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def is_token_blacklisted(db: Session, token: str):
    blacklisted = db.query(BlacklistedToken).filter(BlacklistedToken.token == token).first()
    return blacklisted is not None

def blacklist_token(db: Session, token: str):
    blacklisted_token = BlacklistedToken(token=token)
    db.add(blacklisted_token)
    db.commit()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None