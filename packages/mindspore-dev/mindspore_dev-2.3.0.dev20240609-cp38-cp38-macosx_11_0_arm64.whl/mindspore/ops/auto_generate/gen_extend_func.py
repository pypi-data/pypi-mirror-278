# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

from mindspore.common import dtype as mstype
from mindspore.ops.auto_generate.pyboost_inner_prim import *


def add(input, other, alpha=1):
    r"""
    Adds scaled other value to input Tensor.
    
    .. math::
    
        out_{i} = input_{i} + alpha \times other_{i}
    
    Note:
        - When the two inputs have different shapes,
          they must be able to broadcast to a common shape.
        - The two inputs and alpha comply with the implicit type conversion rules to make the data types
          consistent.
    
    Args:
        input (Union[Tensor, number.Number, bool]): The first input is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        other (Union[Tensor, number.Number, bool]): The second input, is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        alpha (number.Number): A scaling factor applied to `other`, default 1.
    
    Returns:
        Tensor, the shape is the same as the one of the input `input`, `other` after broadcasting,
        and the data type is the one with higher precision or higher digits among the two inputs and alpha.
    
    Raises:
        TypeError: If the type of `input`, `other`, or `alpha` is not one of the following: Tensor, number.Number, bool.
        TypeError: If `alpha` is of type float but `input` and `other` are not of type float.
        TypeError: If `alpha` is of type bool but `input` and `other` are not of type bool.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore import Tensor
        >>> from mindspore.ops.extend import add
        >>> x = Tensor(1, mindspore.int32)
        >>> y = Tensor(np.array([4, 5, 6]).astype(np.float32))
        >>> alpha = 0.5
        >>> output = add(x, y, alpha)
        >>> print(output)
        [3. 3.5 4.]
        >>> # the data type of x is int32, the data type of y is float32,
        >>> # alpha is a float, and the output is the data format of higher precision float32.
        >>> print(output.dtype)
        Float32
    """
    return add_impl(input, other, alpha)


def bmm(input, mat2):
    r"""
    Performs batch matrix-matrix multiplication of two three-dimensional tensors.
    
    .. math::
        \text{output}[b, i, j] = \text{input}[b, i, k] @ \text{mat2}[b, k, j]
    
    Args:
        input (Tensor): The first batch of matrices to be multiplied. Must be a three-dimensional tensor.
        mat2 (Tensor): The second batch of matrices to be multiplied. Must be a three-dimensional tensor.
    
    Returns:
        Tensor, the output tensor of shape `(b, n, p)`, where each matrix is the product of the corresponding matrices in the input batches.
    
    Raises:
        TypeError: If `input` or `mat2` is not three-dimensional tensors.
        ValueError: If the length of the third dimension of `input` is not equal to the length of the second dimension of `mat2`.
        ValueError: If the batch size of the inputs do not match.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> from mindspore.ops.extend import bmm
        >>> a = Tensor(np.ones(shape=[2, 3, 4]), mindspore.float32)
        >>> b = Tensor(np.ones(shape=[2, 4, 5]), mindspore.float32)
        >>> output = bmm(a, b)
        >>> print(output.shape)
        (2, 3, 5)
    """
    return bmm_impl(input, mat2)


def ffn(x, weight1, weight2, expertTokens=None, bias1=None, bias2=None, scale=None, offset=None, deqScale1=None, deqScale2=None, antiquant_scale1=None, antiquant_scale2=None, antiquant_offset1=None, antiquant_offset2=None, activation='fastgelu', inner_precise=0):
    r"""
    None
    """
    return ffn_impl(x, weight1, weight2, expertTokens, bias1, bias2, scale, offset, deqScale1, deqScale2, antiquant_scale1, antiquant_scale2, antiquant_offset1, antiquant_offset2, converted_activation, inner_precise)


def flatten(input, start_dim=0, end_dim=-1):
    r"""
    Flatten a tensor along dimensions from `start_dim` to `end_dim`.
    
    Args:
        input (Tensor): The input Tensor.
    
    Keyword Args:
        start_dim (int, optional): The first dimension to flatten. Default: ``0`` .
        end_dim (int, optional): The last dimension to flatten. Default: ``-1`` .
    
    Returns:
        Tensor. If no dimensions are flattened, returns the original `input`, otherwise return the flattened Tensor.
        If `input` is a 0-dimensional Tensor, a 1-dimensional Tensor will be returned.
    
    Raises:
        TypeError: If `input` is not a Tensor.
        TypeError: If `start_dim` or `end_dim` is not int.
        ValueError: If `start_dim` is greater than `end_dim` after canonicalized.
        ValueError: If `start_dim` or `end_dim` is not in range of [-input.dim, input.dim-1].
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, mint
        >>> input_x = Tensor(np.ones(shape=[1, 2, 3, 4]), mindspore.float32)
        >>> output = mint.flatten(input_x)
        >>> print(output.shape)
        (24,)
    """
    return flatten_impl(input, start_dim, end_dim)


