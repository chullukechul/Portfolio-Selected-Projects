import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.semi_supervised import LabelSpreading
from sklearn.svm import SVC

# ==========================================
# 1. 生成資料與環境設定
# ==========================================
X_np, y_np = make_moons(n_samples=300, noise=0.15, random_state=42)

# 一樣刻意製造標籤匱乏：挑選 6 筆作為有標籤資料
idx_class_0 = np.where(y_np == 0)[0][:3]
idx_class_1 = np.where(y_np == 1)[0][:3]
labeled_idx = np.concatenate([idx_class_0, idx_class_1])

X_labeled = X_np[labeled_idx]
y_labeled = y_np[labeled_idx]

# 準備 Label Propagation 的專用標籤格式
# 規則：有標籤的點填入真實數字 (0 或 1)，無標籤的點全部標記為 -1
y_semi = np.copy(y_np)
unlabeled_idx = np.setdiff1d(np.arange(len(X_np)), labeled_idx)
y_semi[unlabeled_idx] = -1

# ==========================================
# 2. 定義模型與訓練
# ==========================================
print("--- 訓練 Model A: 純監督式 SVM (僅用 6 筆資料) ---")
# 這裡用 SVM (支援向量機) 當作對照組，模擬傳統演算法在資料極少時的掙扎
model_baseline = SVC(kernel='rbf', gamma=2, C=1)
model_baseline.fit(X_labeled, y_labeled)

print("--- 訓練 Model B: 半監督式 Label Spreading ---")
# 使用 LabelSpreading，kernel='knn' 代表用 K-Nearest Neighbors 建構圖
# n_neighbors=7 表示每個點會跟最近的 7 個點連線，墨水就順著這些線流動
model_label_spread = LabelSpreading(kernel='knn', n_neighbors=7)
model_label_spread.fit(X_np, y_semi)


# ==========================================
# 3. 視覺化決策邊界
# ==========================================
def plot_decision_boundary(model, ax, title, is_semi=False):
    x_min, x_max = X_np[:, 0].min() - 0.5, X_np[:, 0].max() + 0.5
    y_min, y_max = X_np[:, 1].min() - 0.5, X_np[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))

    # 預測網格上的每一個點
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 畫出底色區塊
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)

    # 畫出真實分佈 (淺色)
    ax.scatter(X_np[:, 0], X_np[:, 1], c=y_np, cmap=plt.cm.coolwarm, s=20, alpha=0.2, edgecolors='none')

    # 畫出那 6 筆神聖的有標籤資料 (大顆的星星)
    ax.scatter(X_labeled[:, 0], X_labeled[:, 1], c=y_labeled, cmap=plt.cm.coolwarm, s=200, marker='*',
               edgecolors='black', linewidth=1.5)

    ax.set_title(title)
    ax.set_xticks(())
    ax.set_yticks(())


plt.figure(figsize=(12, 5))

ax1 = plt.subplot(1, 2, 1)
plot_decision_boundary(model_baseline, ax1, "Model A: Supervised SVM (6 Labeled Data)")

ax2 = plt.subplot(1, 2, 2)
plot_decision_boundary(model_label_spread, ax2, "Model B: Label Spreading (KNN Graph)")

plt.tight_layout()
plt.savefig('Label_Propagation_Result.png', dpi=300)
plt.show()