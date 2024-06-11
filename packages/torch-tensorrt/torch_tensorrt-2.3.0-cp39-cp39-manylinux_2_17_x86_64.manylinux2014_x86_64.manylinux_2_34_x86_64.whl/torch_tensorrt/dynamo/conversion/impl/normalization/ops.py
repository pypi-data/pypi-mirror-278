from typing import Any, List, Optional, Sequence, Tuple, Union, cast

import numpy as np
import tensorrt as trt
import torch
from torch.fx.node import Target
from torch_tensorrt.dynamo._SourceIR import SourceIR
from torch_tensorrt.dynamo.conversion import impl
from torch_tensorrt.dynamo.conversion._ConversionContext import ConversionContext
from torch_tensorrt.dynamo.conversion.converter_utils import (
    cast_trt_tensor,
    get_axes_for_reduce_op,
    get_positive_dim,
    get_trt_tensor,
    to_numpy,
)
from torch_tensorrt.fx.converters.converter_utils import (
    has_dynamic_shape,
    set_layer_name,
)
from torch_tensorrt.fx.types import TRTTensor
from torch_tensorrt.fx.utils import get_dynamic_dims


def batch_norm(
    ctx: ConversionContext,
    target: Target,
    source_ir: Optional[SourceIR],
    name: str,
    input: TRTTensor,
    weight: Optional[Union[torch.Tensor, np.ndarray]],
    bias: Optional[Union[torch.Tensor, np.ndarray]],
    running_mean: Optional[Union[torch.Tensor, np.ndarray]],
    running_var: Optional[Union[torch.Tensor, np.ndarray]],
    training: bool,
    momentum: float,
    eps: float,
    cudnn_enabled: bool,
    return_mean_rstd: bool,
) -> Union[TRTTensor, Tuple[TRTTensor, torch.Tensor, torch.Tensor]]:
    if has_dynamic_shape(input.shape):
        assert input.shape[1] != -1, "Channel dim can't be dynamic for batch norm."

    if weight is None:
        weight = 1.0

    if bias is None:
        bias = 0.0

    if running_mean is None:
        running_mean = 0.0

    if running_var is None:
        running_var = 1.0

    scale = to_numpy(weight) / np.sqrt(to_numpy(running_var) + eps)
    bias = to_numpy(bias) - to_numpy(running_mean) * scale
    power = np.ones_like(scale)

    # For BatchNorm1d, reshape 1d to 2d
    output_shape = input.shape
    if len(input.shape) < 4:
        assert (
            len(get_dynamic_dims(input.shape)) <= 1
        ), "BatchNorm1D with more than one dynamic dims is not currently supported."
        new_shape = (
            (input.shape[0], input.shape[1], 1, 1)
            if len(input.shape) == 2
            else (input.shape[0], input.shape[1], input.shape[2], 1)
        )
        input = impl.shuffle.reshape(
            ctx, target, source_ir, f"{name}_reshape_2d", input, new_shape
        )
    layer = ctx.net.add_scale(input, trt.ScaleMode.CHANNEL, bias, scale, power)
    set_layer_name(layer, target, name, source_ir)
    output = layer.get_output(0)

    # For BatchNorm1d, reshape output back to 1d
    if len(output_shape) < 4:
        output = impl.shuffle.reshape(
            ctx,
            target,
            source_ir,
            f"{name}_reshape_1d",
            layer.get_output(0),
            output_shape,
        )

    if return_mean_rstd:
        # return fake mean and rstd for now
        return output, None, None

    return output


def layer_norm(
    ctx: ConversionContext,
    target: Target,
    source_ir: Optional[SourceIR],
    name: str,
    input: TRTTensor,
    normalized_shape: List[int],
    weight: Optional[Union[torch.Tensor, np.ndarray]],
    bias: Optional[Union[torch.Tensor, np.ndarray]],
    eps: float,
    cudnn_enable: bool,
    return_mean_rstd: bool,
) -> Union[TRTTensor, Tuple[TRTTensor, torch.Tensor, torch.Tensor]]:
    dims = list(range(len(input.shape) - len(normalized_shape), len(input.shape)))
    axes = get_axes_for_reduce_op(dims)

    weight = get_trt_tensor(ctx, weight, f"{name}_weight")
    bias = get_trt_tensor(ctx, bias, f"{name}_bias")
    if tuple(input.shape) != tuple(weight.shape):
        weight = impl.slice.expand(
            ctx, target, source_ir, f"{name}_expand_weight", weight, input.shape
        )
    if tuple(input.shape) != tuple(bias.shape):
        bias = impl.slice.expand(
            ctx, target, source_ir, f"{name}_expand_bias", bias, input.shape
        )

    layer_norm = ctx.net.add_normalization(input, weight, bias, axes)
    layer_norm.epsilon = eps
    layer_norm.compute_precision = input.dtype
    set_layer_name(layer_norm, target, f"{name}_layer_norm", source_ir)

    if return_mean_rstd:
        # return fake mean and rstd for now
        return layer_norm.get_output(0), None, None

    return layer_norm.get_output(0)


