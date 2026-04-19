import torch
import torch.nn as nn


class FatNetwork(nn.Module):
    def __init__(self):
        super(FatNetwork, self).__init__()
        # 將 28x28 的二維圖片攤平成 784 的一維向量
        self.flatten = nn.Flatten()

        # 單一且極寬的隱藏層 (W = 126)
        self.hidden_layer = nn.Linear(in_features=784, out_features=126)

        # 激活函數 (使用常用的 ReLU)
        self.relu = nn.ReLU()

        # 輸出層 (10 個分類)
        self.output_layer = nn.Linear(in_features=126, out_features=10)

    def forward(self, x):
        x = self.flatten(x)
        x = self.hidden_layer(x)
        x = self.relu(x)
        logits = self.output_layer(x)
        return logits


# 實例化模型
model_a = FatNetwork()


# 驗證總參數量
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


print(f"Model A (Fat Network) 架構:\n{model_a}")
print(f"\n總參數量: {count_parameters(model_a)}")