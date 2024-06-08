"""Type hinting support for AI Edge Quantizer."""

from collections.abc import MutableMapping
import copy
import dataclasses
import enum
from typing import Any, Optional, Union

import numpy as np
from typing_extensions import TypeAlias


QSV: TypeAlias = MutableMapping[str, Any]


class TFLOperationName(str, enum.Enum):
  ALL = '*'
  FULLY_CONNECTED = 'FULLY_CONNECTED'
  BATCH_MATMUL = 'BATCH_MATMUL'
  DEPTHWISE_CONV_2D = 'DEPTHWISE_CONV_2D'
  CONV_2D = 'CONV_2D'
  TRANSPOSE_CONV = 'TRANSPOSE_CONV'
  AVERAGE_POOL_2D = 'AVERAGE_POOL_2D'
  RESHAPE = 'RESHAPE'
  CUSTOM_OP = 'CUSTOM_OP'
  EMBEDDING_LOOKUP = 'EMBEDDING_LOOKUP'
  SOFTMAX = 'SOFTMAX'


# Use same code number as MOJAX for compatibility
class QuantizeMode(enum.Enum):
  CALIBRATE = 2
  MATERIALIZE = 3


class OpExecutionMode(str, enum.Enum):
  """How to execute the op."""

  WEIGHT_ONLY = 'WEIGHT_ONLY'
  DRQ = 'DRQ'  # Dynamic range quantization
  SRQ = 'SRQ'  # Static range quantization


class TensorDataType(str, enum.Enum):
  INT = 'INT'
  FLOAT = 'FLOAT'


class QuantTransformation(enum.Enum):
  """Operations associated with quantization for a tensor."""

  # Do nothing: float_tensor -> float_tensor.
  NO_QUANTIZE = 0
  # Add a quantize op: float_tensor -> Quantize Op -> quantized_tensor.
  ADD_QUANTIZE = 1
  # Add a dequantize op: quantized_tensor -> Dequantize Op -> float_tensor.
  ADD_DEQUANTIZE = 2
  # Quantize the float tensor: float_tensor -> quantized_tensor.
  QUANTIZE_TENSOR = 3
  # create pattern for emulated subchannel quantization, only support fully
  # connected op.
  EMULATED_SUBCHANNEL = 4


@dataclasses.dataclass(frozen=True)
class UniformQuantParams:
  """Parameters for uniform quantization.

  Attributes:
    num_bits: Number of bits to quantize to (e.g. 8 for int8).
    quantized_dimension: The dimension to quantize.
    scale: The scale of the quantization.
    zero_point: The zero point of the quantization.
    symmetric: Whether the quantization is symmetric (force zero_point to be 0).
    quantized_data: The quantized data.
  """

  num_bits: int
  quantized_dimension: Optional[int]
  scale: np.ndarray
  zero_point: np.ndarray
  symmetric: bool = True
  quantized_data: Optional[np.ndarray] = None

  @classmethod
  def from_tfl_tensor_details(cls, tensor_detail) -> 'UniformQuantParams':
    """Creates UniformQuantParams from TFLite tensor details.

    Args:
      tensor_detail: The tensor details from TFLite.

    Returns:
      UniformQuantParams.
    """
    quant_params = tensor_detail['quantization_parameters']
    data_type = tensor_detail['dtype']
    if data_type == np.int8:
      num_bits = 8
    elif data_type == np.int16:
      num_bits = 16
    elif data_type == np.int32:
      num_bits = 32
    elif data_type == np.int64:
      num_bits = 64
    else:
      raise ValueError(f'Unsupported data type: {data_type}')
    symmetric = sum(abs(quant_params['zero_points'])) == 0
    return cls(
        quantized_dimension=quant_params['quantized_dimension'],
        num_bits=num_bits,
        scale=quant_params['scales'],
        zero_point=quant_params['zero_points'],
        symmetric=symmetric,
    )

  def __eq__(self, other):
    if other.__class__ is not self.__class__:
      return NotImplemented
    return (
        self.num_bits == other.num_bits
        and self.quantized_dimension == other.quantized_dimension
        and np.array_equal(self.scale, other.scale)
        and np.array_equal(self.zero_point, other.zero_point)
        and self.symmetric == other.symmetric
        and _compare_array_or_none(self.quantized_data, other.quantized_data)
    )


