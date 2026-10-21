from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from data_model.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserController:
    """Controller for user-related operations"""
    
    @staticmethod
    def create_user(email: str, username: str, password: str, db: Session):
        """Create a new user"""
        # Check if user already exists by email
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username is taken
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        hashed_password = pwd_context.hash(password)
        new_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def get_all_users(skip: int, limit: int, db: Session):
        """Get all users with pagination"""
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    
    @staticmethod
    def get_user_by_username(username: str, app_name: str, db: Session):
        """Get user by username and app_name"""
        user = db.query(User).filter(User.username == username, User.app_name == app_name).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def get_user_by_email(email: str, db: Session):
        """Get user by email"""
        user = db.query(User).filter(User.email == email).first()
        return user
    
    @staticmethod
    def update_user(username: str, app_name: str, email: str = None,
                   is_active: bool = None, role: str = None, db: Session = None):
        """Update user information"""
        user = db.query(User).filter(User.username == username, User.app_name == app_name).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if email:
            user.email = email
        if is_active is not None:
            user.is_active = is_active
        if role:
            user.role = role
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(username: str, app_name: str, db: Session):
        """Delete user"""
        user = db.query(User).filter(User.username == username, User.app_name == app_name).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        return None
    
    @staticmethod
    def create_or_update_saml_user(email: str, username: str, app_name: str,
                                   first_name: str, last_name: str, role: str, db: Session):
        """Create or update user from SAML authentication"""
        print("USER2 app", app_name)
        user = db.query(User).filter(User.username == username, User.app_name == app_name).first()
        
        if (user):
            # Update existing user
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.role = role
            user.is_active = True
        else:
            # Create new user
            user = User(
                email=email,
                username=username,
                app_name=app_name,
                first_name=first_name,
                last_name=last_name,
                role=role,
                is_active=True
            )
            db.add(user)
        
        db.commit()
        db.refresh(user)
        return user
