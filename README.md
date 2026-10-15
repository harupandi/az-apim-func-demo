# Azure Serverless Orders Platform

This is a small cloud-native project built to learn how to design, deploy, secure, and manage an application using Azure services and modern DevOps practices.
The project consists of a React frontend hosted on Azure Static Web Apps, an API gateway managed by Azure API Management (APIM), a Python Azure Function that implements the API, and Azure Cosmos DB for NoSQL to persist order data. Microsoft Entra ID and managed identity provide passwordless authentication between the Function App and Cosmos DB.

## What each component does

- React + Vite: Provides a user interface for submitting orders. Its API URL is configured through a VITE_ environment variable.
- Azure Static Web Apps (SWA): Hosts the frontend and deploys it through a CI/CD workflow.
- Azure API Management: Exposes the API through a gateway endpoint and applies policies such as CORS and rate limiting.
- Azure Functions: Runs the backend using Python's v2 programming model. It exposes GET and POST endpoints at /api/orders.
- Azure Cosmos DB: Stores orders in the OrdersDb database, inside the orders container, using /clientId as the partition key.
- Microsoft Entra ID: Authenticates the Function App to Cosmos DB using a user-assigned managed identity in Azure and a developer identity during local development.

## How an order is processed

1. A user submits an order through the React frontend.
2. The browser sends an HTTPS request to APIM.
3. APIM evaluates its configured policies and forwards the request to the Function App.
4. The Function validates the JSON payload, including the product name, positive integer amount, and client ID.
5. The Function generates a UUID and creates an order document.
6. The Function authenticates to Cosmos DB through DefaultAzureCredential and writes the document using the Cosmos DB SDK.
7. The API returns the created order with HTTP 201 Created.

The current implementation also provides a simple GET endpoint that returns a test response.

## Security and configuration
The project separates frontend configuration from backend credentials:
- The frontend receives the public APIM URL through VITE_ORDERS_API_URL.
- The Function reads its Cosmos DB endpoint, database name, and container name from application settings.
- Cosmos DB access uses Entra ID and managed identity rather than a stored Cosmos DB connection string.
- APIM policies can restrict browser origins and request rates, but CORS is not authentication.

The Function's HTTP trigger is currently configured as ANONYMOUS, so authentication of callers is a separate security task from the Function's authentication to Cosmos DB.

## Roadmap
- [ ] Create a CI/CD workflow for the Function App
- [ ] Automate dependency installation, testing, and deployment using GitHub Actions. Keep environment-specific settings out of source code and consider federated identity for deployment authentication.
- [ ] Migrate infrastructure management to Terraform
- [ ] Strengthen API security
- [ ] Improve observability and reliability

*Overall goal: evolve a working serverless application into a reproducible, secure, and automated Azure platform managed through infrastructure as code and CI/CD.*