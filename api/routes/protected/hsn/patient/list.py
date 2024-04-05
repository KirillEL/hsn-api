import datetime
from datetime import date as tdate
from typing import Optional, List

from fastapi import Request, Depends, Query
from pydantic import BaseModel, Field, parse_obj_as

from core.hsn.patient.model import Patient, PatientFlat, PatientResponse
from core.hsn.patient.queries.own import hsn_get_own_patients, GenderType
from .router import patient_router
from api.exceptions import ExceptionResponseSchema


class Filter(BaseModel):
    full_name: Optional[list[str]] = None
    gender: Optional[list[str]] = None


class SortParams(BaseModel):
    columnKey: Optional[str] = None
    order: Optional[str] = None


class GetOwnPatientsQueryParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    # Assuming full_name and gender are meant to be lists based on your alias notation
    full_name: Optional[List[str]] = None
    gender: Optional[List[str]] = None
    columnKey: Optional[str] = None
    order: Optional[str] = None


class GetOwnPatientResponse(BaseModel):
    data: list[PatientResponse]
    total: int


@patient_router.get(
    '',
    response_model=GetOwnPatientResponse,
    responses={'400': {"model": ExceptionResponseSchema}},
    summary='Получить своих пациентов'
)
async def get_own_patients(
        request: Request,
        limit: Optional[int] = Query(None),
        offset: Optional[int] = Query(None),
        full_name: Optional[List[str]] = Query(None, alias="filters[full_name][0]"),
        gender: Optional[List[str]] = Query(None, alias="filters[gender][0]"),
        columnKey: Optional[str] = Query(None, alias="sortParams[columnKey]"),
        order: Optional[str] = Query(None, alias="sortParams[order]")
):
    params = GetOwnPatientsQueryParams(
        limit=limit,
        offset=offset,
        full_name=full_name,
        gender=gender,
        columnKey=columnKey,
        order=order
    )
    return await hsn_get_own_patients(
        request.user.id,
        limit=params.limit,
        offset=params.offset,
        full_name=params.full_name,
        gender=params.gender,
        columnKey=params.columnKey,
        order=params.order
    )
