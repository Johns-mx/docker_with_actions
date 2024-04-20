from fastapi import status
from sqlalchemy.orm import Session, defer
from sqlalchemy import select, update, insert, delete
from config.functions import updating_user_data
from models.models import MembershipCreate, eMembershipStatus, ResponseModel, ePaymentMethod, eTypePlan, UserDataInternal, UserCreate, User, UserUpdate, UserUpdateInternal
from db.connection import SessionLocal, engine
from db.models import Membership, Plan, User


#region: User
async def query_insert_new_user(user: UserCreate) -> ResponseModel:
    try:
        with SessionLocal() as session, session.begin():
            try:
                new_user = User(username=user.username, password=user.password, email=user.email, full_name=user.full_name)
                session.add(new_user)
            except:
                session.rollback() #>> Revertir la transacción en caso de error.
                raise
            else:
                session.commit()
                session.refresh(new_user)
        return ResponseModel(status=status.HTTP_201_CREATED, error=False, message="Usuario creado exitosamente.", res=None)
    except:
        return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="Usuario no pudo ser registrado.", res=None)


async def query_get_all_users() -> ResponseModel:
    try:
        with SessionLocal() as session:
            all_users= session.query(User).options(
                defer(User.password)
            ).all()
        return ResponseModel(status=status.HTTP_201_CREATED, error=False, message="Todos los usuarios", res=all_users)
    except:
        return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="No se pudieron obtener los usuarios", res=None)


async def query_get_full_user(username: str, password: str) -> ResponseModel:
    try:
        with SessionLocal() as session:
            user_data = session.query(User).filter(User.username == username, User.password == password).options(defer(User.password)).first()
            if not user_data:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario encontrado.", res=user_data)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_get_user_by_id(user_id: int) -> ResponseModel:
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.user_id == user_id).with_entities(User.user_id, User.username, User.email, User.full_name).first()
            if not user:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
            full_name = UserDataInternal(*user)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario encontrado.", res=full_name)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_get_user_by_username(username: str) -> ResponseModel:
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.username == username).with_entities(User.user_id, User.username, User.email, User.full_name).first()
            if not user:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
            full_name = UserDataInternal(*user)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario encontrado.", res=full_name)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_authenticate_user(username: str, password: str) -> ResponseModel:
    try:
        with SessionLocal() as session:
            user_data = session.query(User).filter(User.username == username, User.password == password).with_entities(User.user_id, User.username, User.email, User.full_name).first()
            if not user_data:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
            full_user = UserDataInternal(*user_data)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario encontrado.", res=full_user)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_update_user(new_user_data: UserUpdate) -> ResponseModel:
    try:
        with SessionLocal() as session:
            try:
                user_data = session.query(User).filter(User.username == new_user_data.username, User.password == new_user_data.password).options(defer(User.password)).first()
                if not user_data:
                    return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
                
                #>> Se actualizan los datos de user_data con los nuevos datos de new_user_data.
                new_data = UserUpdateInternal(full_name=new_user_data.full_name, phone=new_user_data.phone, language=new_user_data.language,
                    country=new_user_data.country, address=new_user_data.address, membership=new_user_data.membership
                )
                user_data = await updating_user_data(user_data, new_data)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                session.refresh(user_data)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario actualizado.", res=None)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al actualizar el usuario.", res=None)
#endregion


#region: Membership
async def query_get_all_memberships() -> ResponseModel:
    try:
        with SessionLocal() as session:
            all_memberships = session.query(Membership).all()
        return ResponseModel(status=status.HTTP_201_CREATED, error=False, message="Todas las membresias.", res=all_memberships)
    except:
        return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="No se pudieron obtener las membresias.", res=None)


async def query_insert_new_membership(user_info: User) -> ResponseModel:
    try:
        with SessionLocal() as session:
            try:
                #membership_interface= MembershipCreate(user_id=user_info.user_id, plan_id=eTypePlan.PREMIUM.value, status=eMembershipStatus.ACTIVO.value, payment_method=ePaymentMethod.PAYPAL.value, billing_information=f"Suscrito al plan {eTypePlan.PREMIUM.name}.")
                new_membership = Membership(
                    user_id=user_info.user_id, plan_id=eTypePlan.PREMIUM.value, 
                    status=eMembershipStatus.ACTIVO.value, payment_method=ePaymentMethod.PAYPAL.value, 
                    billing_information=f"Suscrito al plan {eTypePlan.PREMIUM.name}."
                )
                session.add(new_membership)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                session.refresh(new_membership)
        return ResponseModel(status=status.HTTP_201_CREATED, error=False, message="Membresia creada exitosamente.", res=new_membership)
    except:
        return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="Membresia no pudo ser registrada.", res=None)
#endregion


#region: Plan
async def query_get_all_plans() -> ResponseModel:
    try:
        with SessionLocal() as session:
            all_plans = session.query(Plan).all()
        return ResponseModel(status=status.HTTP_201_CREATED, error=False, message="Todos los planes.", res=all_plans)
    except:
        return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="No se pudieron obtener los planes.", res=None)

#endregion