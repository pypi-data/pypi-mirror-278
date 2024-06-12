import asyncio
import json
import logging
from typing import Dict, Any, Union
import ssl

import websockets
import certifi

from .model_config import ModelConfig
from .utils import load_json_buffer, begin_task_execution, split_dict_into_chunks

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
END_OF_STREAM = '<EOS>'
DEFAULT_RESPONSE = {"response": ""}
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


async def interact_with_websocket(uri: str, query_payloads: Dict[Union[str, int], Dict[str, Any]]):
    response_payloads = {qid: {"response": ""} for qid in query_payloads}
    payload_iterator = iter(query_payloads.items())
    tmp_qid, tmp_input_payload = next(payload_iterator, (None, None))
    retry = False
    ws_ready_for_closure = False
    error_ct = 0

    # WEBSOCKET LOOP: Indefinitely opens a new connection when a new one is closed in the SAME asyncio task.
    while not ws_ready_for_closure:
        async with websockets.connect(uri, ssl=SSL_CONTEXT) as ws:
            try:
                if ws_ready_for_closure or tmp_qid is None:
                    break
                # QUERY LOOP: While there are queries remaining to send to the server.
                while tmp_qid is not None:
                    response_payloads[tmp_qid]["success"] = 0
                    if not retry:
                        error_ct = 0
                    await ws.send(json.dumps(tmp_input_payload))
                    # QUERY CHUNK LOOP: While chunks are being received by the WebSocket Client.
                    while True:
                        # Wait for the duration of the WebSocket connection for ANY response
                        response = await ws.recv()
                        parsed_response = load_json_buffer(response)
                        # Parse response stream from WebSocket server based on every use case
                        if isinstance(parsed_response, dict):
                            # Intended use case: user receives JSON response.
                            if 'response' in parsed_response.keys():
                                cleaned = parsed_response["response"].replace(END_OF_STREAM, "")
                                response_payloads[tmp_qid]["response"] += cleaned
                                if 'metadata' in parsed_response.keys() or END_OF_STREAM in parsed_response['response']:
                                    response_payloads[tmp_qid]["metadata"] = parsed_response["metadata"]
                                    response_payloads[tmp_qid]["success"] = 1
                                    retry = False
                                    break
                            # Error: user denied access to the response for some reason.
                            else:
                                logging.log(logging.ERROR, f"Data error: query ID {tmp_qid}: {parsed_response}")
                                response_payloads[tmp_qid].update(parsed_response)
                                retry = False
                                break
                        # Intended use case: user receives TEXT response from websocket
                        # Data format is streamlined regardless of which response type the user selects.
                        else:
                            response_payloads[tmp_qid]["response"] += response.replace(END_OF_STREAM, "")
                            if END_OF_STREAM in response:
                                retry = False
                                response_payloads[tmp_qid]["success"] = 1
                                break
                    # END - QUERY CHUNK LOOP
                    if not retry:
                        logging.log(level=logging.INFO, msg=f"Query ID {tmp_qid} completed...")
                        tmp_qid, tmp_input_payload = next(payload_iterator, (None, None))
                # END - QUERY LOOP
                ws_ready_for_closure = True
            except websockets.ConnectionClosed:
                error_ct += 1
                logging.log(level=logging.INFO, msg=f"Error {error_ct}: WebSocket connection closed on query ID "
                                                    f"{tmp_qid}. Reopening...")
                retry = True if error_ct <= 2 else False
    # END - WEBSOCKET LOOP
    logging.log(logging.INFO, msg="WebSocket connection closed.")
    return response_payloads


@begin_task_execution
async def batch_query_llm_socket(model: ModelConfig, queries: Dict[Union[str, int], str],
                                 max_concurrent_tasks: int = 3) -> Dict[Union[str, int], Dict[str, Any]]:
    payloads = {}
    for qid, message in queries.items():
        payloads[qid] = model.compute_payload(message)
    batches = split_dict_into_chunks(payloads, max_concurrent_tasks)
    tasks = [interact_with_websocket(model.api_url, batch) for batch in batches]

    results = await asyncio.gather(*tasks)
    final_results = {}
    for result_dict in results:
        final_results.update(result_dict)
    return final_results


@begin_task_execution
async def query_llm_socket(model: ModelConfig, query: str) -> Dict[str, Any]:
    tmp_payload = model.compute_payload(query=query)
    result = await interact_with_websocket(model.api_url, {0: tmp_payload})
    return result[0]
