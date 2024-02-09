from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import middleware
from fin_backend.db.dynamodb.models.transactions import Income, Expense, Currency
from typing import Optional
from fin_backend.resolvers import transactions as rt
from pydantic import BaseModel
from enum import Enum
from decimal import Decimal
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("api")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.middleware("http")(middleware.log_time)
app.middleware("http")(middleware.load_user)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("layout.html", {"request": request})


@app.get("/transactions")
async def transactions(request: Request):
    transactions = rt.resolve_transactions(request.state.db, request.state.user)
    return templates.TemplateResponse("transactions.html", {"request": request, "transactions": transactions})


class Currency(Enum):
    ARS = "ARS"
    USD = "USD"


class NewTransactionDTO(BaseModel):
    name: str
    amount: Decimal
    description: Optional[str]
    currency: Currency


@app.post("/income")
async def add_income(request: Request, data: NewTransactionDTO):
    rt.resolve_add_income(
        request.state.db,
        request.state.user,
        data.amount,
        data.currency,
        data.name,
        data.description)


@app.post("/expense")
async def add_expense(request: Request, data: NewTransactionDTO):
    rt.resolve_add_expense(
        request.state.db,
        request.state.user,
        data.amount,
        data.currency,
        data.name,
        data.description)


class RemoveTransactionDTO(BaseModel):
    id: str
    
@app.delete("/transaction")
async def delete_transaction(request: Request, data: RemoveTransactionDTO):
    rt.resolve_delete_transaction(request.state.db, request.state.user, data.id)

