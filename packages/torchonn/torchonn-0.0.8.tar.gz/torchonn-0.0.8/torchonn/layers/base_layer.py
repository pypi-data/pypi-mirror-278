"""
Date: 2024-05-31 22:37:26
LastEditors: Jiaqi Gu && jiaqigu@asu.edu
LastEditTime: 2024-05-31 22:59:39
FilePath: /pytorch-onn/torchonn/layers/base_layer.py
"""

import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import torch
from mmcv.cnn.bricks import build_activation_layer, build_conv_layer, build_norm_layer
from mmengine.registry import MODELS
from pyutils.general import logger
from torch import Tensor, nn
from torch.nn.modules.utils import _pair
from torch.types import Device

from .utils import partition_chunks

__all__ = [
    "ONNBaseLayer",
    "ONNBaseConv2d",
    "ONNBaseLinear",
    "build_linear_layer",
    "build_conv_layer",
    "build_norm_layer",
    "build_activation_layer",
    "convert_linear_layer",
    "convert_conv_layer",
    "convert_layer",
]


class ONNBaseLayer(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.init_transform()

    def load_cfgs(
        self,
        **cfgs,
    ) -> None:
        raise NotImplementedError

    def register_parameter_buffer(
        self, param_groups: Dict, buffer_groups: Dict
    ) -> None:
        for p_name, p in param_groups.items():
            if not hasattr(self, p_name):
                if not isinstance(p, nn.Parameter):
                    p = nn.Parameter(p)
                self.register_parameter(p_name, p)

        for p_name, p in buffer_groups.items():
            if not hasattr(self, p_name):
                if isinstance(p, nn.Parameter):
                    p = p.data
                self.register_buffer(p_name, p)

    def reset_parameters(self) -> None:
        raise NotImplementedError

    def pack_weights(self) -> None:
        ## e.g, self.weights = {"weight": self.weight}
        raise NotImplementedError

    def build_transform(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def add_transform(self, src_name: str, dst_name: str, transform_cfg: Dict):
        ## if there are any arguments need to pass to the transform function, please pass it before by
        ## wrap it with partial function
        # enable all transforms by default
        transform_cfg = {k: [True, v] for k, v in transform_cfg.items()}
        if src_name in self.transform_registry:
            if dst_name in self.transform_registry[src_name]:
                self.transform_registry[src_name][dst_name].update(transform_cfg)
            else:
                self.transform_registry[src_name][dst_name] = transform_cfg
        else:
            for name in self.transform_registry:
                if dst_name in self.transform_registry[name]:

                    raise ValueError(
                        f"output transform param {dst_name} already exists for source param {name}"
                    )
            self.transform_registry[src_name] = {dst_name: transform_cfg}

    def set_transform_flag(
        self, src_name: str, dst_name: str, transform_name: str, flag: bool = True
    ) -> None:
        assert (
            src_name in self.transform_registry
        ), f"source params {src_name} not found in transform_registry"

        assert (
            dst_name in self.transform_registry[src_name]
        ), f"target params {dst_name} not found in transform_registry of {src_name}"

        assert (
            transform_name in self.transform_registry[src_name][dst_name]
        ), f"transform {transform_name} not found for src param {src_name} -> dst param {dst_name}"

        self.transform_registry[src_name][dst_name][transform_name][0] = flag

    def remove_transform(
        self, src_name: str, dst_name: str = None, transform_name: str = None
    ) -> None:
        assert (
            src_name in self.transform_registry
        ), f"source params {src_name} not found in transform_registry"

        if dst_name is None:
            del self.transform_registry[src_name]
        else:
            assert (
                dst_name in self.transform_registry[src_name]
            ), f"target params {dst_name} not found in transform_registry of {src_name}"

            if transform_name is None:
                del self.transform_registry[src_name][dst_name]
            else:
                assert (
                    transform_name in self.transform_registry[src_name][dst_name]
                ), f"transform {transform_name} not found for src param {src_name} -> dst param {dst_name}"

                del self.transform_registry[src_name][dst_name][transform_name]

    def clear_transform(self, name: str) -> None:
        assert (
            name in self.transform_registry
        ), f"params {name} not found in transform_registry"
        self.transform_registry[name] = {}

    def init_transform(
        self,
    ) -> None:
        self.transform_registry = {}

    @classmethod
    def from_layer(cls, layer: nn.Module, *args, **kwargs) -> nn.Module:
        raise NotImplementedError

    def get_num_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def enable_fast_forward(self) -> None:
        self.fast_forward_flag = True

    def disable_fast_forward(self) -> None:
        self.fast_forward_flag = False

    def set_phase_variation(
        self, noise_std: float, random_state: Optional[int] = None
    ) -> None:
        self.phase_noise_std = noise_std

    def set_gamma_noise(
        self, noise_std: float, random_state: Optional[int] = None
    ) -> None:
        self.gamma_noise_std = noise_std

    def set_crosstalk_factor(self, crosstalk_factor: float) -> None:
        self.crosstalk_factor = crosstalk_factor

    def set_weight_bitwidth(self, w_bit: int) -> None:
        self.w_bit = w_bit

    def set_input_bitwidth(self, in_bit: int) -> None:
        self.in_bit = in_bit

    def set_output_bitwidth(self, out_bit: int) -> None:
        self.out_bit = out_bit

    def load_parameters(self, param_dict: Dict[str, Any]) -> None:
        """
        description: update parameters based on this parameter dictionary\\
        param param_dict {dict of dict} {param_name: param_tensor, ...}
        """
        for name, param in param_dict.items():
            getattr(self, name).data.copy_(param)

    def switch_mode_to(self, mode: str) -> None:
        src_mode = self.mode
        self.mode = mode

        if src_mode in self.transform_registry:
            transforms = self.transform_registry[src_mode]
            del self.transform_registry[src_mode]
            self.transform_registry[mode] = transforms

    def get_output_dim(
        self, img_height: int | None = None, img_width: int | None = None
    ):
        if hasattr(self, "kernel_size"):
            h_out = (
                img_height
                - self.dilation[0] * (self.kernel_size[0] - 1)
                - 1
                + 2 * self.padding[0]
            ) / self.stride[0] + 1
            w_out = (
                img_width
                - self.dilation[1] * (self.kernel_size[1] - 1)
                - 1
                + 2 * self.padding[1]
            ) / self.stride[1] + 1
            return int(h_out), int(w_out)
        elif hasattr(self, "out_features"):
            return self.out_features
        else:
            raise NotImplementedError

    def transform_weight(
        self, weights: Dict[str, Tensor] | None = None
    ) -> dict[str, Tensor]:
        ## forward weights through transform, e.g., reparameterization, quantization, pruning, adding noise etc.
        ## weights, e.g., {"weight": self.weight} -> return weight
        if weights is None:
            weights = self.weights
        new_weights = {}
        for src_name, weight in weights.items():
            if src_name in self.transform_registry:
                for dst_name, transforms in self.transform_registry[src_name].items():
                    for flag, transform in transforms.values():
                        if flag:
                            weight = transform(weight)

                    new_weights[dst_name] = weight
        return new_weights

    def transform_input(self, x: Tensor) -> Tensor:
        ## forward input through transform, e.g., reparameterization, quantization, pruning, adding noise etc.
        ## x -> return x
        for transforms in self.transform_registry["input"].values():
            for flag, transform in transforms.values():
                if flag:
                    x = transform(x)
        return x

    def transform_output(self, x: Tensor) -> Tensor:
        ## forward output through transform, e.g., reparameterization, quantization, pruning, adding noise etc.
        ## x -> return x
        for transforms in self.transform_registry["output"].values():
            for flag, transform in transforms.values():
                if flag:
                    x = transform(x)
        return x

    def _forward_impl(self, x: Tensor, weights: Dict[str, Tensor]) -> Tensor:
        raise NotImplementedError

    def _input_transform(self, x: Tensor) -> Tensor:
        return x

    def _weight_transform(self, weights: Tensor | Tuple[Tensor]) -> Dict[str, Tensor]:
        return weights

    def _output_transform(self, x: Tensor) -> Tensor:
        return x

    def forward(self, x: Tensor) -> Tensor:
        ## preprocess input
        x = self.transform_input(x)

        ## preprocess weights
        weights = self.transform_weight(self.weights)

        ## forward pass
        out = self._forward_impl(x, weights)

        ## postprocess output
        out = self.transform_output(out)

        ## add bias
        if self.bias is not None:
            out = out + self.bias.reshape([-1] + [1] * (out.dim() - 2))

        return out

    def extra_repr(self) -> str:
        return ""


class ONNBaseConv2d(ONNBaseLayer):
    __constants__ = [
        "stride",
        "padding",
        "dilation",
        "groups",
        "padding_mode",
        "output_padding",
        "in_channels",
        "out_channels",
        "kernel_size",
        "miniblock",
    ]
    __annotations__ = {"bias": Optional[torch.Tensor]}

    _in_channels: int
    out_channels: int
    kernel_size: Tuple[int, ...]
    stride: Tuple[int, ...]
    padding: Tuple[int, ...]
    dilation: Tuple[int, ...]
    transposed: bool
    output_padding: Tuple[int, ...]
    groups: int
    padding_mode: str
    weight: Tensor
    bias: Optional[Tensor]

    ## default configs
    default_cfgs = dict(
        miniblock=(
            1,
            1,
            4,
            4,
        ),  # [#tiles, pe per tile, row, col] # i.e., [R, C, k1, k2]
        w_bit=32,
        in_bit=32,
        out_bit=32,
        photodetect=False,
        device=torch.device("cpu"),
    )

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

    def load_cfgs(
        self,
        **cfgs,
    ) -> None:
        self.__dict__.update(self.default_cfgs)
        self.__dict__.update(cfgs)
        self.kernel_size = _pair(self.kernel_size)
        self.stride = _pair(self.stride)
        self.padding = _pair(self.padding)
        self.dilation = _pair(self.dilation)
        assert (
            self.groups == 1
        ), f"Currently group convolution is not supported, but got group: {self.groups}"

        if "miniblock" in self.__dict__:

            self.load_block_cfgs()

    def load_block_cfgs(self) -> None:
        self.in_channels_flat = self.in_channels * np.prod(self.kernel_size)

        if isinstance(self.miniblock, int):
            self.miniblock = (1, 1, self.miniblock, self.miniblock)
        else:
            if len(self.miniblock) == 2:
                self.miniblock = (1, 1, *self.miniblock)
            assert (
                len(self.miniblock) >= 4 and len(self.miniblock) % 2 == 0
            ), logger.error(
                f"Invalid miniblock config {self.miniblock}. Must be even number of integers or a single integer"
            )

        self.miniblock_dim_x = np.prod(self.miniblock[1::2])
        self.miniblock_dim_y = np.prod(self.miniblock[::2])
        self.grid_dim_x = int(np.ceil(self.in_channels_flat / self.miniblock_dim_x))
        self.grid_dim_y = int(np.ceil(self.out_channels / self.miniblock_dim_y))
        self.in_channels_pad = self.grid_dim_x * self.miniblock_dim_x
        self.out_channels_pad = self.grid_dim_y * self.miniblock_dim_y

    @classmethod
    def from_layer(
        cls,
        layer: nn.Conv2d,
        **cfgs,
    ) -> nn.Module:
        """Initialize from a nn.Conv2d/nn.Linear layer. Weight mapping will be performed

        Args:
            cfgs for the optical layer
        Returns:
            Module: a converted optical layer module
        """
        assert isinstance(
            layer, nn.Conv2d
        ), f"The conversion target must be nn.Conv2d, but got {type(layer)}."
        in_channels = layer.in_channels
        out_channels = layer.out_channels
        kernel_size = layer.kernel_size
        stride = layer.stride
        padding = layer.padding
        dilation = layer.dilation
        groups = layer.groups
        bias = layer.bias is not None
        device = layer.weight.data.device
        instance = cls(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=groups,
            bias=bias,
            **cfgs,
        ).to(device)
        if "miniblock" in instance.__dict__:
            weight = partition_chunks(
                layer.weight.data.flatten(1), instance.weight.shape
            )
        else:
            weight = layer.weight.data
        instance.weight.data.copy_(weight)

        instance.sync_parameters(src="weight")
        if bias:
            instance.bias.data.copy_(layer.bias)

        return instance

    def extra_repr(self):
        s = (
            "{in_channels}, {out_channels}, kernel_size={kernel_size}"
            ", stride={stride}"
        )
        if self.padding != (0,) * len(self.padding):
            s += ", padding={padding}"
        if self.dilation != (1,) * len(self.dilation):
            s += ", dilation={dilation}"
        if self.groups != 1:
            s += ", groups={groups}"
        if self.bias is None:
            s += ", bias=False"
        if self.miniblock is not None:
            s += ", miniblock={miniblock}"
        if self.in_bit is not None:
            s += ", in_bit={in_bit}"
        if self.w_bit is not None:
            s += ", in_bit={w_bit}"
        if self.out_bit is not None:
            s += ", out_bit={out_bit}"

        s = s.format(**self.__dict__)
        return s


class ONNBaseLinear(ONNBaseLayer):
    __constants__ = ["in_features", "out_features"]
    in_features: int
    out_features: int
    weight: Tensor

    ## default configs
    default_cfgs = dict(
        miniblock=(
            1,
            1,
            4,
            4,
        ),  # [#tiles, pe per tile, row, col] # i.e., [R, C, k1, k2]
        w_bit=32,
        in_bit=32,
        out_bit=32,
        photodetect=False,
        device=torch.device("cpu"),
    )

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

    def load_cfgs(
        self,
        **cfgs,
    ) -> None:
        self.__dict__.update(self.default_cfgs)
        self.__dict__.update(cfgs)

        if "miniblock" in self.__dict__:
            self.load_block_cfgs()

    def load_block_cfgs(self) -> None:
        if isinstance(self.miniblock, int):
            self.miniblock = (1, 1, self.miniblock, self.miniblock)
        else:
            if len(self.miniblock) == 2:
                self.miniblock = (1, 1, *self.miniblock)
            assert (
                len(self.miniblock) >= 4 and len(self.miniblock) % 2 == 0
            ), logger.error(
                f"Invalid miniblock config {self.miniblock}. Must be even number of integers or a single integer"
            )

        self.miniblock_dim_x = np.prod(self.miniblock[1::2])
        self.miniblock_dim_y = np.prod(self.miniblock[::2])
        self.grid_dim_x = int(np.ceil(self.in_features / self.miniblock_dim_x))
        self.grid_dim_y = int(np.ceil(self.out_features / self.miniblock_dim_y))
        self.in_features_pad = self.grid_dim_x * self.miniblock_dim_x
        self.out_features_pad = self.grid_dim_y * self.miniblock_dim_y

    @classmethod
    def from_layer(
        cls,
        layer: nn.Conv2d,
        **cfgs,
    ) -> nn.Module:
        """Initialize from a nn.Conv2d/nn.Linear layer. Weight mapping will be performed

        Args:
            cfgs for the optical layer
        Returns:
            Module: a converted optical layer module
        """
        assert isinstance(
            layer, nn.Linear
        ), f"The conversion target must be nn.Linear, but got {type(layer)}."

        in_features = layer.in_features
        out_features = layer.out_features
        bias = layer.bias is not None
        device = layer.weight.data.device
        instance = cls(
            in_features=in_features,
            out_features=out_features,
            bias=bias,
            **cfgs,
        ).to(device)

        if "miniblock" in instance.__dict__:
            weight = partition_chunks(layer.weight.data, instance.weight.shape)
        else:
            weight = layer.weight.data
        instance.weight.data.copy_(weight)

        instance.sync_parameters(src="weight")
        if bias:
            instance.bias.data.copy_(layer.bias)

        return instance

    def extra_repr(self):
        s = "{in_features}, {out_features}"
        if self.bias is None:
            s += ", bias=False"
        if self.miniblock is not None:
            s += ", miniblock={miniblock}"
        if self.in_bit is not None:
            s += ", in_bit={in_bit}"
        if self.w_bit is not None:
            s += ", in_bit={w_bit}"
        if self.out_bit is not None:
            s += ", out_bit={out_bit}"

        s = s.format(**self.__dict__)
        return s


def build_linear_layer(cfg: Optional[Dict], *args, **kwargs) -> nn.Module:
    if cfg is None:
        cfg_ = dict(type="Linear")
    else:
        if not isinstance(cfg, dict):
            raise TypeError("cfg must be a dict")
        if "type" not in cfg:
            raise KeyError('the cfg dict must contain the key "type"')
        cfg_ = cfg.copy()

    layer_type = cfg_.pop("type")
    if inspect.isclass(layer_type):
        return layer_type(*args, **kwargs, **cfg_)  # type: ignore
    # Switch registry to the target scope. If `linear_layer` cannot be found
    # in the registry, fallback to search `linear_layer` in the
    # mmengine.MODELS.
    with MODELS.switch_scope_and_registry(None) as registry:
        linear_layer = registry.get(layer_type)
    if linear_layer is None:
        raise KeyError(
            f"Cannot find {linear_layer} in registry under scope "
            f"name {registry.scope}"
        )
    layer = linear_layer(*args, **kwargs, **cfg_)

    return layer


def convert_linear_layer(ref_layer: nn.Module, cfg: Optional[Dict]) -> nn.Module:
    if cfg is None:
        cfg_ = dict(type="Linear")
    else:
        if not isinstance(cfg, dict):
            raise TypeError("cfg must be a dict")
        if "type" not in cfg:
            raise KeyError('the cfg dict must contain the key "type"')
        cfg_ = cfg.copy()

    layer_type = cfg_.pop("type")

    device = next(ref_layer.parameters()).device

    if inspect.isclass(layer_type):
        assert hasattr(
            layer_type, "from_layer"
        ), f"{layer_type} does not have a from_layer method for conversion"
        return layer_type.from_layer(ref_layer, **cfg_).to(device)

    # Switch registry to the target scope. If `linear_layer` cannot be found
    # in the registry, fallback to search `linear_layer` in the
    # mmengine.MODELS.
    with MODELS.switch_scope_and_registry(None) as registry:
        linear_layer = registry.get(layer_type)
    if linear_layer is None:
        raise KeyError(
            f"Cannot find {linear_layer} in registry under scope "
            f"name {registry.scope}"
        )
    assert hasattr(
        linear_layer, "from_layer"
    ), f"{linear_layer} does not have a from_layer method for conversion"
    layer = linear_layer.from_layer(ref_layer, **cfg_).to(device)
    return layer


def convert_conv_layer(ref_layer: nn.Module, cfg: Optional[Dict]) -> nn.Module:
    """Build convolution layer.

    Args:
        cfg (None or dict): The conv layer config, which should contain:
            - type (str): Layer type.
            - layer args: Args needed to instantiate an conv layer.
        args (argument list): Arguments passed to the `__init__`
            method of the corresponding conv layer.
        kwargs (keyword arguments): Keyword arguments passed to the `__init__`
            method of the corresponding conv layer.

    Returns:
        nn.Module: Created conv layer.
    """
    if cfg is None:
        cfg_ = dict(type="Conv2d")
    else:
        if not isinstance(cfg, dict):
            raise TypeError("cfg must be a dict")
        if "type" not in cfg:
            raise KeyError('the cfg dict must contain the key "type"')
        cfg_ = cfg.copy()

    layer_type = cfg_.pop("type")

    device = next(ref_layer.parameters()).device

    if inspect.isclass(layer_type):
        assert hasattr(
            layer_type, "from_layer"
        ), f"{layer_type} does not have a from_layer method for conversion"
        return layer_type.from_layer(ref_layer, **cfg_).to(device)
    # Switch registry to the target scope. If `conv_layer` cannot be found
    # in the registry, fallback to search `conv_layer` in the
    # mmengine.MODELS.
    with MODELS.switch_scope_and_registry(None) as registry:
        conv_layer = registry.get(layer_type)
    if conv_layer is None:
        raise KeyError(
            f"Cannot find {conv_layer} in registry under scope "
            f"name {registry.scope}"
        )
    assert hasattr(
        conv_layer, "from_layer"
    ), f"{conv_layer} does not have a from_layer method for conversion"
    layer = conv_layer.from_layer(ref_layer, **cfg_).to(device)

    return layer


def convert_layer(ref_layer: nn.Module, cfg: Optional[Dict]) -> nn.Module:
    if isinstance(ref_layer, nn.Conv2d):
        return convert_conv_layer(ref_layer, cfg)
    elif isinstance(ref_layer, nn.Linear):
        return convert_linear_layer(ref_layer, cfg)
    else:
        raise NotImplementedError(f"Conversion for {type(ref_layer)} is not supported")