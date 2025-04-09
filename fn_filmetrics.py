import azure.functions as func
import logging
import pandas as pd
from io import StringIO
from utils import parse_csv

bp = func.Blueprint()

@bp.route(route="filmetrics", methods=['POST'])
def filmetrics(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a filmetrics request.")

    if not req.files:
        return func.HttpResponse("No file uploaded", status_code=400)

    for input_file in req.files.values():
        try:
            filename = input_file.filename
            contents = input_file.stream.read()
            logging.info(f"Received file: {filename}")

            df = parse_csv(contents, skip_rows=8)
            selected_columns = df[[col for col in df.columns if 'L1 d' in col  or 'L1 n' in col]]

            output = StringIO()
            selected_columns.to_json(output, index=False)
            output.seek(0)  
            
            return func.HttpResponse(
                output.getvalue(),
                status_code=200,
                mimetype="application/json",
                headers={"Content-Disposition": f"attachment; filename=processed_{filename}"}
            )

        except ValueError as e:
            logging.error(f"CSV Processing Error: {str(e)}")
            return func.HttpResponse(f"CSV Processing Error: {str(e)}", status_code=400)
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")
            return func.HttpResponse(f"Unexpected Error: {str(e)}", status_code=500)

    return func.HttpResponse("Unexpected error", status_code=500)