def index_select(input, dim, index):
    r"""
    Generates a new Tensor that accesses the values of `input` along the specified `dim` dimension
    using the indices specified in `index`. The new Tensor has the same number of dimensions as `input`,
    with the size of the `dim` dimension being equal to the length of `index`, and the size of all other
    dimensions will be unchanged from the original `input` Tensor.
    
    .. note::
        The value of index must be in the range of `[0, input.shape[dim])`, the result is undefined out of range.
    
    Args:
        input (Tensor): The input Tensor.
        dim (int): The dimension to be indexed.
        index (Tensor): A 1-D Tensor with the indices.
    
    Returns:
        Tensor, has the same dtype as input Tensor.
    
    Raises:
        TypeError: If `input` or `index` is not a Tensor.
        TypeError: If `dim` is not int number.
        ValueError: If the value of `dim` is out the range of `[-input.ndim, input.ndim - 1]`.
        ValueError: If the dimension of `index` is not equal to 1.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import mindspore
        >>> from mindspore import Tensor, ops
        >>> import numpy as np
        >>> input = Tensor(np.arange(16).astype(np.float32).reshape(2, 2, 4))
        >>> print(input)
        [[[ 0.  1.  2.  3.]
        [ 4.  5.  6.  7.]]
        [[ 8.  9. 10. 11.]
        [12. 13. 14. 15.]]]
        >>> index = Tensor([0,], mindspore.int32)
        >>> y = ops.index_select_ext(input, 1, index)
        >>> print(y)
        [[[ 0.  1.  2.  3.]]
        [[ 8.  9. 10. 11.]]]
    """
    return index_select_impl(input, dim, index)


def leaky_relu(input, negative_slope=0.01):
    r"""
    leaky_relu activation function. The element of `input` less than 0 times `negative_slope` .
    
    The activation function is defined as:
    
    .. math::
        \text{leaky_relu}(input) = \begin{cases}input, &\text{if } input \geq 0; \cr
        {\negative_slope} * input, &\text{otherwise.}\end{cases}
    
    where :math:`\negative_slope` represents the `negative_slope` parameter.
    
    For more details, see `Rectifier Nonlinearities Improve Neural Network Acoustic Models
    <https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf>`_.
    
    LeakyReLU Activation Function Graph:
    
    .. image:: ../images/LeakyReLU.png
        :align: center
    
    Args:
        input (Tensor): The input of leaky_relu is a Tensor of any dimension.
        negative_slope (Union[int, float]): Slope of the activation function when the element of `input` is less than 0.
          Default: ``0.01`` .
    
    Returns:
        Tensor, has the same type and shape as the `input`.
    
    Raises:
        TypeError: If `input` is not a Tensor.
        TypeError: If `negative_slope` is not a float or an int.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> input = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> print(mint.leaky_relu(input, negative_slope=0.2))
        [[-0.2  4.  -1.6]
         [ 2.  -1.   9. ]]
    """
    return leaky_relu_impl(input, negative_slope)


def matmul(input, mat2):
    r"""
    None
    """
    return matmul_impl(input, mat2)


def mean(input, axis=None, keep_dims=False, dtype=None):
    r"""
    Reduces all dimension of a tensor by averaging all elements in the dimension, by default.
    And reduce a dimension of `input` along the specified `axis`. `keep_dims`
    determines whether the dimensions of the output and input are the same.
    
    Note:
        The `axis` with tensor type is only used for compatibility with older versions and is not recommended.
    
    Args:
        input (Tensor[Number]): The input tensor. The dtype of the tensor to be reduced is number.
            :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
        axis (Union[int, tuple(int), list(int), Tensor]): The dimensions to reduce. Default: ``None`` ,
            reduce all dimensions. Only constant value is allowed. Assume the rank of `input` is r,
            and the value range is [-r,r).
        keep_dims (bool): If ``True`` , keep these reduced dimensions and the length is 1.
            If ``False`` , don't keep these dimensions. Default: ``False`` .
        dtype (:class:`mindspore.dtype`): The desired data type of returned Tensor. Default: ``None`` .
    
    Returns:
        Tensor, has the same data type as input tensor.
    
        - If `axis` is ``None`` , and `keep_dims` is ``False`` ,
          the output is a 0-D tensor representing the product of all elements in the input tensor.
        - If `axis` is int, set as 1, and `keep_dims` is ``False`` ,
          the shape of output is :math:`(x_0, x_2, ..., x_R)`.
        - If `axis` is tuple(int), set as (1, 2), and `keep_dims` is ``False`` ,
          the shape of output is :math:`(x_0, x_3, ..., x_R)`.
        - If `axis` is 1-D Tensor, set as [1, 2], and `keep_dims` is ``False`` ,
          the shape of output is :math:`(x_0, x_3, ..., x_R)`.
    
    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If `axis` is not one of the following: int, tuple, list or Tensor.
        TypeError: If `keep_dims` is not a bool.
        ValueError: If `axis` is out of range.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> x = Tensor(np.random.randn(3, 4, 5, 6).astype(np.float32))
        >>> output = ops.mean(x, 1, keep_dims=True)
        >>> result = output.shape
        >>> print(result)
        (3, 1, 5, 6)
        >>> # case 1: Reduces a dimension by averaging all elements in the dimension.
        >>> x = Tensor(np.array([[[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]],
        ... [[4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5], [6, 6, 6, 6, 6, 6]],
        ... [[6, 6, 6, 6, 6, 6], [8, 8, 8, 8, 8, 8], [10, 10, 10, 10, 10, 10]]]),
        ... mindspore.float32)
        >>> output = ops.mean(x)
        >>> print(output)
        5.0
        >>> print(output.shape)
        ()
        >>> # case 2: Reduces a dimension along the axis 0
        >>> output = ops.mean(x, 0, True)
        >>> print(output)
        [[[4. 4. 4. 4. 4. 4.]
        [5. 5. 5. 5. 5. 5.]
        [6. 6. 6. 6. 6. 6.]]]
        >>> # case 3: Reduces a dimension along the axis 1
        >>> output = ops.mean(x, 1, True)
        >>> print(output)
        [[[2. 2. 2. 2. 2. 2.]]
        [[5. 5. 5. 5. 5. 5.]]
        [[8. 8. 8. 8. 8. 8.]]]
        >>> # case 4: Reduces a dimension along the axis 2
        >>> output = ops.mean(x, 2, True)
        >>> print(output)
        [[[ 2.]
        [ 2.]
        [ 2.]]
        [[ 4.]
        [ 5.]
        [ 6.]]
        [[ 6.]
        [ 8.]
        [10.]]]
    """
    return mean_impl(input, axis, keep_dims, dtype)


