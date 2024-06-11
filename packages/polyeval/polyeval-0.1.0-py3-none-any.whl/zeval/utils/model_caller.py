# zeval/zeval/utils/model_caller.py
import litellm
from litellm import completion
from unionllm import UnionLLM

class ModelCaller:
    def __init__(self, config):
        self.config = config

    def call(self, **params):
        # 更新或合并额外参数，避免重复
        effective_params = {**params}
                
        try:
            self.client = UnionLLM(**params)
            return self.client.completion(**effective_params)
        except:
            try:
                # 去掉不需要的参数provider
                effective_params.pop('provider', None)
                return litellm.completion(**effective_params)
            except Exception as e:
                print("Exception: ", e)
                return str(e)