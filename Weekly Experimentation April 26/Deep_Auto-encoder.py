import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# 1. 基本設定與資料載入
EPOCHS = 15  # 為了看出明顯分群，Epoch 稍微調高一點
BATCH_SIZE = 128
LR = 0.001
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([transforms.ToTensor()])
train_dataset = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)
test_dataset = torchvision.datasets.MNIST(root='./data', train=False, transform=transform, download=True)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)
# 測試集不用 shuffle，且 Batch Size 設為全部，方便一次畫圖
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=10000, shuffle=False)


# ==========================================
# 2. 定義模型結構 (對照圖片)
# ==========================================

# 模型 A：淺層自動編碼器 (784 -> 2 -> 784)
class ShallowAE(nn.Module):
    def __init__(self):
        super(ShallowAE, self).__init__()
        self.encoder = nn.Linear(28 * 28, 2)
        self.decoder = nn.Sequential(
            nn.Linear(2, 28 * 28),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded  # 回傳 encoded 以便畫圖


# 模型 B：深層自動編碼器 (784 -> 1000 -> 500 -> 250 -> 2 -> 250 -> 500 -> 1000 -> 784)
class DeepAE(nn.Module):
    def __init__(self):
        super(DeepAE, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 1000), nn.ReLU(),
            nn.Linear(1000, 500), nn.ReLU(),
            nn.Linear(500, 250), nn.ReLU(),
            nn.Linear(250, 2)
        )
        self.decoder = nn.Sequential(
            nn.Linear(2, 250), nn.ReLU(),
            nn.Linear(250, 500), nn.ReLU(),
            nn.Linear(500, 1000), nn.ReLU(),
            nn.Linear(1000, 28 * 28),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded


# ==========================================
# 3. 定義訓練與可視化函數
# ==========================================

def train_and_visualize(model, title):
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    criterion = nn.MSELoss()

    print(f"--- 開始訓練: {title} ---")
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        for images, _ in train_loader:
            images = images.view(-1, 28 * 28).to(device)

            encoded, outputs = model(images)
            loss = criterion(outputs, images)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f'Epoch [{epoch + 1}/{EPOCHS}], Loss: {total_loss / len(train_loader):.4f}')

    # --- 開始繪製二維潛在空間 ---
    model.eval()
    with torch.no_grad():
        # 拿測試集的 10000 張圖片來畫圖
        test_images, test_labels = next(iter(test_loader))
        test_images = test_images.view(-1, 28 * 28).to(device)

        # 取得降維後的 2D 特徵
        encoded_features, _ = model(test_images)
        encoded_features = encoded_features.cpu().numpy()
        test_labels = test_labels.numpy()

    # 繪製散佈圖
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(encoded_features[:, 0], encoded_features[:, 1], c=test_labels, cmap='tab10', alpha=0.6, s=10)
    plt.colorbar(scatter, ticks=range(10))
    plt.title(f"Latent Space of {title}")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.grid(True)
    plt.show()


# ==========================================
# 4. 執行實驗
# ==========================================

# 實驗 1：訓練淺層網路並畫圖
shallow_model = ShallowAE()
train_and_visualize(shallow_model, "Shallow Auto-encoder (784->2->784)")

# 實驗 2：訓練深層網路並畫圖
deep_model = DeepAE()
train_and_visualize(deep_model, "Deep Auto-encoder (Multi-layer)")