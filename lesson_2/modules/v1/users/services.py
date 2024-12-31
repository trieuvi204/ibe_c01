from . import schemas
from . import models
from fastapi import HTTPException
from db.crud_db import BaseCRUB


database_url = "mongodb://localhost:27017/"
database_name = "ibe_app"
collection_name = "users"

database = BaseCRUB(database_url, database_name, collection_name)



# Does the user exist?
async def get_user_by_email(email:str) ->str:
  _email = await database.get_user_by_email(email)
  if _email is not None:
    return _email
  return  None
  
#  Register user
async def register_user(data: schemas.RegisterUserRequest) -> models.Users:
  user = models.Users(**data).model_dump()
  # Check if the user already exists
  if await get_user_by_email(user["email"]):
    # error 420: User email already exists
    raise HTTPException(420, detail="User email already exists")
  
  # validate password
  if len(user["password"]) < 8:
    # error 422: Password must be at least 8 characters
    raise HTTPException(422, detail="Password must be at least 8 characters") 
  if not any(char.isdigit() for char in user["password"]):
    # error 422: Password must contain at least one number
    raise HTTPException(422, detail="Password must contain at least one number")
  if not any(char.isupper() for char in user["password"]):
    # error 422: Password must contain at least one uppercase letter
    raise HTTPException(422, detail="Password must contain at least one uppercase letter")

  register_result = await database.save(user)
  return register_result

#  Login user
async def login_user(data:schemas.LoginUserRequest) -> models.Users:
  user = await get_user_by_email(data["email"])
  if user is None:
    # error 421: User not found
    raise HTTPException(421, detail="User not found")
  
  if data["password"] != user["password"]:
    # error 423: Password not match
    raise HTTPException(423, detail="Password not match")
  return user

#  Get me all
async def get_me_all() -> list[models.Users]:
  emails = await database.get_all_by_emails()
  if len(emails) == 0:
    # error 424: Database is empty
    raise HTTPException(424, detail="Database is empty")
  users = [models.Users(**user).model_dump() for user in emails]
  return users



#  Get me
async def get_me(data: str) -> models.Users:
  users = await database.get_all_by_emails()
  if len(users) == 0:
    # error 423: Database is empty
    raise HTTPException(424, detail="Database is empty")
  user = await get_user_by_email(data)
  if user is None:
    # error 421: User not found
    raise HTTPException(421, detail="User not found")
  return user

# check modified
async def check_modified(data: dict, user: models.Users) -> bool:
  for key, value in data.items():
    if user[key] != value:
      return True
  return False

# Update me
async def update_me(data: schemas.UpdateMeRequest, email: str) -> models.Users:
  users = await database.get_all_by_emails()
  if len(users) == 0:
    # error 423: Database is empty
    raise HTTPException(424, detail="Database is empty") 
  user = await get_user_by_email(email)
  if user is None:
    # error 421: User not found
    raise HTTPException(421, detail="User not found")
  is_modified = await check_modified(data, user)
  # validate password
  if len(data["password"]) < 8:
    # error 422: Password must be at least 8 characters
    raise HTTPException(422, detail="Password must be at least 8 characters") 
  if not any(char.isdigit() for char in data["password"]):
    # error 422: Password must contain at least one number
    raise HTTPException(422, detail="Password must contain at least one number")
  if not any(char.isupper() for char in data["password"]):
    # error 422: Password must contain at least one uppercase letter
    raise HTTPException(422, detail="Password must contain at least one uppercase letter")
  if is_modified is False:
    # error 304: No data is modified
    raise HTTPException(304, detail="No data is modified")
  user.update(data)
  updated_user = await database.update_by_email(email, user)
  if updated_user is False:
    # error 427: Update failed
    raise HTTPException(427, detail="Update failed")
  return user


# Delete me
async def delete_me(email: str) -> bool:
  users = await database.get_all_by_emails()
  if len(users) == 0:
    # error 423: Database is empty
    raise HTTPException(424, detail="Database is empty")
  user = await get_user_by_email(email)
  if user is None:
    # error 421: User not found
    raise HTTPException(421, detail="User not found")
  
  delete_result= await database.delete_by_email(email)
  print(delete_result)
  return delete_result