from fastapi import Depends, HTTPException
from buscabook.config import oauth_schema, SECRET_KEY, ALGORITHM
from buscabook.database import get_session
from buscabook.models import User
from sqlalchemy.orm import Session
from jose import jwt, JWTError

def verify_token(token: str = Depends(oauth_schema), session: Session = Depends(get_session)):

    try:
        token_content = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = token_content.get("sub")
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido.")
    
    user = session.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    else:
        return user