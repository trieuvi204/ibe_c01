from . import schemas
from . import models
from fastapi import HTTPException

fake_db = []

# Does the user exist?
async def get_user_by_email(email:str):
  for user in fake_db:
    if user['email']  == email:
      return user
  return  None
  
#  Register user
async def register_user(data: schemas.RegisterUserRequest) -> models.Users:
  user = models.Users(**data).model_dump()
  # Check if the user already exists
  if await get_user_by_email(user["email"]):
    # error 420: User email already exists
    raise HTTPException(420, detail="User email already exists")
  fake_db.append(user)
  return user

#  Login user
async def login_user(data:schemas.LoginUserRequest) -> models.Users:
  user = await get_user_by_email(data["email"])
  if user is None:
    # error 421: User not found
    raise HTTPException(421, detail="User not found")
  
  if user["password"] != data["password"]:
    # error 423: Password not match
    raise HTTPException(423, detail="Password not match")
  return user

#  Get me all
async def get_me_all() -> list[models.Users]:
  if len(fake_db) == 0:
    # error 424: Database is empty
    raise HTTPException(424, detail="Database is empty")
  users = [models.Users(**user).model_dump() for user in fake_db]
  return users



#  Get me
async def get_me(data: str) -> models.Users:
  if len(fake_db) == 0:
    # error 423: Database is empty
    raise HTTPException(424, detail="Database is empty")
  user = await get_user_by_email(data)
  if user is None:
    print("user: ", user)
    # error 421: User not found
    raise HTTPException(421, detail="User not found")
  print(user)
  return user

# check modified
async def check_modified(data: dict, user: models.Users) -> bool:
  for key, value in data.items():
    if user[key] != value:
      return True
  return False

# Update me
async def update_me(data: schemas.UpdateMeRequest) -> models.Users:
  if len(fake_db) == 0:
    # error 423: Database is empty
    raise HTTPException(424, detail="Database is empty") 
  user = await get_me(data["email"])
  is_modified = await check_modified(data, user)
  if is_modified is False:
    # error 304: No data is modified
    raise HTTPException(304, detail="No data is modified")
  user.update(data)
  fake_db[0] = user
  return user


# Delete me
async def delete_me(email: str):
  if len(fake_db) == 0:
    # error 423: Database is empty
    raise HTTPException(424, detail="Database is empty")
  user = await get_me(email)
  if user is None:
    # error 421: User not found
    raise HTTPException(421, detail="User not found")
  
  fake_db.remove(user)
  return None