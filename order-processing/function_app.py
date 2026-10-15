import azure.functions as func
import uuid
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

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

        order = {
            "orderId": str(uuid.uuid4()),
            "product": product.strip(),
            "amount": amount,
            "clientId": client_id.strip(),
            "status": "Processing",
            "test": "Successful"
        }

        return func.HttpResponse(
            json.dumps(order),
            status_code=201,
            mimetype="application/json"
        )
    
    return func.HttpResponse("Method not suported", status_code=405)