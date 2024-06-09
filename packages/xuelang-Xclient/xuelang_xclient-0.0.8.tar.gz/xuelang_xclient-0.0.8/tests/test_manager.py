import sys
sys.path.append("./")
from Xclient.manager import ModelManager

a = ModelManager()
print(a.get_model_repository_index("grpc://10.88.36.58:8201"))
print(a.is_model_ready(("grpc://10.88.36.58:8201",'equation_search')))
# a.load_model(("grpc://10.88.36.57:8201",'repeat'))
# print(a.get_model_config(("grpc://10.88.36.58:8201",'bge_large_zh')))