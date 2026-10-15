
import azure.functions as func
import uuid
import json
import logging
import os

from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError
from azure.identity import DefaultAzureCredential

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Authenticate with Microsoft Entra ID.
# Locally, DefaultAzureCredential can use your Azure CLI login.
# In Azure, it can use the Function App's managed identity.
credential = DefaultAzureCredential()

cosmos_client = CosmosClient(
    url=os.environ["COSMOS_ENDPOINT"],
    credential=credential
)

database = cosmos_client.get_database_client(
    os.environ["COSMOS_DATABASE_NAME"]
)

container = database.get_container_client(
    os.environ["COSMOS_CONTAINER_NAME"]
)


@app.route(route="orders", methods=["GET", "POST"])
def create_order(req: func.HttpRequest) -> func.HttpResponse:

    if req.method == "GET":
        return func.HttpResponse(
            json.dumps({"Hello": "World!!"}),
            status_code=200,
            mimetype="application/json"
        )

    if req.method == "POST":
        try:
            body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Request body must be valid JSON"}),
                status_code=400,
                mimetype="application/json"
            )

        if not isinstance(body, dict):
            return func.HttpResponse(
                json.dumps({"error": "Request body must be a JSON object"}),
                status_code=400,
                mimetype="application/json"
            )

        product = body.get("product")
        amount = body.get("amount")
        client_id = body.get("clientId")

        if not isinstance(product, str) or not product.strip():
            return func.HttpResponse(
                json.dumps({"error": "product must be a non-empty string"}),
                status_code=400,
                mimetype="application/json"
            )

        # bool is a subclass of int in Python, so reject it explicitly.
        if type(amount) is not int or amount <= 0:
            return func.HttpResponse(
                json.dumps({"error": "amount must be a positive integer"}),
                status_code=400,
                mimetype="application/json"
            )

        if not isinstance(client_id, str) or not client_id.strip():
            return func.HttpResponse(
                json.dumps({"error": "clientId must be a non-empty string"}),
                status_code=400,
                mimetype="application/json"
            )

        order_id = str(uuid.uuid4())

        order = {
            "id": order_id,
            "orderId": order_id,
            "product": product.strip(),
            "amount": amount,
            "clientId": client_id.strip(),
            "status": "Processing",
            "test": "Successful"
        }

        try:
            # Persist the order in Cosmos DB.
            container.create_item(body=order)

            return func.HttpResponse(
                json.dumps(order),
                status_code=201,
                mimetype="application/json"
            )

        except CosmosHttpResponseError:
            logging.exception("Failed to save order to Cosmos DB")
            return func.HttpResponse(
                json.dumps({"error": "Failed to save order"}),
                status_code=500,
                mimetype="application/json"
            )

    return func.HttpResponse(
        "Method not supported",
        status_code=405
    )
