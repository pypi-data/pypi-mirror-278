from abc import ABC, abstractmethod
from typing import List, Union
import numpy as np
from vertexai.preview.language_models import TextEmbeddingModel, TextEmbeddingInput

class BaseTextEncoder(ABC):
    VALID_RETURN_TYPES = ['list', 'numpy', 'all']

    @abstractmethod
    def encode(self, text, return_type='list', task_type=None):
        pass
    
    def validate_return_type(self, return_type):
        if return_type not in BaseTextEncoder.VALID_RETURN_TYPES:
            raise ValueError('Invalid return type')
    
    def validate_task_type(self, task_type):
        pass
    
    def convert_to_return_type(self, results, return_type):
        if return_type == 'all':
            return results
        results = [result.values for result in results]
        if return_type == 'list':
            return results if len(results) > 1 else results[0]
        elif return_type == 'numpy':
            return np.array(results) if len(results) > 1 else np.array(results[0])


class VertexEncoder(BaseTextEncoder):
    """
    Text encoder using VertexAI's TextEmbeddingModel

    Args:
        model_name (str): Name of the model to use

    Example:
        encoder = VertexEncoder("textembedding-gecko-multilingual@001")
        text = 'Hello, World!'
        print(encoder.encode(text))

    Return:
        [0.1, 0.2, ..., 0.3]


    """
    def __init__(self, model_name):
        super().__init__()
        self.model = TextEmbeddingModel.from_pretrained(model_name)
        
    def encode(
            self, 
            text: Union[str, List[str]],
            return_type='list', 
            task_type='SEMANTIC_SIMILARITY'
        ):
        self.validate_return_type(return_type)
        if isinstance(text, str):
            text_input = [TextEmbeddingInput(text=text, task_type=task_type)]
        elif isinstance(text, list):
            text_input = [TextEmbeddingInput(text=t, task_type=task_type) for t in text]
        result = self.model.get_embeddings(text_input)
        return self.convert_to_return_type(result, return_type)


class EncodersFactory(BaseTextEncoder):
    
    MODEL_MAPPER = {
        "textembedding-gecko-multilingual@001": VertexEncoder,
        'textembedding-gecko@003': VertexEncoder,
        'text-embedding-004': VertexEncoder  
    }

    """
    Factory class to create text encoders based on the brand

    Args:
        sites_model_list (List[Dict[str, str]]): List of dictionaries containing brand and encoder-model

    Example:
        sites_model_list = [
            {"brand": "site1", "encoder-model": "textembedding-gecko-multilingual@001"},
            {"brand": "site2", "encoder-model": "textembedding-gecko@003"}
        ]
        factory = EncodersFactory(sites_model_list)
        text = 'Hello, World!'
        print(factory.encode(text, 'site1'))
    """
    def __init__(self, sites_model_list):
        self.models = {}
        for site in sites_model_list:
            self.models[site["brand"]] = EncodersFactory.MODEL_MAPPER.get(site["encoder-model"])(site["encoder-model"])

    def encode(
            self, 
            text: Union[str, List[str]],
            brand: str, 
            return_type='list', 
            task_type=None
        ):
        # model = self.models.get(site)
        if not self.models.get(brand):
            raise ValueError(f'Unsupported domain: {brand}')
        return self.models.get(brand).encode(text=text, return_type=return_type, task_type=task_type)

