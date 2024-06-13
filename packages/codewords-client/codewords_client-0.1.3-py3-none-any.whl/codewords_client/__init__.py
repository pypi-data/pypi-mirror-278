import asyncio
import json
import os

import requests
import websockets

# add ../ to sys.path
from codewords_core.io_metadata import InputOutputMetadata
from codewords_core.file_type_utils import download_files_and_update_variables, upload_files_and_update_variables

WS_URL = os.getenv('CWR_WS_URL', "wss://d21x5wziv7.execute-api.eu-west-2.amazonaws.com/prod/")
HTTPS_URL = os.getenv('CWR_HTTPS_URL', "https://na9ywpljw9.execute-api.eu-west-2.amazonaws.com/prod/runtime")


def cw_function(
    *,
    function_id: str,
    version: str,
    auth_data: dict | None = None,
    runner_id: str,
    sync: bool = True,
    **init_kwargs
) -> 'CWFunction':
    if auth_data is None:
        # get CODEWORDS_API_KEY from the environment
        auth_data = {
            "type": "api_key",
            "data": os.getenv("CODEWORDS_API_KEY")
        }
        if auth_data['data'] is None:
            raise ValueError("auth_data or CODEWORDS_API_KEY must be provided")

    resp = requests.post(
        HTTPS_URL,
        json={
            "action": "get_info",
            "function_id": function_id,
            "version": version,
            "auth_data": auth_data,
            "runner_id": runner_id,
        },
    )
    resp.raise_for_status()
    definition_dict = resp.json()

    inputs_metadata = [InputOutputMetadata.parse_obj(input_data) for input_data in definition_dict['inputs']]
    outputs_metadata = [InputOutputMetadata.parse_obj(output_data) for output_data in definition_dict['outputs']]
    function_class = SyncCodewordsFunction if sync else AsyncCodewordsFunction

    return function_class(
        definition_dict,
        inputs_metadata,
        outputs_metadata,
        auth_data=auth_data,
        runner_id=runner_id,
        **init_kwargs
    )


class CWFunction():
    def __init__(
        self,
        definition_dict,
        inputs_metadata,
        outputs_metadata,
        *,
        working_directory='',
        auth_data: dict,
        runner_id: str,
        verbose=False,
    ):
        self.definition_dict = definition_dict
        self.inputs_metadata = inputs_metadata
        self.outputs_metadata = outputs_metadata
        self.working_directory = working_directory
        self.auth_data = auth_data
        self.runner_id = runner_id
        self._print = print if verbose else lambda *args, **kwargs: None

    async def run(self, inputs: dict):
        # find all the file type fields and upload them
        inputs = await upload_files_and_update_variables(
            variables=inputs,
            variables_metadata=self.inputs_metadata,
            working_directory=self.working_directory,
        )

        # call the lambda at WS_URL with an event
        event = {
            'action': 'run',
            'function_id': self.definition_dict['function_id'],
            'version': self.definition_dict['version'],
            'inputs': inputs,
            'runner_id': self.runner_id,
            'auth_data': self.auth_data,
        }
        async with websockets.connect(WS_URL) as ws:
            self._print(f"sending event to runtime: {event}")
            await ws.send(json.dumps(event))

            # TODO - handle intermediate messages
            response = await ws.recv()
            response = json.loads(response)

        if not response['type'] == 'run_complete':
            raise ValueError(f"run didnt complete successfully: {response}")

        outputs = response['outputs']
        # download any files that were uploaded
        outputs = await download_files_and_update_variables(
            variables=outputs,
            variables_metadata=self.outputs_metadata,
            working_directory=self.working_directory,
        )

        return outputs, response['run_info']

    async def call_async(self, **inputs):
        outputs, run_info = await self.run(inputs)
        # if there's an error throw that
        if len(run_info['error_messages']) > 0:
            raise Exception(f"Run failed with error messages: {run_info['error_messages']}")

        return outputs
    
    def call_sync(self, **inputs):
        return asyncio.run(self.call_async(**inputs))


class SyncCodewordsFunction(CWFunction):
    def __call__(self, **inputs):
        return self.call_sync(**inputs)


class AsyncCodewordsFunction(CWFunction):
    async def __call__(self, **inputs):
        return self.call_async(**inputs)