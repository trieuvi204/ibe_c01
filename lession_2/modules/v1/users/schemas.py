from pydantic import BaseModel
from typing import Optional

# error response
class ErrorResponse(BaseModel):
  detail: str
# error response


# Register user
# Register user request
class RegisterUserRequest(BaseModel):
  fullname: str
  email: str
  password: str

# Register user response
class RegisterUserRespone(BaseModel):
  fullname: str
  password:str
  email: str
  phone_number: Optional[str] = None

# Register user

# Login user
# Login user request
class LoginUserRequest(BaseModel):
  email:str
  password:str

# Login user response
class LoginUserResponse(RegisterUserRespone):
  pass

# Login user

# Get me
# Get me response
class GetMeResponse(RegisterUserRespone):
  pass

# Get me request
class GetMeRequest(RegisterUserRequest):
  pass
# Get me

# Update me
# Update me request
class UpdateMeRequest(BaseModel):
  fullname: Optional[str] = None
  email: Optional[str] = None
  phone_number: Optional[str] = None
  password: Optional[str] = None
  
# Update me response
class UpdateMeResponse(RegisterUserRespone):
  pass
# Update me

