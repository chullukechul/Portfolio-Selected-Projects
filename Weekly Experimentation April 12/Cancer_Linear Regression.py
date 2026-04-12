import torch
import torch.nn as nn
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ==========================================
# 1. 資料預處理
# ==========================================
data = load_breast_cancer()
X, y = data.data, data.target

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)


# ==========================================
# 2. 建立 Linear Regression 模型 (關鍵改動 1)
# ==========================================
class LinearRegressionModel(nn.Module):
    def __init__(self, n_features):
        # 使用現代 Python 3 語法
        super().__init__()
        self.linear = nn.Linear(n_features, 1)

    def forward(self, x):
        # 【拔除 Sigmoid】：直接回傳線性組合結果
        y_predicted = self.linear(x)
        return y_predicted


n_samples, n_features = X_train.shape
model = LinearRegressionModel(n_features)

# ==========================================
# 3. 定義損失函數與優化器 (關鍵改動 2)
# ==========================================
# 先用 0.01 觀察收斂，之後你可以手動改成 50.0 體驗真正的梯度爆炸
learning_rate = 0.05

# 【改用 MSELoss】：線性迴歸的標準損失函數
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# ==========================================
# 4. 訓練迴圈
# ==========================================
num_epochs = 1000

for epoch in range(num_epochs):
    y_predicted = model(X_train)
    loss = criterion(y_predicted, y_train)

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch: {epoch + 1}, Loss: {loss.item():.4f}')

# ==========================================
# 5. 模型評估 (關鍵改動 3)
# ==========================================
with torch.no_grad():
    y_predicted = model(X_test)

    # 【修改決策邊界】：輸出不再是 0~1，而是任意實數。強行劃定 >= 0.5 為類別 1
    y_predicted_cls = (y_predicted >= 0.5).float()

    accuracy = y_predicted_cls.eq(y_test).sum() / float(y_test.shape[0])
    print(f'\nTest Accuracy: {accuracy.item():.4f}')