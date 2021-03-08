from torchvision.models import resnet
from torchvision.ops.misc import FrozenBatchNorm2d
from torchvision.models._utils import IntermediateLayerGetter


def resnet_backbone(
        backbone_name='resnet50',
        pretrained=False,
        trainable_layers=3,
        returned_layer=4
):
    """
    :param backbone_name: resnet architecture. Possible values are 'ResNet', 'resnet18', 'resnet34', 'resnet50',
             'resnet101', 'resnet152', 'resnext50_32x4d', 'resnext101_32x8d', 'wide_resnet50_2', 'wide_resnet101_2'
    :param pretrained: If True, returns a model with backbone pre-trained on Imagenet
    :param trainable_layers: number of trainable (not frozen) resnet layers starting from final block.
            Valid values are between 0 and 5, with 5 meaning all backbone layers are trainable.
    :param returned_layer: layer of the network to return.
    """
    backbone = resnet.__dict__[backbone_name](pretrained=pretrained, norm_layer=FrozenBatchNorm2d)
    assert 0 <= trainable_layers <= 5
    layers_to_train = ['layer4', 'layer3', 'layer2', 'layer1', 'conv1'][:trainable_layers]

    if trainable_layers == 5:
        layers_to_train.append('bn1')

    # freeze layers
    for name, parameter in backbone.named_parameters():
        if all([not name.startswith(layer) for layer in layers_to_train]):
            parameter.requires_grad_(False)

    assert 0 < returned_layer < 5
    return_layer = {f'layer{returned_layer}': f'layer{returned_layer}'}

    return IntermediateLayerGetter(model=backbone, return_layers=return_layer)