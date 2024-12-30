from fastapi import APIRouter

from . import schemas
from . import services
router = APIRouter(prefix= "/v1/users", tags=["users"])

# router user registration
@router.post("/register" ,status_code = 201, response_model = schemas.RegisterUserRespone, responses = {
  420: {"model": schemas.ErrorResponse, "description": "User email already exists"},
  422: {"model": schemas.ErrorResponse, "description": "Invalid format"}
}) 
async def register(data: schemas.RegisterUserRequest):
  data = data.model_dump()
  result = await services.register_user(data)
  return schemas.RegisterUserRespone(**result)

# router user login
@router.post("/login", status_code = 201, response_model = schemas.LoginUserResponse, responses = {
  421: {"model": schemas.ErrorResponse, "description": "User not found"},
  423: {"model": schemas.ErrorResponse, "description": "Password not match"}
})
async def login(data: schemas.LoginUserRequest):
  data =  data.model_dump()
  result = await services.login_user(data)
  return schemas.LoginUserResponse(**result)

# router get all user
@router.get("/me/all", status_code= 200 ,response_model= list[schemas.GetMeResponse], responses = {
  424: {"model": schemas.ErrorResponse, "description": "Database is empty"} 
})
async def get_me_all():
  result = await services.get_me_all()
  # return all users
  return [schemas.GetMeResponse(**item) for item in result]

# router get me
@router.get("/me", status_code=200, response_model= schemas.GetMeResponse, responses = {
  421: {"model": schemas.ErrorResponse, "description": "User not found"},
  424: {"model": schemas.ErrorResponse, "description": "Database is empty"}
})
async def get_me(email: str):
  result = await services.get_me(email)
  return schemas.GetMeResponse(**result)

# router update me
@router.put("/me", status_code=200, response_model=schemas.UpdateMeResponse, responses= {
  423: {"model": schemas.ErrorResponse, "description": "Database is empty"},
  421: {"model": schemas.ErrorResponse, "description": "User not found"},
  422: {"model": schemas.ErrorResponse, "description": "Invalid format"},
  427: {"model": schemas.ErrorResponse, "description": "Update failed"}
})
async def update_me(data: schemas.UpdateMeRequest, email: str):
  data = data.model_dump(exclude_none=True)
  result = await services.update_me(data, email)
  return schemas.UpdateMeResponse(**result) 

# router delete me
@router.delete("/me", status_code=204, responses = {
  424: {"model": schemas.ErrorResponse, "description": "Database is empty"},
  421: {"model": schemas.ErrorResponse, "description": "User not found"}
})
async def delete_me(email: str):
  await services.delete_me(email)