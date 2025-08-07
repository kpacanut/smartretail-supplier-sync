import azure.functions as func
import logging
import json
import requests

app = func.FunctionApp()

@app.function_name(name="StockHandlerFunction")
@app.queue_trigger(arg_name="msg", queue_name="product-stock", connection="AzureWebJobsStorage")
def main(msg: func.QueueMessage):
    try:
        stock_event = msg.get_json()
        correlation_id = stock_event.get("correlationId", "N/A")

        logging.info(f"📥 Received stock event with correlationId: {correlation_id}")
        logging.info(f"🧾 Event Data: {stock_event}")

        response = requests.post(
            "http://localhost:5000/order",
            json=stock_event,
            headers={"X-Correlation-ID": correlation_id}
        )

        logging.info(f"📤 Sent to Supplier API — Response: {response.text}")

    except Exception as e:
        logging.error(f"❌ Error processing message: {e}")

