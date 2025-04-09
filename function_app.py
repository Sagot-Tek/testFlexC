import azure.functions as func
import fn_filmetrics

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

app.register_functions(fn_filmetrics.bp)