@dataclasses.dataclass(frozen=True)
class NonLinearQuantParams:
  """Parameters for nonlinear quantization.

  Currently only used for fp16 quantization.

  Attributes:
    num_bits: Number of bits to quantize to (e.g. 16 for fp16).
    quantized_data: The quantized data.
    data_type: The data type of the tensor.
  """

  num_bits: int
  quantized_data: Optional[np.ndarray]
  data_type: TensorDataType = TensorDataType.FLOAT

  def __eq__(self, other):
    if other.__class__ is not self.__class__:
      return NotImplemented
    return (
        self.num_bits == other.num_bits
        and self.data_type == other.data_type
        and _compare_array_or_none(self.quantized_data, other.quantized_data)
    )


@dataclasses.dataclass(frozen=True)
class OpToTensorParams:
  """Tensor params authored from an associated op.

  Attributes:
    subgraph_op_id: The position of the op in the subgraph.
    transformations: The transformations to be applied to the tensor.
    parameters: The quantization parameters for the tensor.
  """

  subgraph_op_id: int
  transformations: list[QuantTransformation]
  parameters: Union[None, UniformQuantParams, NonLinearQuantParams] = None


@dataclasses.dataclass
class TensorTransformationParams:
  """Transformation info for a tensor.

  Every tensor in .tflite has the following property:
   * Produced by one source op (producer), except constant tensor or model
   input.
   * Consumed by one or many destination ops (consumer), except model output.

  Because users configure quantization settings in Op level
  `OpQuantizationConfig`, each tensor will receive transformation parameters
   * from the source op
   * from the destination ops
  """

  tensor_name: str
  producer: Optional[OpToTensorParams] = None
  consumers: Optional[list[OpToTensorParams]] = None


@dataclasses.dataclass(frozen=True)
class TensorQuantizationConfig:
  """Quantization configuration for a tensor.

  Attributes:
    num_bits: Number of bits to quantize to (e.g. 8 for int8).
    symmetric: Whether to perform symmetric or asymmetric quantization. In the
      symmetric quantization mode, the zero point is always 0.
    channel_wise: Whether to perform channel_wise quantization.
    dtype: The data type of the tensor.
  """

  # Number of bits to quantize to (e.g. 8 for int8).
  num_bits: int
  # Whether to perform symmetric or asymmetric quantization. In the symmetric
  # quantization mode, the zero point is always 0.
  symmetric: bool = True
  # Whether to perform channel_wise quantization.
  channel_wise: bool = False
  dtype: TensorDataType = TensorDataType.INT

  def to_dict(self) -> dict[str, Any]:
    """Converts ActivationQuantizationConfig to dict."""
    return dataclasses.asdict(
        self,
        dict_factory=lambda x: {  # pylint: disable=g-long-lambda
            k: v
            for (k, v) in x
            # Skip None and empty dict values.
            if v is not None and not (isinstance(v, dict) and not v)
        },
    )

  @classmethod
  def from_dict(cls, params: dict[str, Any]) -> 'TensorQuantizationConfig':
    """Converts a given dict to TensorQuantizationConfig."""
    params_copy = copy.deepcopy(params)
    return cls(**params_copy)


