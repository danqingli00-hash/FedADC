########################################################################################
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
import torchvision.models as models


########################################################################################
class NetMnist1(torch.nn.Module):
    def __init__(self):
        super(NetMnist1, self).__init__()
        self.linear1 = torch.nn.Linear(784, 512)
        self.linear2 = torch.nn.Linear(512, 256)
        self.linear3 = torch.nn.Linear(256, 128)
        self.linear4 = torch.nn.Linear(128, 64)
        self.linear5 = torch.nn.Linear(64, 10)

    def forward(self, x):
        x = x.view(-1, 784)
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = F.relu(self.linear3(x))
        feature = F.relu(self.linear4(x))
        x = self.linear5(feature)
        return x, feature


########################################################################################
########################################################################################
class ConvBlock(nn.Module):
    def __init__(self, ks, ch_in, ch_out):
        super(ConvBlock, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size=ks, stride=1, padding=1, bias=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(ch_out, ch_out, kernel_size=ks, stride=1, padding=1, bias=True),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.conv(x)


class NetMnist2(nn.Module):
    def __init__(self, kernel_size, in_ch):
        super(NetMnist2, self).__init__()
        feature_list = [16, 32, 64, 128, 256]

        self.conv1 = ConvBlock(kernel_size, in_ch, feature_list[0])
        self.conv5 = ConvBlock(kernel_size, feature_list[0], feature_list[4])

        self.fcn1 = nn.Linear(feature_list[4] * 28 * 28, 1024)
        self.fcn2 = nn.ReLU()
        self.fcn3 = nn.Linear(1024, 64)
        self.fcn4 = nn.ReLU()
        self.fcn5 = nn.Linear(64, 10)

    def forward(self, x):
        x1 = self.conv1(x)
        x5 = self.conv5(x1)
        x5 = x5.view(x5.size()[0], -1)

        x5 = self.fcn1(x5)
        x5 = self.fcn2(x5)
        x5 = self.fcn3(x5)
        x5 = self.fcn4(x5)
        out = self.fcn5(x5)

        return out, x5


class NetMnist3(torch.nn.Module):
    def __init__(self):
        super(NetMnist3, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.pooling = torch.nn.MaxPool2d(2)
        self.fc1 = torch.nn.Linear(320, 64)
        self.fc2 = torch.nn.Linear(64, 10)

    def forward(self, x):
        batch_size = x.size(0)
        x = F.relu(self.pooling(self.conv1(x)))
        x = F.relu(self.pooling(self.conv2(x)))
        x = x.view(batch_size, -1)
        feature = F.relu(self.fc1(x))
        x = self.fc2(feature)
        return x, feature


########################################################################################
class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion * planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion * planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion * planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion * planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion * planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion * planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion * planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion * planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


########################################################################################
########################################################################################
class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes):
        super(ResNet, self).__init__()
        self.in_planes = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.linear = nn.Linear(512 * block.expansion, num_classes)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        feature = out.view(out.size(0), -1)
        out = self.linear(feature)
        return out, feature


class ResNetClassifier(nn.Module):
    def __init__(self, typeIdx, num_classes):
        super(ResNetClassifier, self).__init__()
        ###########################################################
        if typeIdx == 1:
            self.resnet = models.resnet34(pretrained=True)
        elif typeIdx == 2:
            self.resnet = models.resnet50(pretrained=True)
        elif typeIdx == 3:
            self.resnet = models.resnet101(pretrained=True)
        ###########################################################
        num_features = None
        if typeIdx == 1:
            num_features = 512
        elif typeIdx == 2:
            num_features = 2048
        elif typeIdx == 3:
            num_features = 2048
        # num_features = self.resnet.fc.in_features
        ###########################################################
        self.fcn4 = nn.ReLU()
        self.fcn5 = nn.Linear(num_features, 1024)

        self.resnet.fc = nn.Linear(1024, num_classes)

    def _forward_impl(self, x: Tensor):
        # See note [TorchScript super()]
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = self.resnet.relu(x)
        x = self.resnet.maxpool(x)

        x = self.resnet.layer1(x)
        x = self.resnet.layer2(x)
        x = self.resnet.layer3(x)
        x = self.resnet.layer4(x)

        x = self.resnet.avgpool(x)
        feature = torch.flatten(x, 1)

        x5 = self.fcn4(feature)
        feature = self.fcn5(x5)

        x = self.resnet.fc(feature)

        return x, feature

    def forward(self, x: Tensor):
        return self._forward_impl(x)


def ResNet18(num_classes):
    return ResNet(BasicBlock, [2, 2, 2, 2], num_classes)


def ResNet34(num_classes):
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes)


def ResNet50(num_classes):
    return ResNet(BasicBlock, [3, 4, 12, 3], num_classes)


def ResNet101(num_classes):
    return ResNet(Bottleneck, [3, 4, 23, 3], num_classes)


def ResNet152(num_classes):
    return ResNet(Bottleneck, [3, 8, 36, 3], num_classes)


########################################################################################
class Generator(nn.Module):
    def __init__(self, channelNum, latentDim, imgSize):
        super(Generator, self).__init__()

        self.init_size = imgSize // 4
        self.l1 = nn.Sequential(nn.Linear(latentDim, 128 * self.init_size ** 2))

        self.conv_blocks0 = nn.Sequential(
            nn.BatchNorm2d(128),
        )
        self.conv_blocks1 = nn.Sequential(
            nn.Conv2d(128, 128, 3, stride=1, padding=1),
            nn.BatchNorm2d(128, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
        )
        self.conv_blocks2 = nn.Sequential(
            nn.Conv2d(128, 64, 3, stride=1, padding=1),
            nn.BatchNorm2d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, channelNum, 3, stride=1, padding=1),
            nn.Tanh(),
            nn.BatchNorm2d(channelNum, affine=False)
        )

    def forward(self, z):
        out = self.l1(z)
        out = out.view(out.shape[0], 128, self.init_size, self.init_size)
        img = self.conv_blocks0(out)
        img = nn.functional.interpolate(img, scale_factor=2)
        img = self.conv_blocks1(img)
        img = nn.functional.interpolate(img, scale_factor=2)
        img = self.conv_blocks2(img)
        return img
########################################################################################
