import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons

# ==========================================
# 1. 生成資料與環境設定
# ==========================================
# 生成雙半月形資料 (300筆)
X_np, y_np = make_moons(n_samples=300, noise=0.15, random_state=42)

# 刻意製造「標籤匱乏」：只挑選 6 筆作為有標籤資料 (Labeled)
labeled_indices = [0, 1, 2, 3, 4, 5]  # 剛好各涵蓋幾個兩類的點 (人為挑選或隨機)
# 為了確保實驗穩定，我們手動挑選 3個屬於類別0，3個屬於類別1的點
idx_class_0 = np.where(y_np == 0)[0][:3]
idx_class_1 = np.where(y_np == 1)[0][:3]
labeled_idx = np.concatenate([idx_class_0, idx_class_1])

# 剩下的 294 筆全部作為無標籤資料 (Unlabeled)
unlabeled_idx = np.setdiff1d(np.arange(len(X_np)), labeled_idx)

X_labeled = torch.FloatTensor(X_np[labeled_idx])
y_labeled = torch.LongTensor(y_np[labeled_idx])
X_unlabeled = torch.FloatTensor(X_np[unlabeled_idx])
y_true_unlabeled = torch.LongTensor(y_np[unlabeled_idx])  # 只用來畫圖對照，不參與訓練


# ==========================================
# 2. 定義神經網路 (輕量級 MLP)
# ==========================================
class SimpleMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 2)  # 輸出兩個類別的 Logits
        )

    def forward(self, x):
        return self.net(x)


# ==========================================
# 3. 訓練函數
# ==========================================
def train_model(X_train, y_train, epochs=200):
    model = SimpleMLP()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
    return model


# ==========================================
# 4. 進行實驗：純監督式 vs 半監督式
# ==========================================
print("--- 訓練 Model A: 純監督式 (僅使用 6 筆標籤資料) ---")
model_baseline = train_model(X_labeled, y_labeled, epochs=300)

print("--- 訓練 Model B: 半監督式 (Self-Training) ---")
# Step 4.1: 先用 6 筆資料訓練初始模型
model_self_train = train_model(X_labeled, y_labeled, epochs=100)

# Step 4.2: Self-Training 迭代
confidence_threshold = 0.997  # 只取信心度高於 85% 的預測作為偽標籤
X_pool = X_labeled.clone()
y_pool = y_labeled.clone()

# 迭代 3 次
for iteration in range(3):
    model_self_train.eval()
    with torch.no_grad():
        # 對無標籤資料進行預測
        logits = model_self_train(X_unlabeled)
        probs = torch.softmax(logits, dim=1)
        max_probs, pseudo_labels = torch.max(probs, dim=1)

        # 篩選高信心度的資料點
        confident_mask = max_probs > confidence_threshold
        X_confident = X_unlabeled[confident_mask]
        y_confident = pseudo_labels[confident_mask]

        print(f"迭代 {iteration + 1}: 成功為 {len(X_confident)} 筆無標籤資料貼上偽標籤。")

        # 將偽標籤資料加入訓練池中
        X_pool_new = torch.cat([X_pool, X_confident])
        y_pool_new = torch.cat([y_pool, y_confident])

    # 用擴增後的資料集重新訓練模型
    model_self_train = train_model(X_pool_new, y_pool_new, epochs=150)
    X_pool, y_pool = X_pool_new, y_pool_new


# ==========================================
# 5. 視覺化決策邊界 (Decision Boundary)
# ==========================================
def plot_decision_boundary(model, ax, title):
    x_min, x_max = X_np[:, 0].min() - 0.5, X_np[:, 0].max() + 0.5
    y_min, y_max = X_np[:, 1].min() - 0.5, X_np[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    grid_tensor = torch.FloatTensor(np.c_[xx.ravel(), yy.ravel()])

    model.eval()
    with torch.no_grad():
        preds = torch.argmax(model(grid_tensor), dim=1).numpy()
        preds = preds.reshape(xx.shape)

    ax.contourf(xx, yy, preds, alpha=0.3, cmap=plt.cm.coolwarm)

    # 畫出底層真實分佈 (淺色)
    ax.scatter(X_np[:, 0], X_np[:, 1], c=y_np, cmap=plt.cm.coolwarm, s=20, alpha=0.2, edgecolors='none')
    # 畫出那 6 筆神聖的有標籤資料 (大顆的星星)
    ax.scatter(X_labeled[:, 0], X_labeled[:, 1], c=y_labeled, cmap=plt.cm.coolwarm, s=200, marker='*',
               edgecolors='black', linewidth=1.5)

    ax.set_title(title)
    ax.set_xticks(())
    ax.set_yticks(())


plt.figure(figsize=(12, 5))
ax1 = plt.subplot(1, 2, 1)
plot_decision_boundary(model_baseline, ax1, "Model A: Supervised Only (6 Labeled Data)")

ax2 = plt.subplot(1, 2, 2)
plot_decision_boundary(model_self_train, ax2, "Model B: Semi-Supervised (Self-Training)")

plt.tight_layout()
plt.savefig('Semi_Supervised_Result.png', dpi=300)
plt.show()