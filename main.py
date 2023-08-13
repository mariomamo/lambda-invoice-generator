import base64
import json
import logging

from flowables.Invoice import Invoice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# lambda
pdf_path = "/tmp/"
# local
# pdf_path = ""


def lambda_handler(event, context):
    logger.info(f"Event: {event}")

    if 'body' not in event:
        logger.error("Body is missing")
        return return_400_error()

    request_body = json.loads(event['body'])
    if 'invoice' not in request_body:
        logger.error("Invoice infos are missing")
        return return_400_error()

    invoice = request_body['invoice']
    logger.info(f"Invoice: {invoice}")
    invoice = Invoice(output_path=get_pdf_path(), data=invoice)
    invoice.generate()

    return return_response()


def get_pdf_path():
    return f'{pdf_path}invoice.pdf'


def return_400_error():
    return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json"
        }
    }


def return_response():
    try:
        with open(get_pdf_path(), "rb") as file:
            bytes = file.read()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/pdf"
            },
            "body": base64.b64encode(bytes),
            "isBase64Encoded": True
        }
    except Exception as ex:
        logger.info(ex)
        return {
            "statusCode": 500
        }

    # return {
    #     "statusCode": 308,
    #     "headers": {
    #         "location": "https://mariooffertucci.altervista.org/PhotoSharing_1.0.4.jar"
    #     }
    # }


if __name__ == '__main__':
    data = {
        "invoice_number": "xxx",
        "p_iva_customer": " xxx",
        "cf_customer": "xxx",
        "path_logo": "https://upload.wikimedia.org/wikipedia/commons/8/85/Logo-Test.png",
        "items_list": [
            {
                "quantity": 0,
                "description": "Generatore fatture",
                "unityPrice": 150
            }
        ]
    }
    r = lambda_handler({"body": json.dumps({"invoice": data})}, {})
    print(r)