@dataclasses.dataclass(frozen=True)
class OpQuantizationConfig:
  """Configuration class to control the quantization process behavior.

  Default as float activation and weights. The default execution mode is
  WEIGHT_ONLY.

  Attributes:
    activation_tensor_config: The quantization configuration for activation
      tensors in the op (i.e., runtime tensors).
    weight_tensor_config: The quantization configuration for weight tensor in
      the op.
    execution_mode: How to execute the op after quantization.
  """

  # Quant config for activation tensors in the op (i.e., runtime tensors).
  activation_tensor_config: Optional[TensorQuantizationConfig] = None

  # Quantization config for weight tensor in the op.
  # Bias tensor quantization is deduced from activation/weight config.
  # e.g., int8A X int8W => int32 bias.
  weight_tensor_config: TensorQuantizationConfig = TensorQuantizationConfig(
      dtype=TensorDataType.INT,
      num_bits=8,
  )

  # How to execute the op after quantization.
  execution_mode: OpExecutionMode = OpExecutionMode.WEIGHT_ONLY

  def __post_init__(self):
    if self.activation_tensor_config is None:
      return
    # Make sure the setting is valid.
    if (
        self.activation_tensor_config.dtype == TensorDataType.INT
        and self.weight_tensor_config.dtype == TensorDataType.FLOAT
    ):
      raise ValueError(
          'An op can not be set to have integer activation but float weights!'
      )
    if (
        self.activation_tensor_config.dtype == TensorDataType.INT
        and self.weight_tensor_config.dtype == TensorDataType.INT
        and self.execution_mode != OpExecutionMode.SRQ
    ):
      raise ValueError(
          'Op execution mode must be SRQ (static range quantization) if both'
          ' activation and weight tensors are quantized!'
      )

  def to_dict(self) -> dict[str, Any]:
    """Converts OpQuantizationConfig to dict."""
    return dataclasses.asdict(
        self,
        dict_factory=lambda x: {  # pylint: disable=g-long-lambda
            k: v
            for (k, v) in x
            # Skip None and empty dict values.
            if v is not None and not (isinstance(v, dict) and not v)
        },
    )

  @classmethod
  def from_dict(cls, params: dict[str, Any]) -> 'OpQuantizationConfig':
    """Converts a given dict to OpQuantizationConfig."""
    params_copy = copy.deepcopy(params)
    params_copy['weight_tensor_config'] = TensorQuantizationConfig.from_dict(
        params_copy['weight_tensor_config']
    )
    if 'activation_tensor_config' in params_copy:
      params_copy['activation_tensor_config'] = (
          TensorQuantizationConfig.from_dict(
              params_copy['activation_tensor_config']
          )
      )
    return cls(**params_copy)


@dataclasses.dataclass(frozen=True)
class GraphInfo:
  """Aggregates graph information needed to perform quantization for an op.

  Attributes:
    subgraph_tensors: A list of tensors in the subgraph.
    buffers: A list of buffers in the subgraph.
  """

  subgraph_tensors: list[Any]
  buffers: list[Any]


@dataclasses.dataclass(frozen=True)
class OpInfo:
  """Aggregates op information needed to perform quantization for an op.

  Attributes:
    op: The op to be quantized.
    op_name: The name of the op.
    subgraph_op_index: The position of the op in the subgraph.
    op_quant_config: The quantization configuration for the op.
  """

  op: Any
  op_name: TFLOperationName
  subgraph_op_index: int  # position of the op in the subgraph.
  op_quant_config: OpQuantizationConfig


# data classes used by model modifier.


# TODO(b/335530570): this needs to support more than one parameters
@dataclasses.dataclass
class TransformationInst:
  """Transformation instruction for a tensor.

  Attributes:
    transformation: The transformation to be applied to the tensor.
    tensor_id: The id of the tensor.
    producer: The id of the producer op.
    consumers: The ids of the consumer ops.
    parameters: The quantization parameters for the tensor.
  """

  transformation: QuantTransformation
  tensor_id: int
  producer: Optional[int]
  consumers: list[int]
  parameters: Union[None, UniformQuantParams, NonLinearQuantParams] = None


@dataclasses.dataclass
class TensorTransformationInsts:
  """Transformation instructions for a tensor.

  Attributes:
    tensor_name: The name of the tensor.
    subgraph_id: The id of the subgraph.
    instructions: The transformation instructions for the tensor.
  """

  tensor_name: str
  subgraph_id: int
  instructions: Optional[list[TransformationInst]]


@dataclasses.dataclass(frozen=True)
class TransformationInfo:
  """Transformation information for an op.

  Attributes:
    op_id: The id where op replacement/insertion begins.
    num_ops_added: The number of ops added during the transformation.
    output_tensor_id: The id of the output tensor.
  """

  op_id: int
  num_ops_added: int
  output_tensor_id: int


def _compare_array_or_none(
    obj1: Optional[np.ndarray], obj2: Optional[np.ndarray]
):
  """Compares two arrays or None.

  Args:
    obj1: The first object to compare.
    obj2: The second object to compare.

  Returns:
    True if both objects are None or both objects are equal.
  """
  if obj1 is None and obj2 is None:
    return True  # Both None, so they're equal
  elif obj1 is None or obj2 is None:
    return False  # Only one is None, so they're different
  else:
    return np.array_equal(obj1, obj2)
