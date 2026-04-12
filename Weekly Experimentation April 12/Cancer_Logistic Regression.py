import torch
import torch.nn as nn
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ==========================================
# 1. 資料預處理 (Data Preprocessing)
# ==========================================
# 載入資料
data = load_breast_cancer()
X, y = data.data, data.target

# 特徵標準化 (Standardization) - 極度重要
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 切割訓練集與測試集 (80% 訓練, 20% 測試)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 將 Numpy Array 轉換為 PyTorch 的 Tensor格式
X_train = torch.tensor(X_train, dtype=torch.float32)
# 注意：y 需要轉換維度，從 (N,) 變成 (N, 1)，以對齊模型輸出的維度
y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)


# ==========================================
# 2. 建立 Logistic Regression 模型
# ==========================================
class LogisticRegression(nn.Module):
    def __init__(self, n_features):
        super().__init__()
        # nn.Linear 封裝了權重 W 和偏差 b: f = Wx + b
        self.linear = nn.Linear(n_features, 1)

    def forward(self, x):
        # 加上 Sigmoid 啟動函數: f(x) = \sigma(Wx + b)
        y_predicted = torch.sigmoid(self.linear(x))
        return y_predicted


# 實例化模型 (輸入特徵數為 30)
n_samples, n_features = X_train.shape
model = LogisticRegression(n_features)

# ==========================================
# 3. 定義損失函數與優化器
# ==========================================
learning_rate = 50000
# 使用 Binary Cross Entropy Loss
criterion = nn.BCELoss()
# 使用隨機梯度下降 (SGD)
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# ==========================================
# 4. 撰寫訓練迴圈 (Training Loop)
# ==========================================
num_epochs = 1000

for epoch in range(num_epochs):
    # Step 1: Forward pass (前向傳播)
    y_predicted = model(X_train)

    # Step 2: Compute Loss (計算損失)
    loss = criterion(y_predicted, y_train)

    # Step 3: Backward pass (反向傳播，計算梯度)
    loss.backward()

    # Step 4: Update weights (更新權重 W 與 b)
    optimizer.step()

    # Step 5: Zero gradients (清空梯度，避免 PyTorch 預設的梯度累加)
    optimizer.zero_grad()

    # 每 100 個 epoch 印出一次 Loss，觀察收斂狀況
    if (epoch + 1) % 100 == 0:
        print(f'Epoch: {epoch + 1}, Loss: {loss.item():.4f}')

# ==========================================
# 5. 模型評估 (Evaluation)
# ==========================================
# 評估階段不需要計算梯度，使用 torch.no_grad() 節省記憶體與算力
with torch.no_grad():
    y_predicted = model(X_test)
    # 將機率值四捨五入轉換為 0 或 1 的類別標籤
    y_predicted_cls = y_predicted.round()
    # 計算準確率
    accuracy = y_predicted_cls.eq(y_test).sum() / float(y_test.shape[0])
    print(f'\nTest Accuracy: {accuracy.item():.4f}')