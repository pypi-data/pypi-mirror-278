
import json
import os
import sys

import requests
import websockets

# add ../ to sys.path
from codewords_core.io_metadata import InputOutputMetadata
from codewords_core.file_type_utils import download_files_and_update_variables, upload_files_and_update_variables

try:
    WS_URL = os.environ['CWR_WS_URL']
    HTTPS_URL = os.environ['CWR_HTTPS_URL']
except KeyError as e:
    print(f"Environment variable {e} not set")
    sys.exit(1)


def cw_function(
    function_id: str,
    version: str,
    auth_data: dict,
    runner_id: str,
    **init_kwargs
) -> 'CWFunction':
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
    return CWFunction(
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
        verbose=False
    ):
        self.definition_dict = definition_dict
        self.inputs_metadata = inputs_metadata
        self.outputs_metadata = outputs_metadata
        self.working_directory = working_directory
        self.auth_data = auth_data
        self.runner_id = runner_id
        self._print = print if verbose else lambda *args, **kwargs: None

    async def run(self, inputs: Dict[str, Any]):
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

    async def __call__(self, **inputs):
        outputs, run_info = await self.run(inputs)
        # if there's an error throw that
        if len(run_info['error_messages']) > 0:
            raise Exception(f"Run failed with error messages: {run_info['error_messages']}")

        return outputs

