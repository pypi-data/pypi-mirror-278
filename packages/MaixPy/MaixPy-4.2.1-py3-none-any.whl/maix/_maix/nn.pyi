"""
maix.nn module
"""
from __future__ import annotations
import maix._maix.err
import maix._maix.tensor
__all__ = ['LayerInfo', 'MUD', 'NN']
class LayerInfo:
    dtype: maix._maix.tensor.DType
    name: str
    shape: list[int]
    def __init__(self, name: str = '', dtype: maix._maix.tensor.DType = ..., shape: list[int] = []) -> None:
        ...
    def __str__(self) -> str:
        """
        To string
        """
    def to_str(self) -> str:
        """
        To string
        """
class MUD:
    items: dict[str, dict[str, str]]
    type: str
    def __init__(self, model_path: str = None) -> None:
        ...
    def load(self, model_path: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model_path: direction [in], model file path, model format can be MUD(model universal describe file) file.
        
        
        Returns: error code, if load success, return err::ERR_NONE
        """
class NN:
    def __init__(self, model_path: str = None) -> None:
        ...
    def extra_info(self) -> dict[str, str]:
        """
        Get model extra info define in MUD file
        
        Returns: extra info, dict type, key-value object, attention: key and value are all string type.
        """
    def forward(self, inputs: dict[str, maix._maix.tensor.Tensor]) -> dict[str, maix._maix.tensor.Tensor]:
        """
        forward run model, get output of model,
        this is specially for MaixPy, not efficient, but easy to use in MaixPy
        
        Args:
          - input: direction [in], input tensor
        
        
        Returns: output tensor
        """
    def inputs_info(self) -> list[LayerInfo]:
        """
        Get model input layer info
        
        Returns: input layer info
        """
    def load(self, model_path: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model_path: direction [in], model file path, model format can be MUD(model universal describe file) file.
        
        
        Returns: error code, if load success, return err::ERR_NONE
        """
    def loaded(self) -> bool:
        """
        Is model loaded
        
        Returns: true if model loaded, else false
        """
    def outputs_info(self) -> list[LayerInfo]:
        """
        Get model output layer info
        
        Returns: output layer info
        """
