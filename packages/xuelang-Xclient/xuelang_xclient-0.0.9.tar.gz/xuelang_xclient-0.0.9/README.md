# LLMOps-Xclient

Xclient客户端是一个用户友好的工具，旨在与Triton推理服务器毫不费力地通信。它为您管理技术细节，让您专注于您的数据和您的目标实现的结果。以下是它的帮助:

* 获取模型配置:客户机从服务器检索关于模型的详细信息，例如输入和输出数据张量的形状和名称。这一步对于正确准备数据和解释响应是至关重要的。这个功能被封装在ModelClient类中。

* 发送请求:利用模型信息，客户端通过将传递给infer_sample或infer_batch方法的参数映射到模型输入来生成推理请求。它将您的数据发送到Triton服务器，请求模型执行推理。参数可以作为位置参数或关键字参数传递(不允许混合它们)，其余的由客户端处理。

* 返回响应:然后将模型的响应返回给您。它将输入解码为numpy数组，并将模型输出映射到从infer_sample或infer_batch方法返回给您的字典元素。如果批处理维度是由客户端添加的，它还会删除该维度。

由于获取模型配置的额外步骤，此过程可能会引入一些延迟。但是，您可以通过为多个请求重用Xclient客户端，或者使用预加载的模型配置(如果有的话)对其进行设置，从而将其最小化。

Xclient包括五个专门的基础客户端，以满足不同的需求:

* ModelClient:用于简单请求-响应操作的直接的同步客户机。
* FuturesModelClient:一个多线程客户端，可以并行处理多个请求，加快操作速度。
* DecoupledModelClient:为解耦模型设计的同步客户机，它允许与Triton服务器进行灵活的交互模式。
* AsyncioModelClient:一个异步客户端，可以很好地与Python的asyncio一起工作，以实现高效的并发操作。
* AsyncioDecoupledModelClient:一个与异步兼容的客户端，专门用于异步处理解耦模型。

三个专门为MetaLM 服务的高级客户端：
* ChatMetaLM：专门用于大模型对话，可以流式返回。
* MetaLMEmbeddings：专门用于嵌入的客户端，支持稠密嵌入和稀疏嵌入。
* MetaLMRerank：专门用于重排的客户端。

Xclient客户机使用来自Triton的tritonclient包。它是Triton Inference Server的Python客户端库。它提供了使用HTTP或gRPC协议与服务器通信的低级API。Xclient客户端构建在tritonclient之上，并提供用于与服务器通信的高级API。并不是所有tritonclient的特性都可以在Xclient客户端中使用。如果需要对与服务器的通信进行更多的控制，可以直接使用tritonclient。


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