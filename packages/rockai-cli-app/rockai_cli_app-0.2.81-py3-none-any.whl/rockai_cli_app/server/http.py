from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import signal
from rockai_cli_app.predictor import BasePredictor
import uvicorn
from rockai_cli_app.parser.config_util import parse_config_file, get_predictor_class_name,get_predictor_path
from rockai_cli_app.server.utils import (
    load_class_from_file,
    get_input_type,
    get_output_type,
)
import rockai_cli_app.data_class
import typing
import logging
from rockai_cli_app.data_class import InferenceResponse
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Set the initial logging level to INFO

# Create a logger
logger = logging.getLogger(__name__)


class MyFastAPI(FastAPI):
    pass

def create_app(path:Path) -> MyFastAPI:

    app: MyFastAPI = MyFastAPI()

    pred: BasePredictor = load_class_from_file(
        Path.cwd() / get_predictor_path(parse_config_file(path / "rock.yaml")),
        get_predictor_class_name(parse_config_file(path / "rock.yaml")),
        BasePredictor,
    )

    
    input_type = get_input_type(pred)
    output_type = get_output_type(pred)

    class InferenceRequest(
        rockai_cli_app.data_class.InferenceRequest.get_pydantic_model(
            input_type=input_type
        )
    ):
        pass
    
    InfRes = InferenceResponse.get_pydantic_model(input_type=input_type, output_type=output_type)

    @app.on_event("startup")
    async def start_up_event():
        """
        Run the setup function of the predictor and load the model
        """
        logger.debug("setup start...")
        pred.setup()
        logger.debug("setup finish...")


    @app.post("/shutdown")
    async def shutdown():
        """
        Shutdown the server.
        """
        pid = os.getpid()
        os.kill(pid, signal.SIGINT)
        return JSONResponse(content={"message": "Shutting down"}, status_code=200)


    @app.get("/")
    async def root():
        """
        Hello World!, when you see this message, it means the server is up and running.
        """
        return JSONResponse(content={"docs_url": "/docs","Hello":"World!"}, status_code=200)


    
    @app.post(
        "/predictions",
        response_model=InfRes,
        response_model_exclude_unset=True,
    )
    async def predict(
        request_body: InferenceRequest = Body(default=None),
    ) -> typing.Any:
        """
        Running the prediction.
        """
        logger.debug("prediction start...")
        if request_body is None or request_body.input is None:
            request_body = InferenceRequest(input={})
        request_body = request_body.dict()
        result = pred.predict(**request_body['input'])
        return JSONResponse(content=jsonable_encoder(InfRes(output=result)))


    return app


def start_server(port):
    app = create_app(path=Path.cwd())
    uvicorn.run(app, host="0.0.0.0", port=port)
