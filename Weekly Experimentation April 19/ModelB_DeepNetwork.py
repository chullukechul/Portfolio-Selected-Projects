import torch
import torch.nn as nn


class DeepNetwork(nn.Module):
    def __init__(self):
        super(DeepNetwork, self).__init__()
        self.flatten = nn.Flatten()

        # 4 層較窄的隱藏層 (寬度皆為 h = 93)
        self.hidden1 = nn.Linear(in_features=784, out_features=93)
        self.hidden2 = nn.Linear(in_features=93, out_features=93)
        self.hidden3 = nn.Linear(in_features=93, out_features=93)
        self.hidden4 = nn.Linear(in_features=93, out_features=93)

        # 激活函數
        self.relu = nn.ReLU()

        # 輸出層 (10 個分類)
        self.output_layer = nn.Linear(in_features=93, out_features=10)

    def forward(self, x):
        x = self.flatten(x)
        # 依序通過多層神經網路 (Deep)
        x = self.relu(self.hidden1(x))
        x = self.relu(self.hidden2(x))
        x = self.relu(self.hidden3(x))
        x = self.relu(self.hidden4(x))
        logits = self.output_layer(x)
        return logits


# 實例化模型
model_b = DeepNetwork()


# 驗證總參數量
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


print(f"Model B (Deep Network) 架構:\n{model_b}")
print(f"\n總參數量: {count_parameters(model_b)}")