import sys
sys.path.append("./")
import numpy as np
from Xclient.client import ModelClient

sample = np.array(
    ['你从哪里来，要到哪里去'.encode("utf-8")], dtype=np.object_
)

with ModelClient("grpc://10.88.36.58:8201", "bge_large_zh") as client:
    print(client.model_config)
    res = client.infer_sample('1')
    print(res)
