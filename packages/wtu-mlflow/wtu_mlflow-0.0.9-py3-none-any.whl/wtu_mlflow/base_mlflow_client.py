import logging
import os
import pika
import onnx

from abc import ABCMeta, abstractmethod
from mlflow.models.signature import ModelSignature
from mlflow.models.utils import ModelInputExample
from typing import Optional
from .schema import Schema

"""
ModelInputExample
    mlflow 1.x 버전에서는 from mlflow.models.utils import ModelInputExample
    mlflow 2.x 버전에서는 from mlflow.models.signature import ModelInputExample
"""

logger = logging.getLogger(__name__)


class BaseMLflowClient(metaclass=ABCMeta):
    def __init__(self):
        self._ONNX_TO_TRITON_DTYPE = {
            onnx.TensorProto.BOOL: "TYPE_BOOL",
            onnx.TensorProto.UINT8: "TYPE_UINT8",
            onnx.TensorProto.UINT16: "TYPE_UINT16",
            onnx.TensorProto.UINT32: "TYPE_UINT32",
            onnx.TensorProto.UINT64: "TYPE_UINT64",
            onnx.TensorProto.INT8: "TYPE_INT8",
            onnx.TensorProto.INT16: "TYPE_INT16",
            onnx.TensorProto.INT32: "TYPE_INT32",
            onnx.TensorProto.INT64: "TYPE_INT64",
            onnx.TensorProto.FLOAT16: "TYPE_FP16",
            onnx.TensorProto.FLOAT: "TYPE_FP32",
            onnx.TensorProto.DOUBLE: "TYPE_FP64",
            onnx.TensorProto.STRING: "TYPE_STRING",
            # Brain floating point (bfloat16) is not directly supported in ONNX, you might need to handle it separately
            # "TYPE_BF16": <corresponding ONNX type if available or a custom handler>
        }
        self._uploadModelExchange = os.environ["RABBIT_MODEL_UPLOAD_TOPIC"]

        self._connection = pika.BlockingConnection(
            pika.URLParameters(os.environ["RABBIT_ENDPOINT_URL"])
        )
        self._channel = self._connection.channel()

    def _get_triton_compatible_type(self, tensor_type):
        return self._ONNX_TO_TRITON_DTYPE.get(tensor_type.elem_type, "UNKNOWN")

    @abstractmethod
    def upload(
        self,
        model,
        input_example: Optional[Schema] = None,
        output_example: Optional[Schema] = None,
    ):
        pass

        """
        _log_tensor:
        onnx.load 로 로드된 모델을 통해 input tensor와 output tensor의 정보를 출력합니다.
        """

    @abstractmethod
    def _log_tensor(self, model):
        pass

    @abstractmethod
    def _log_model(
        self,
        model,
        model_name: str,
        signature: ModelSignature = None,
        input_example: ModelInputExample = None,
    ) -> str:
        pass