def softplus(input, beta=1, threshold=20):
    r"""
    None
    """
    return softplus_impl(input, beta, threshold)


def stack(tensors, dim=0):
    r"""
    Stacks a list of tensors in specified dim.
    
    Stacks the list of input tensors with the same rank `R`, output is a tensor of rank `(R+1)`.
    
    Given input tensors of shape :math:`(x_1, x_2, ..., x_R)`. Set the number of input tensors as `N`.
    If :math:`dim \ge 0`, the shape of the output tensor is
    :math:`(x_1, x_2, ..., x_{dim}, N, x_{dim+1}, ..., x_R)`.
    
    Args:
        tensors (Union[tuple, list]): A Tuple or list of Tensor objects with the same shape and type.
        dim (int): Dimension to stack. The range is [-(R+1), R+1). Default: ``0`` .
    
    Returns:
        Tensor. A stacked Tensor with the same type as `tensors`.
    
    Raises:
        TypeError: If the data types of elements in `tensors` are not the same.
        ValueError: If the length of `tensors` is not greater than zero;
                    or if dim is out of the range [-(R+1), R+1);
                    or if the shapes of elements in tensors are not the same.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> from mindspore import Tensor, mint
        >>> import numpy as np
        >>> data1 = Tensor(np.array([0, 1]).astype(np.float32))
        >>> data2 = Tensor(np.array([2, 3]).astype(np.float32))
        >>> output = mint.stack([data1, data2], 0)
        >>> print(output)
        [[0. 1.]
            [2. 3.]]
    """
    return stack_impl(tensors, dim)


def sub(input, other, alpha=1):
    r"""
    Subtracts scaled other value from input Tensor.
    
    .. math::
    
        out_{i} = input_{i} - alpha \times other_{i}
    
    Note:
        - When the two inputs have different shapes,
          they must be able to broadcast to a common shape.
        - The two inputs and alpha comply with the implicit type conversion rules to make the data types
          consistent.
    
    Args:
        input (Union[Tensor, number.Number, bool]): The first input is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        other (Union[Tensor, number.Number, bool]): The second input, is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        alpha (number.Number): A scaling factor applied to `other`, default 1.
    
    Returns:
        Tensor, the shape is the same as the one of the input `input`, `other` after broadcasting,
        and the data type is the one with higher precision or higher digits among the two inputs and alpha.
    
    Raises:
        TypeError: If the type of `input`, `other`, or `alpha` is not one of the following: Tensor, number.Number, bool.
        TypeError: If `alpha` is of type float but `input` and `other` are not of type float.
        TypeError: If `alpha` is of type bool but `input` and `other` are not of type bool.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore import Tensor
        >>> from mindspore.ops.extend import sub
        >>> x = Tensor(np.array([4, 5, 6]).astype(np.float32))
        >>> y = Tensor(1, mindspore.int32)
        >>> alpha = 0.5
        >>> output = sub(x, y, alpha)
        >>> print(output)
        [3.5 4.5 5.5]
        >>> # the data type of x is float32, the data type of y is int32,
        >>> # alpha is a float, and the output is the data format of higher precision float32.
        >>> print(output.dtype)
        Float32
    """
    return sub_impl(input, other, alpha)


def topk(input, k, dim=-1, largest=True, sorted=True):
    r"""
    None
    """
    return topk_impl(input, k, dim, largest, sorted)

