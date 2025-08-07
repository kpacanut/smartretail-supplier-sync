# SmartRetail Supplier Sync - Milestone 3

**Project:** SmartRetail Supplier Sync: Event-Driven Inventory Coordination with Docker and Azure Serverless  
**Author:** Kathleen Pacanut  
**Date:** August 07, 2025  

---

## Objective

This milestone challenges students to extend the SmartRetail hybrid architecture with a supplier coordination workflow , implemented using event-driven design principles.
Students will design and build a system where product stock events emitted by the backend are consumed asynchronously by an Azure Function and routed to a simulated Supplier API microservice, 
also running as a Docker container. Logging and correlation IDs will be used to trace the full message flow.

---

## Architecture Overview

```
Backend (Python) → Azure Queue → Azure Function → Supplier API (Docker)
```

- **Backend Service:** Emits a product stock event to Azure Queue
- **Azure Function (Queue Trigger):** Subscribes to the queue, logs and routes the message
- **Supplier API:** Receives the order and logs the request using correlationId

## Message Format

Sample product event:
```json
{
  "product": "Wireless Mouse",
  "quantity": 2,
  "correlationId": "abc123-xyz789"
}
```

- `product`: Name of product
- `quantity`: Stock count
- `correlationId`: Used for traceability

---

## How to Deploy & Test

### Backend Emitter

```bash
cd backend
python emit_event.py
```

### Azure Function (Local)

```bash
cd azure-function
func start
```

### Supplier API

```bash
cd supplier-api
docker build -t supplier-api .
docker run -p 5000:5000 supplier-api
```

---

## Logs (Traceability via correlationId)

### Backend log

```
[INFO] Event emitted to queue with correlationId: abc123-xyz789
```

### Azure Function log

```
M-1: Received stock event with correlationId: abc123-xyz789
M-2: Event Data: { product: "Wireless Mouse", quantity: 2 }
M-3: Sent to Supplier API | Response: 200 - Order confirmed
```

### Supplier API log

```
[INFO] ✅ Order received: Wireless Mouse (Qty: 2) | correlationId: abc123-xyz789
```

---

## 🧪 Notes

- Function was tested locally due to Azure permission restrictions.
- Traceability is implemented across all logs via correlationId.
- Dockerized Supplier API simulates external supplier response.

---
