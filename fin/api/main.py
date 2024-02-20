from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import middleware
from fin.resolvers import transactions as rt
from fin.resolvers import labels as rl
import logging
from fastapi.staticfiles import StaticFiles
from models import NewTransactionDTO, RemoveTransactionDTO, NewLabelDTO
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.middleware("http")(middleware.log_time)
app.middleware("http")(middleware.load_user)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("layout.html", {"request": request})


@app.get("/transactions")
async def transactions(request: Request, name: str = None):
    transactions = rt.resolve_transactions(request.state.db, request.state.user)

    transaction_stats = rt.compute_transaction_stats(transactions)

    return templates.TemplateResponse(
        "transactions.html",
        {
            "request": request,
            "transactions": transactions,
            "transaction_stats": transaction_stats,
        },
    )


@app.post("/income")
async def add_income(request: Request, data: NewTransactionDTO):
    new_income = rt.resolve_add_income(
        request.state.db,
        request.state.user,
        data.amount,
        data.currency,
        data.name,
        data.description,
        data.labels,
    )

    response = templates.TemplateResponse(
        "transactions.html", {"request": request, "transactions": [new_income]}
    )

    return response


@app.post("/expense")
async def add_expense(request: Request, data: NewTransactionDTO):
    new_expense = rt.resolve_add_expense(
        request.state.db,
        request.state.user,
        data.amount,
        data.currency,
        data.name,
        data.description,
        data.labels,
    )

    response = templates.TemplateResponse(
        "transactions.html", {"request": request, "transactions": [new_expense]}
    )

    return response


@app.delete("/transaction")
async def delete_transaction(request: Request, data: RemoveTransactionDTO):
    rt.resolve_delete_transaction(request.state.db, request.state.user, data.id)


@app.post("/label")
async def add_label(request: Request, data: NewLabelDTO):
    label = rl.resolve_add_label(
        request.state.db, request.state.user, data.name, data.description
    )

    response = templates.TemplateResponse(
        "labels.html", {"request": request, "labels": [label]}
    )

    additional_headers = {
        "hx-location": json.dumps({"path": "/labels", "target": "#user-labels"})
    }

    response.headers.update(additional_headers)

    return response


@app.get("/labels")
async def labels(request: Request):
    labels = rl.resolve_labels(request.state.db, request.state.user)

    return templates.TemplateResponse(
        "labels.html", {"request": request, "labels": labels}
    )
