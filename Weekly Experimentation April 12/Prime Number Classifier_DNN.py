import torch
import torch.nn as nn
import numpy as np
from sklearn.model_selection import train_test_split


# ==========================================
# 1. 生成資料集 (Dataset Generation)
# ==========================================
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0: return False
    return True


NUM_BITS = 10
numbers = np.arange(2, 2 ** NUM_BITS)
labels = np.array([1 if is_prime(n) else 0 for n in numbers])


# 【特徵工程】：將十進位整數轉換為二進位陣列
def encode_binary(numbers, num_bits):
    return np.array([[(n >> i) & 1 for i in range(num_bits)] for n in numbers])


X = encode_binary(numbers, NUM_BITS)
y = labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

print(f"訓練集資料筆數: {X_train.shape[0]}")
print(f"測試集資料筆數: {X_test.shape[0]}\n")


# ==========================================
# 2. 建立 Deep Neural Network 模型
# ==========================================
class PrimeNet(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        # 使用 nn.Sequential 串接兩層隱藏層與非線性啟動函數 ReLU
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)


model = PrimeNet(input_size=NUM_BITS)

# 改用 Adam 優化器加速收斂
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

# ==========================================
# 3. 訓練迴圈
# ==========================================
num_epochs = 2000

for epoch in range(num_epochs):
    y_predicted = model(X_train)
    loss = criterion(y_predicted, y_train)

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    if (epoch + 1) % 200 == 0:
        print(f'Epoch: {epoch + 1:4d}, Training Loss: {loss.item():.4f}')

# ==========================================
# 4. 模型評估
# ==========================================
with torch.no_grad():
    train_pred = (model(X_train) >= 0.5).float()
    train_acc = train_pred.eq(y_train).sum() / float(y_train.shape[0])

    test_pred = (model(X_test) >= 0.5).float()
    test_acc = test_pred.eq(y_test).sum() / float(y_test.shape[0])

    print(f'\n[結果揭曉]')
    print(f'訓練集準確率 (背誦能力): {train_acc.item() * 100:.2f}%')
    print(f'測試集準確率 (泛化能力): {test_acc.item() * 100:.2f}%')