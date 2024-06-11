import numpy as np
from Xclient.client import ModelClient
from Xclient.llms import ChatMetaLM
from Xclient import AsyncioDecoupledModelClient

# async def main():
#     client = AsyncioDecoupledModelClient("grpc://10.88.36.58:8201", "Qwen2-0.5B-Instruct")
#     async for answer in client.infer_sample(np.array(["I'm Pickle Rick".encode('utf-8')])):
#         print(answer)
#     await client.close()

# # Run the code as a coroutine using asyncio.run()
# import asyncio
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

with ModelClient("grpc://10.88.36.58:8201", "Qwen2-0.5B-Instruct") as client:
    print(client.model_config)
    
llm = ChatMetaLM(server_url="10.88.36.58:8201", model_name="Qwen2-0.5B-Instruct",stop=['。'])
#result = llm.invoke("I'm Pickle Rick")
#print(result)
for token in llm.stream("介绍一下你自己"):
    print(token)