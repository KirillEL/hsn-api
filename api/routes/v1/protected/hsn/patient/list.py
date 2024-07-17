import datetime
from datetime import date as tdate
from typing import Optional, List

from fastapi import Request, Depends, Query
from pydantic import BaseModel, Field, parse_obj_as

from core.hsn.patient.schemas import Patient, PatientFlat, PatientResponse, PatientResponseWithoutFullName
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
    full_name: Optional[List[str]] = None
    gender: Optional[List[str]] = None
    location: Optional[List[str]] = None
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
        full_name: Optional[List[str]] = Query(None, alias='filters[full_name][0]'),
        gender: Optional[List[str]] = Query(None, alias="filters[gender][0]"),
        location: Optional[List[str]] = Query(None, alias="filters[location][0]"),
        columnKey: Optional[str] = Query(None, alias="sortParams[columnKey]"),
        order: Optional[str] = Query(None, alias="sortParams[order]")
):
    params = GetOwnPatientsQueryParams(
        limit=limit,
        offset=offset,
        gender=gender,
        full_name=full_name,
        location=location,
        columnKey=columnKey,
        order=order
    )
    return await hsn_get_own_patients(
        request.user.id,
        limit=params.limit,
        offset=params.offset,
        gender=params.gender,
        full_name=params.full_name,
        location=params.location,
        columnKey=params.columnKey,
        order=params.order
    )