def native_group_norm(
    ctx: ConversionContext,
    target: Target,
    source_ir: Optional[SourceIR],
    name: str,
    input: TRTTensor,
    weight: Optional[Union[torch.Tensor, np.ndarray]],
    bias: Optional[Union[torch.Tensor, np.ndarray]],
    N: int,
    C: int,
    HxW: int,
    group: int,
    eps: float,
    return_mean_rstd: bool = True,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    assert (
        len(input.shape) >= 3
    ), f"The input dimension should not be less than 3, got {len(input.shape)}!"
    B, C = input.shape[0], input.shape[1]

    # Groups are a subdivision of the channel dimension.
    assert (
        C % group == 0
    ), f"The num of channels ({C}) should be divisible by num_groups ({group})!"

    if weight is None:
        weight = to_numpy(1.0)

    if bias is None:
        bias = to_numpy(0.0)

    # Normalize every group.
    reshaped_input = impl.shuffle.reshape(
        ctx,
        target,
        source_ir,
        name,
        input,
        (B * group, -1),
    )

    dim = 1

    # E[X]
    mean_trt = impl.reduce.mean(
        ctx,
        target,
        source_ir,
        f"{name}_mean",
        reshaped_input,
        dim,
        True,
    )

    # X - E[X]
    sub_trt = impl.elementwise.sub(
        ctx,
        target,
        source_ir,
        f"{name}_sub",
        reshaped_input,
        mean_trt,
    )

    # variance = mean(pow(sub_trt, 2))
    pow_trt = get_trt_tensor(ctx, 2, f"{name}_power", np.float32)
    pow_var = impl.elementwise.pow(
        ctx,
        target,
        source_ir,
        f"{name}_pow",
        sub_trt,
        pow_trt,
    )

    var_trt = impl.reduce.mean(
        ctx,
        target,
        source_ir,
        f"{name}_mean_var",
        pow_var,
        dim,
        True,
    )

    # sqrt((var + eps))
    eps_trt = get_trt_tensor(ctx, eps, f"{name}_eps", np.float32)
    add_trt = impl.elementwise.add(
        ctx,
        target,
        source_ir,
        f"{name}_add",
        var_trt,
        eps_trt,
    )
    sqrt_trt = impl.unary.sqrt(
        ctx,
        target,
        source_ir,
        f"{name}_sqrt",
        add_trt,
    )

    # y = (X - E[X]) / sqrt((var + eps))
    div_trt = impl.elementwise.div(
        ctx,
        target,
        source_ir,
        f"{name}_div",
        sub_trt,
        sqrt_trt,
    )

    # y * gamma + beta
    gamma_trt = get_trt_tensor(ctx, weight, f"{name}_gamma")
    beta_trt = get_trt_tensor(ctx, bias, f"{name}_beta")

    output = impl.shuffle.reshape(
        ctx,
        target,
        source_ir,
        f"{name}_reshape_div",
        div_trt,
        input.shape,
    )

    weight_bias_shape = (1, C) + (1,) * (len(input.shape) - 2)

    reshaped_gamma = impl.shuffle.reshape(
        ctx,
        target,
        source_ir,
        f"{name}_reshape_gamma",
        gamma_trt,
        weight_bias_shape,
    )

    output = impl.elementwise.mul(
        ctx,
        target,
        source_ir,
        f"{name}_mul_gamma",
        output,
        reshaped_gamma,
    )

    reshaped_bias = impl.shuffle.reshape(
        ctx,
        target,
        source_ir,
        f"{name}_reshape_beta",
        beta_trt,
        weight_bias_shape,
    )

    output = impl.elementwise.add(
        ctx,
        target,
        source_ir,
        f"{name}_add_beta",
        output,
        reshaped_bias,
    )

    if return_mean_rstd:
        # return fake mean and rstd for now
        return output, None, None

    return output


def group_norm(
    ctx: ConversionContext,
    target: Target,
    source_ir: Optional[SourceIR],
    name: str,
    input: TRTTensor,
    num_groups: int,
    weight: Optional[Union[torch.Tensor, np.ndarray]],
    bias: Optional[Union[torch.Tensor, np.ndarray]],
    eps: float,
    cudnn_enabled: bool,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    return native_group_norm(
        ctx,
        target,
        source_ir,
        name,
        input,
        weight,
        bias,
        0,
        0,
        0,
        num_groups,
        eps,
        return_mean_rstd=False,
    )


def softmax(
    ctx: ConversionContext,
    target: Target,
    source_ir: Optional[SourceIR],
    name: str,
    input: TRTTensor,
    dim: Optional[Any] = None,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_ranks = len(input.shape)

    if not isinstance(input, TRTTensor):
        raise RuntimeError(
            f"softmax received input {input} that is not part "
            "of the TensorRT region!"
        )

    # Used to get dim when dim is None. Copied from PyTorch softmax implementation.
    def get_softmax_dim(ndim: int) -> int:
        if ndim == 0 or ndim == 1 or ndim == 3:
            ret = 0
        else:
            ret = 1
        return ret

    if dim is None:
        dim = get_softmax_dim(input_ranks)
    else:
        dim = cast(int, dim)

    dim = get_positive_dim(dim, input_ranks)

    layer = ctx.net.add_softmax(input)
    layer.axes = 1 << dim
    set_layer_name(layer, target, name, source_ir)
    return layer.get_output(0)


def pdist(
    ctx: ConversionContext,
    target: Target,
    source_ir: Optional[SourceIR],
    name: str,
    input: TRTTensor,
    p: float = 2,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    shape = input.shape
    # Extend input from shape [N, D] to [N, 1, D]
    extend_input = impl.shuffle.reshape(
        ctx,
        target,
        source_ir,
        f"{name}_reshape",
        input,
        shape=shape[0:1] + (1,) + shape[1:],
    )
    # Expand the input from [N, 1, D] to [N, N, D]
    x = impl.slice.expand(
        ctx,
        target,
        source_ir,
        f"{name}_sub",
        extend_input,
        (shape[0], shape[0]) + shape[1:],
    )
    # Subtract the expanded input from original input. Result shape = [N, N, D]
    # This matrix has the distance of each sample to every other sample and hence the shape is [N, N, D]
    x = impl.elementwise.sub(ctx, target, source_ir, f"{name}_sub", x, input)

    if p == 0:
        # norm = torch.sum(x!=0, dim=2)
        nonzero_val = impl.elementwise.ne(ctx, target, source_ir, f"{name}_ne", x, 0)
        norm = impl.reduce.sum(
            ctx, target, source_ir, f"{name}_sum", nonzero_val, dim=2, keepdim=False
        )
        norm = cast_trt_tensor(
            ctx, norm, torch.float32, f"{name}_cast", target, source_ir
        )
    elif p == 1:
        # norm = torch.sum(torch.abs(x), dim=2)
        abs_val = impl.unary.abs(ctx, target, source_ir, f"{name}_abs", x)
        norm = impl.reduce.sum(
            ctx, target, source_ir, f"{name}_sum", abs_val, dim=2, keepdim=False
        )
    elif 0 < p < 1 or 1 < p < float("inf"):
        # norm = torch.pow(torch.sum(torch.pow(torch.abs(x), p), dim=2), 1/p)
        abs_val = impl.unary.abs(ctx, target, source_ir, f"{name}_abs", x)
        pow_val = impl.elementwise.pow(
            ctx, target, source_ir, f"{name}_pow1", abs_val, p
        )
        sum_val = impl.reduce.sum(
            ctx, target, source_ir, f"{name}_sum", pow_val, dim=2, keepdim=False
        )
        norm = impl.elementwise.pow(
            ctx, target, source_ir, f"{name}_pow2", sum_val, 1 / p
        )
    elif p == float("inf"):
        # norm = torch.max(torch.abs(x))
        abs_val = impl.unary.abs(ctx, target, source_ir, f"{name}_abs", x)
        norm = impl.reduce.max(
            ctx,
            target,
            source_ir,
            f"{name}_max",
            abs_val,
            dim=2,
            keepdim=False,
            return_indices=False,
        )
    else:
        raise RuntimeError(
            f"p should between [0, inf], currently p={p} is not supported!"
        )
    indices = np.triu_indices(shape[0], k=1)
    return impl.select.index(ctx, target, source_ir, f"{name}_index", norm, indices)
