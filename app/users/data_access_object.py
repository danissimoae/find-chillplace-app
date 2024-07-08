from app.data_access_object.base import Base_Data_Access_Object
from app.users.models import Users

class Users_Data_Access_Object(Base_Data_Access_Object):
    model = Users