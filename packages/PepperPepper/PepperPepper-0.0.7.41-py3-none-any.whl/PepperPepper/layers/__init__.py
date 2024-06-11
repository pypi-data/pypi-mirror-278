# layers 模块
# 功能：包含自定义的神经网络层或模块。
# 子模块/文件：
# attention.py：实现各种注意力机制层。
# custom_layer.py：用户自定义层的示例或模板。












# # layers/__init__.py
#
# # 导入 layers 子包中的各个模块
# from . import conv_layers
# from . import pooling_layers
# from . import normalization_layers
# from . import activation_layers
#
# # 如果需要，可以直接导入这些模块中的特定层类
# from .conv_layers import Conv2D, DepthwiseConv2D
# from .pooling_layers import MaxPooling2D, AveragePooling2D
# from .normalization_layers import BatchNormalization
# from .activation_layers import ReLU, Sigmoid, Softmax
#
# # __all__ 变量定义了当使用 from layers import * 时导入哪些对象
# # 注意：通常不推荐使用 from package import *
# __all__ = [
#     'Conv2D', 'DepthwiseConv2D',
#     'MaxPooling2D', 'AveragePooling2D',
#     'BatchNormalization',
#     'ReLU', 'Sigmoid', 'Softmax',
#     # ... 其他希望用户直接访问的关键层类 ...
# ]