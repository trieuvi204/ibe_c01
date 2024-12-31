from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

class BaseCRUB:
  def __init__(self, database_url: str, database_name: str, collection_name: str):
    self.database_url = database_url
    self.database_name = database_name
    self.collection_name = collection_name
    self.client = self.connect()
    self.db = self.client[self.database_name]
    self.collection = self.db[self.collection_name]

  def connect(self) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(self.database_url)
  
  async def save(self, document: dict) -> dict:
    result = await self.collection.insert_one(document)
    # Thêm trường _id vào document và trả về toàn bộ tài liệu
    document["_id"] = result.inserted_id
    return document

  
  async def get_email_by_email(self, email:str) -> str:
    query = {"email": email}
    document = await self.get_document_by_query(query)
    return document["email"]
  
  async def get_user_by_email(self, email:str) -> str:
    query = {"email": email}
    document = await self.get_document_by_query(query)
    if document is None:
      return None
    return document

  async def get_by_password(self, password:str) -> str:
    query = {"password": password}
    document = await self.get_document_by_query(query)
    if document is None:
      return None
    return document["password"]
  
  async def get_document_by_query(self, query: str) -> str:
    return await self.collection.find_one(query)


  async def get_documents_by_query(self, query):
    documents = self.collection.find(query)
    result = []
    async for document in documents:
      result.append(document)
    return result
  
  async def get_all_by_emails(self) -> list:
    documents = self.collection.find({})
    users = []
    async for document in documents:
      # Chuyển ObjectId thành chuỗi
      document['_id'] = str(document['_id'])
      users.append(document)
    return users
  
  async def update_by_email(self, _email: str, new_user_data: dict) -> bool:
    query = {"email": _email}
    new_values = {"$set": new_user_data}
    result = await self.collection.update_one(query, new_values)
    
    return result.modified_count > 0
  
  async def delete_by_email(self, email) -> bool:
    query = {"email": email}
    result = await self.collection.delete_one(query)
    return result.deleted_count > 0
  
# async def main():
#   database_url = "mongodb://localhost:27017/"
#   database_name = "ibe_app"
#   collection_name = "users"

#   data = {
#     "fullname": "trieuvi",
#     "email": "caodinhtrieuvi2004@gmail.com",
#     "password": "Trieuvi!.5842"
#   }

#   user_crud = BaseCRUB(database_url, database_name, collection_name)

#   # register_result = await user_crud.save(data)
#   # print(f"Inserted document with ID: {register_result}")

#   # register_result = await user_crud.save({
#   #   "fullname": "huyentran",
#   #   "email": "htran43044@gmail.com",
#   #   "password": "htranxinhdeptuyetvoiqua43044<3"
#   # })
#   # print(f"Inserted document with ID: {register_result}")

#   # get_by_email_result = await user_crud.get_by_email("caodinhtrieuvi2004@gmail.com")
#   # print("Get a email: ", get_by_email_result)

  # get_by_password_result = await user_crud.get_by_password("htranxinhdeptuyetvoiqua43044<3")
  # print("Get a password: ", get_by_password_result)


#   # update_by_email_result = await user_crud.update_by_email("caodinhtrieuvi2004@gmail.com", "trieuvi5842@gmail.com")
#   # print("Update status: ", update_by_email_result)

  # delete_by_email_result = await user_crud.delete_by_email("trieuvi5842@gmail.com")
  # print("Delete status: ", delete_by_email_result)

  # get_all_emails_result = await user_crud.get_all_emails()
  # print("Get all emails: ", get_all_emails_result)


# asyncio.run(main())
    