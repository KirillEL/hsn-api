from typing import Optional

from fastapi import Request, Query
from pydantic import BaseModel

from core.hsn.patient.model import (
    DictPatientResponse,
)
from core.hsn.patient.queries.own import hsn_query_own_patients
from .router import patient_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException


class Filter(BaseModel):
    full_name: Optional[list[str]] = None
    gender: Optional[list[str]] = None


class SortParams(BaseModel):
    columnKey: Optional[str] = None
    order: Optional[str] = None


class GetOwnPatientsQueryParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    birth: Optional[str] = None
    columnKey: Optional[str] = None
    order: Optional[str] = None


@patient_router.get(
    "",
    response_model=DictPatientResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Получить своих пациентов",
)
async def get_own_patients_route(
    request: Request,
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    patronymic: Optional[str] = Query(None),
    birth: Optional[str] = Query(None),
    columnKey: Optional[str] = Query(None, alias="sortParams[columnKey]"),
    order: Optional[str] = Query(None, alias="sortParams[order]"),
):
    params = GetOwnPatientsQueryParams(
        limit=limit,
        offset=offset,
        name=name,
        last_name=last_name,
        patronymic=patronymic,
        birth=birth,
        columnKey=columnKey,
        order=order,
    )
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_query_own_patients(
        request,
        request.user.doctor.id,
        limit=params.limit,
        offset=params.offset,
        name=params.name,
        last_name=params.last_name,
        patronymic=params.patronymic,
        birth=params.birth,
        columnKey=params.columnKey,
        order=params.order,
    )
