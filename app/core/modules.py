from fastapi import status
from db.models import User
from models.models import ResponseModel, UserFullModel
from config.queries import query_get_user_by_username


class UsersManagement(object):
    """Users Management"""
    def __init__(self):
        self.username: str=""
    
    async def config_user_is_blocked(self, query_response: UserFullModel | User):
        if not query_response.block:
            #return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="Usuario bloqueado.", res=False)
            return False
        #return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario activo.", res=True)
        return True
    
    async def config_user_have_membership(self):
        pass


