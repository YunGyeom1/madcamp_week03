from sqlalchemy.orm import Session
from app.db.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(session: Session, email: str, password: str):
    hashed_password = generate_password_hash(password)
    user = User(email=email, password=hashed_password)
    session.add(user)
    session.commit()
    return user

def login_user(session: Session, email: str, password: str):
    user = session.query(User).filter(User.email == email).first()
    if user and check_password_hash(user.password, password):
        return {"success": True, "message": "Login successful", "user": user}
    return {"success": False, "message": "Invalid email or password"}