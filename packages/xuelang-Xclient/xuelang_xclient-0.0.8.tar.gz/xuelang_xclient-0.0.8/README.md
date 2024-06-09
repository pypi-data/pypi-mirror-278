# LLMOps-Xclient

这是triton服务的客户端。

## 打包
```
python setup.py sdist bdist_wheel || true 
```
## 上传
```
twine check dist/*

twine upload dist/*
```

## 4种模式
```
import numpy as np

from Xclient.client import ModelClient,FuturesModelClient,DecoupledModelClient,AsyncioModelClient

sample = np.array(
    ['你从哪里来，要到哪里去'.encode("utf-8")], dtype=np.object_
)
sample2 = np.array([
    ['你从哪里来，要到哪里去'.encode("utf-8")],
    ['你从哪里来，要到哪里去.........'.encode("utf-8")]
], dtype=np.object_
)
```

### 同步模式
```
with ModelClient("grpc://10.88.36.58:8201", "bge_large_zh","2") as client:
    print(client.model_config)
    res = client.infer_sample(sample)
    print(res)
    res = client.infer_batch(sample2)
    print(res)
```

### 并发模式，不等待
```
with FuturesModelClient("grpc://10.88.36.58:8201", "bge_large_zh","2") as client:
    res = client.infer_sample(sample)
print(res.result())
```

### 异步模式
#async 暂时可以不用

### 解耦模式，流
```
in_value = [4, 2, 0, 1]
delay_value = [1, 2, 3, 4]
wait_value = 5
IN = np.array(in_value, dtype=np.int32)
DELAY = np.array(delay_value, dtype=np.uint32)
WAIT = np.array([wait_value], dtype=np.uint32)
with DecoupledModelClient("grpc://10.88.36.58:8201", "repeat","1") as client:
    res = client.infer_sample(IN,DELAY,WAIT)
for r in res:
    print(r)
```