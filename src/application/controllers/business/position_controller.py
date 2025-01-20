from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from domain.entities.business.position.position import PositionTable, PositionBase
from core.database.database import get_session
from core.services.user_service import user_service
import core.datasource.business_datasource as bd
import domain.helpers.responses as resp
from core.services.user_service import UserService

position_router = APIRouter(prefix="/business/position", tags=["position"])
user_service = UserService()

@position_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED
)
def create_position(
    position: PositionBase,
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return bd.create_position(position, session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@position_router.post(
    "/create/list",
    status_code=status.HTTP_201_CREATED
)
def create_positions(
    positions: List[PositionBase],
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        
        for position in positions:
            bd.create_position(position, session)
        return resp.created_response("Positions created successfully")
    except Exception as err:
        return resp.internal_server_error_response(err)

        
@position_router.get(
    "/all",
    status_code=status.HTTP_200_OK
)
def get_positions(session: Session = Depends(get_session)):
    return bd.get_positions(session)
        

@position_router.put(
    "/update/{id}",
    status_code=status.HTTP_202_ACCEPTED
)
def update_position(
    id: int,
    position: PositionBase,
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        return bd.update_position(id, position, session)
    except Exception as err:
        return resp.internal_server_error_response(err)