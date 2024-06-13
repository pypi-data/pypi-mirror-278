import yaml  
import os  
import sys
import importlib

def call_func( modle_name: str, func_name: str) -> callable:  
    try:  
        sys.path.append(os.getcwd())
        module = importlib.import_module(modle_name)  
        func = getattr(module, func_name) 
        if callable(func):  
            return func  
        else:  
            pass 
    except Exception as e:  
        pass


def start():
    yaml_file = sys.argv[1]  
    # 读取YAML文件  
    with open(yaml_file, 'r') as file:  
        apis = yaml.safe_load(file)  
    # 遍历apis列表  
    for api in apis.get("apis"): 
        handler = api['handler'].split('.')  # 分割handler字符串为模块和函数名  
        path = "/".join(api['handler'].split('.')[:-2]) 
        module_name = handler[-2]
        function_name = handler[-1]
        print(".".join(api['handler'].split(".")[:-1]), api['handler'].split(".")[-1])
        is_func = call_func(".".join(api['handler'].split(".")[:-1]), api['handler'].split(".")[-1])
        if is_func:
            print(f"函数已存在: {path} {module_name}:{function_name}")  
            continue
        if path:
            os.makedirs(path, exist_ok=True)
        # 创建Python模块文件（如果尚不存在）  
        module_path = f"{path}{'/' if path else ''}{module_name}.py"
        with open(module_path, 'a+') as file:  
            # 写入一个简单的函数存根  
            file.write(f"""
def {function_name}():
    # {api['name']}
    return {{"errorcode":"0000", "msg":"success"}}
            """)  

        # 注意：这里我们并没有实际执行或导入这个函数，只是创建了文件  
        print(f"Created/Updated file: {module_path} {module_name} {function_name}")  
    
if __name__ == "__main__":
    config_path = sys.argv[1]
    start()