import os

import grpc
import numpy as np
import sys
sys.path.append("./")
from Xclient import InferenceClient
import time
TRITON_HOST = os.environ.get("TRITON_HOST", "10.88.36.57")


def get_client(protocol, port, model_name,model_version,stream):
    #print(f"Testing {protocol}", flush=True)
    return InferenceClient.create_with(model_name, f"{TRITON_HOST}:{port}",model_version=model_version, protocol=protocol,streaming=stream)

def test_with_input_name():
    client = get_client('http',8200, model_name="bge_large_zh",model_version='2',stream=False)
    #print(client.default_model_spec)
    # sample = np.random.rand(100, 100).astype(np.float32)
    sample = np.array(
        ['你从哪里来，要到哪里去'.encode("utf-8")], dtype=np.object_
    )
    sample = sample.reshape(1,1)
    result = client({client.default_model_spec.model_input[0].name: sample})
    print(result)
    # assert np.isclose(result, sample).all()

def test_with_repeat():
    client = get_client('grpc',8201, model_name="repeat",model_version='1',stream=True)
    print(client.default_model_spec)
    in_value = [4, 2, 0, 1]
    delay_value = [1, 2, 3, 4]
    wait_value = 5
    IN = np.array(in_value, dtype=np.int32)
    DELAY = np.array(delay_value, dtype=np.uint32)
    WAIT = np.array([wait_value], dtype=np.uint32)
    result = client({"IN": IN,"DELAY":DELAY,"WAIT":WAIT})
    for res in result:
        print(res)

    #time.sleep(10)
    # print(result)
    # for res in result:
    #     print(res)
#self.model_specs.
#def test_get_input_name():
# 
# def fun(t):
#     for i in range(t):
#         time.sleep(1)
#         yield i



if __name__ == "__main__":
    #get_client('http',8200,'internlm')
    #test_with_input_name()
    test_with_repeat()