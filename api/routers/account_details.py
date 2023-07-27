from fastapi import APIRouter, Depends, Response
from typing import Union, Optional
from authenticator import authenticator
from queries.account_details import (
    Error,
    AccountDetailPostIn,
    AccountDetailPutIn,
    AccountDetailOut,
    AccountDetailQueries,
    AccountDetailsOut,
)

router = APIRouter()


@router.get("/account", response_model=Union[AccountDetailsOut, Error])
def get_one_account(
    response: Response,
    query: AccountDetailQueries = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> Union[AccountDetailsOut, Error]:
    account = query.get_one(account_data.get("id"))
    if account is None:
        response.status_code = 404
        return {"message": "Account not found"}
    return account


# @router.post("/account_details", response_model=Union[AccountDetailOut, Error])
# def create_account_details(
#     account_details: AccountDetailPostIn,
#     query: AccountDetailQueries = Depends(),
# ) -> Union[AccountDetailOut, Error]:
#     return query.create(account_details)


@router.put(
    "/account_details",
    response_model=Union[AccountDetailOut, Error],
)
def update_account_details(
    account_details: AccountDetailPutIn,
    query: AccountDetailQueries = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> Union[AccountDetailOut, Error]:
    return query.update(account_data.get("id"), account_details)


@router.delete("/account_details/{account_id}", response_model=bool)
def delete_account_details(
    account_id: int,
    query: AccountDetailQueries = Depends(),
) -> bool:
    return query.delete(account_id)
