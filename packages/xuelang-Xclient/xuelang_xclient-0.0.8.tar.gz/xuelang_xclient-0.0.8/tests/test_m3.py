from Xclient.client import ModelClient,FuturesModelClient,DecoupledModelClient,AsyncioModelClient
import numpy as np
import ast
import copy

#encode
# inputs = {
#     'action':['embed'],
#     # 'source_sentence': ['']
#     # 'source_sentence': ['江苏的小镇']
#     'source_sentence': ['江苏的小镇','BM25的定义是什么？']
# }

#compare
inputs = {
    # dense sparse colbert sparse+dense colbert+sparse+dense 五种方法任选
    'action':['compare','dense'],
    'source_sentence': ['江苏的小镇','BM25的定义是什么？','whats up bro?'],
    'sentences_to_compare': ['BM25就是BM25','获取该村周边地级市']
}

input0= np.array(
    [str(inputs).encode("utf8")],
    dtype=np.object_
)

with ModelClient("grpc://10.88.36.58:8201", "bge-m3", "1") as client:
# with ModelClient("grpc://10.88.36.58:8201", "bge_large_zh", "2") as client:
    print(client.model_config)
    res = client.infer_sample(input0)
    print(res)