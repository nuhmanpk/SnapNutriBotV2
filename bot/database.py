import motor.motor_asyncio
from .vars import DATABASE_URL, DATABASE_NAME


class Database:
    def __init__(self, uri=DATABASE_URL, database_name=DATABASE_NAME):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users_col = self.db.users
        self.meals_col = self.db.meals
        self.cache = {}
    
    def new_user(self, id):
        return {"id": id}
    
    async def add_user(self, id):
        user = self.new_user(id)
        await self.users_col.insert_one(user)
    
    async def get_user(self, id):
        user = self.cache.get(id)
        if user is not None:
            return user
        
        user = await self.users_col.find_one({"id": int(id)})
        self.cache[id] = user
        return user
    
    async def update_user(self, id, update_data):
        await self.users_col.update_one({"id": int(id)}, {"$set": update_data})
        self.cache.pop(id, None)
    
    async def is_user_exist(self, id):
        user = await self.users_col.find_one({'id': int(id)})
        return True if user else False
    
    async def total_users_count(self):
        count = await self.users_col.count_documents({})
        return count
    
    async def get_all_users(self):
        all_users = self.users_col.find({})
        return all_users
    
    async def delete_user(self, user_id):
        await self.users_col.delete_many({'id': int(user_id)})

    async def add_meal(self, user_id, meal_data):
        meal_entry = {"user_id": user_id, **meal_data}
        await self.meals_col.insert_one(meal_entry)
    
    async def get_meals_by_user(self, user_id):
        meals = self.meals_col.find({"user_id": user_id})
        return meals


db = Database()
