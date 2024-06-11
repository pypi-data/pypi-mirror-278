# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


from executorch.backends.vulkan.test.op_tests.utils.codegen import VkTestSuite


# Prime numbers dim sizes for testing
XL = 113
L = 89
M2 = 41
M1 = 37
M = 29
S2 = 11
S1 = 7
S = 5
XS = 3


def get_binary_elementwise_inputs():
    return VkTestSuite(
        [
            ((M1, M2), (M1, M2)),
            ((M1, M2), (M1, 1), 2.0),
            ((M1, M2), (1, M2)),
            ((S, S1, S2), (S, S1, S2)),
            ((S, S1, S2), (S, S1, 1), 2.0),
            ((S, S1, S2), (S, 1, S2), 2.0),
        ]
    )


def get_mm_inputs():
    test_suite = VkTestSuite(
        [
            ((M1, L), (L, M2)),
            ((S1, S2), (S2, M)),
        ],
    )
    test_suite.prepacked_args = ["mat2"]
    return test_suite


def get_pool2d_inputs():
    test_suite = VkTestSuite(
        [
            ((S, M1, M2), [2, 2], [1, 1], [0, 0], [1, 1]),
        ]
    )
    test_suite.supports["layouts"] = ["api::GPUMemoryLayout::TENSOR_CHANNELS_PACKED"]
    return test_suite


test_suites = {
    "aten.add.Tensor": get_binary_elementwise_inputs(),
    "aten.sub.Tensor": get_binary_elementwise_inputs(),
    "aten.div.Tensor": get_binary_elementwise_inputs(),
    "aten.mul.Tensor": get_binary_elementwise_inputs(),
    "aten.mm.default": get_mm_inputs(),
    "aten.max_pool2d_with_indices.default": get_pool2d_inputs(),
}

prepacked_args = {"aten.mm.default": {"mat2"}}

support_exceptions = {
    "aten.max_pool2d_with_indices.default": {
        "layouts": ["api::GPUMemoryLayout::TENSOR_CHANNELS_PACKED"]
    },
}
