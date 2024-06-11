import logging
from flask import Flask, request, json, Response
from paste.translogger import TransLogger
import os
from tempfile import TemporaryDirectory
import autotwin_gmglib as gmg
from werkzeug.exceptions import NotImplemented, HTTPException

LOG_FORMAT = "%(asctime)s %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
MSG_FORMAT = (
    "%(REMOTE_ADDR)s - %(REMOTE_USER)s "
    '"%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" '
    '%(status)s %(bytes)s "%(HTTP_REFERER)s" "%(HTTP_USER_AGENT)s"'
)

logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)
app = Flask("proc-mining-serv")
wsgi = TransLogger(app, format=MSG_FORMAT, setup_console_handler=False)

NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
NEO4J_DATABASE = os.environ["NEO4J_DATABASE"]


@app.post("/graph-model")
def create_graph_model() -> Response:
    """Create a graph model in the SKG.

    Returns:
        Response with model ID.
    """
    request_data = request.get_data()
    request_data = json.loads(request_data)
    config = gmg.load_config()
    config = gmg._deep_update(request_data, config)
    work_directory = TemporaryDirectory()
    config["work_path"] = work_directory.name
    config["neo4j"]["uri"] = NEO4J_URI
    config["neo4j"]["username"] = NEO4J_USERNAME
    config["neo4j"]["password"] = NEO4J_PASSWORD
    config["neo4j"]["database"] = NEO4J_DATABASE
    gmg.import_log(config)
    log = gmg.load_log(config)
    model = gmg.generate_model(log, config)
    model_id = gmg.export_model(model, config)
    response_data = json.dumps({"model_id": model_id})
    return Response(response_data, status=201, mimetype="application/json")


@app.post("/petri-net")
def create_petri_net() -> Response:
    """Create a Petri net in the SKG.

    Returns:
        Response with model ID.
    """
    raise NotImplemented()  # noqa: F901


@app.post("/automaton")
def create_automaton() -> Response:
    """Create an automaton in the SKG.

    Returns:
        Response with model ID.
    """
    raise NotImplemented()  # noqa: F901


@app.errorhandler(HTTPException)
def transform_exception(error) -> Response:
    """Transform an HTTP exception into the JSON format.

    Returns:
        Response with error information.
    """
    response = error.get_response()
    response.data = json.dumps(
        {
            "code": error.code,
            "name": error.name,
            "description": error.description,
        }
    )
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    import waitress

    waitress.serve(wsgi, host="localhost")
