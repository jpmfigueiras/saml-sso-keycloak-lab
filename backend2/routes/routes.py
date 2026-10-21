import os
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from helper import prepare_fastapi_request
from controllers.user_controller import UserController
from config import Settings

settings = Settings()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
SAML_DIR = os.path.join(BASE_DIR, "saml")

# Auth Router (SAML)
auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@auth_router.get("/login")
def login(request: Request):
    '''
    Initiates the SAML login process by redirecting the user to the Identity Provider (IdP) login page.
    
    Parameters:
        ------------
        request: Request object from FastAPI.
    
    Returns:
        ------------
        RedirectResponse: Redirects the user to the SAML login URL.
    '''
    req = prepare_fastapi_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=SAML_DIR)
    return RedirectResponse(url=auth.login(), status_code=302)

@auth_router.post("/saml/acs")
async def saml_acs(request: Request, db: Session = Depends(get_db)):
    '''
    Processes the SAML authentication response from the Identity Provider (IdP).
    Creates or updates user in the database and sets authentication cookies.
    
    Parameters:
        ------------
        request: Request object from FastAPI.
        db: Database session.
    
    Returns:
        ------------
        RedirectResponse: Redirects the user to the frontend with authentication cookies set.
    '''
    form = await request.form()
    req = prepare_fastapi_request(request, dict(form))
    auth = OneLogin_Saml2_Auth(req, custom_base_path=SAML_DIR)
    auth.process_response()
    errors = auth.get_errors()
    if(errors):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "SAML response error",
                "errors": errors,
                "last_error_reason": auth.get_last_error_reason()
            }
        )
    if(not auth.is_authenticated()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    print("APP2 - antes process_response", flush=True)
    attributes = auth.get_attributes()
    print("APP2 - depois process_response", flush=True)
    name_id = auth.get_nameid()
    session_index = auth.get_session_index()
    first_name = attributes.get("first_name", [None])[0]
    last_name = attributes.get("last_name", [None])[0]
    email = attributes.get("email", [None])[0]
    roles = attributes.get("role", [])
    print("ROLES app2:", roles, flush=True)
    role = roles[0] if roles else "user"
    print("Creating/updating user app2:", email, name_id, first_name, last_name, role, flush=True)
    user = UserController.create_or_update_saml_user(
        email=email,
        username=name_id,
        app_name=settings.app_name,
        first_name=first_name,
        last_name=last_name,
        role=role,
        db=db
    )
    response = RedirectResponse(url="http://localhost:3001", status_code=302)
    response.set_cookie("access_token", user.username, httponly=True, samesite="lax")
    response.set_cookie("saml_name_id", name_id or "", httponly=True, samesite="lax")
    response.set_cookie("saml_session_index", session_index or "", httponly=True, samesite="lax")
    return response

@auth_router.get("/me")
def me(request: Request, db: Session = Depends(get_db)):
    '''
    Retrieves the current authenticated user's information.
    
    Parameters:
        ------------
        request: Request object from FastAPI.
        db: Database session.
    
    Returns:
        ------------
        dict: User information (id, email, username, is_active).
    '''
    username = request.cookies.get("access_token")
    if (not username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    user = UserController.get_user_by_username(username=username, app_name=settings.app_name, db=db)
    return {
        "email": user.email,
        "username": user.username,
        "role": user.role,
        "is_active": user.is_active
    }

@auth_router.get("/logout")
def logout(request: Request):
    '''
    Initiates the SAML logout process by redirecting the user to the Identity Provider (IdP) logout page.
    
    Parameters:
        ------------
        request: Request object from FastAPI.
    
    Returns:
        ------------
        RedirectResponse: Redirects the user to the SAML logout URL and clears authentication cookies.
    '''
    req = prepare_fastapi_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=SAML_DIR)
    name_id = request.cookies.get("saml_name_id")
    session_index = request.cookies.get("saml_session_index")
    slo_url = auth.logout(
        name_id=name_id,
        session_index=session_index,
        return_to="http://localhost:3001/login"
    )
    response = RedirectResponse(url=slo_url, status_code=302)
    response.delete_cookie("access_token")
    response.delete_cookie("saml_name_id")
    response.delete_cookie("saml_session_index")
    return response

@auth_router.get("/saml/sls")
@auth_router.post("/saml/sls")
async def saml_sls(request: Request):
    '''
    Processes the SAML Single Logout (SLO) response from the Identity Provider (IdP).
    Handles both GET (HTTP-REDIRECT) and POST (HTTP-POST) bindings.
    
    Parameters:
        ------------
        request: Request object from FastAPI.
    
    Returns:
        ------------
        RedirectResponse: Redirects the user to the login page and clears all authentication cookies.
    '''
    if (request.method == "POST"):
        form = await request.form()
        req = prepare_fastapi_request(request, dict(form))
    else:
        req = prepare_fastapi_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=SAML_DIR)
    redirect_url = auth.process_slo(delete_session_cb=lambda: None)
    errors = auth.get_errors()
    if (errors):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "SAML logout error",
                "errors": errors,
                "reason": auth.get_last_error_reason()
            }
        )
    response = RedirectResponse(
        url=redirect_url or "http://localhost:3001/login",
        status_code=302
    )
    response.delete_cookie("access_token")
    response.delete_cookie("saml_name_id")
    response.delete_cookie("saml_session_index")
    return response
