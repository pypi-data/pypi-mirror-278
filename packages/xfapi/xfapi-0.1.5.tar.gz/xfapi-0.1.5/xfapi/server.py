from fastapi import FastAPI, APIRouter ,Request
from fastapi.responses import JSONResponse
import uvicorn  
from .utils.load_yaml import YamlConfig  
import os  
import importlib  
import logging  

logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  
  
class HTTPServer:  
    def __init__(self, host="0.0.0.0", port=8000, config_path="api.yaml", auth_middleware=None):  
        self.host = host  
        self.port = port  
        self.app = FastAPI()  
        self.router = APIRouter()  
        self.config_path = config_path 
        self.auth_middleware = auth_middleware
  
    def call_func(self, modle_name: str, func_name: str) -> callable:  
        try:  
            module = importlib.import_module(modle_name)  
            func = getattr(module, func_name)  
            if callable(func):  
                return func  
            else:  
                raise ValueError(f"函数 {func_name} 在模块 {modle_name} 中不可调用")  
        except Exception as e:  
            raise ImportError(f"导入模块 {modle_name} 或获取函数 {func_name} 时出错: {e}")  
    
    def register_routes(self):  
        if not os.path.exists(self.config_path):  
            logger.error("api.yaml文件不存在，请先创建该文件")  
            return  
        try:  
            self.apis = YamlConfig(self.config_path).get_configs().get("apis")  
            if not self.apis:  
                logger.error("api.yaml文件格式错误，请检查")  
                return  
            # 注册中间件
            if self.auth_middleware:
                if callable(self.auth_middleware):  
                    self.app.middleware("http")(self.auth_middleware)
                else:
                    logger.error("auth_middleware 必须是一个可调用的函数")
            for api in self.apis:  
                logger.info(f"""注册路由: {api.get("path")} {api.get("method")} -> {api.get("handler")}""")
                modle_path = ".".join(api.get("handler").split(".")[:-1])  
                func_name = api.get("handler").split(".")[-1]  
                try:  
                    func = self.call_func(modle_path, func_name)  
                except Exception as e:  
                    logger.error(f"在模块 {modle_path} 中找不到或无法调用函数 {func_name}: {e}")  
                    continue  
                  
                method = api.get("method", "").lower()  
                path = api.get("path")  
                  
                if method == "get":  
                    self.router.add_api_route(path, func, methods=["GET"])  
                elif method == "post":  
                    self.router.add_api_route(path, func, methods=["POST"])  
                elif method == "put":  
                    self.router.add_api_route(path, func, methods=["PUT"])  
                elif method == "delete":  
                    self.router.add_api_route(path, func, methods=["DELETE"])  
                else:  
                    logger.warning(f"不支持的方法: {method}") 
            self.app.include_router(self.router) 
        except Exception as e:  
            logger.error(f"注册路由时出错: {e}")  
  
    def start(self):  
        self.register_routes()  
        uvicorn.run(self.app, host=self.host, port=self.port)  
  

