from pydantic import BaseModel, field_validator
from typing import Optional
import re
from fastapi import HTTPException

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

  # validate email using field validator
  @field_validator("email")
  def validate_email(cls, value: str) -> str:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
      raise HTTPException(422, detail="Invalid email format")
    return value




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

