import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# 從我們自訂的 model.py 檔案中導入 DeepAE 類別
from model import DeepAE


def train_model(model, train_loader, device, epochs=15, lr=0.001):
    """負責訓練模型的函式"""
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    print("--- 開始訓練 Deep Auto-encoder ---")
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for images, _ in train_loader:
            images = images.view(-1, 28 * 28).to(device)

            _, outputs = model(images)
            loss = criterion(outputs, images)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {total_loss / len(train_loader):.4f}')
    return model


def visualize_latent_space(model, device):
    """負責在 2D 潛在空間取樣並生成圖片的函式"""
    model.eval()
    n = 15  # 15x15 的網格
    digit_size = 28
    figure = np.zeros((digit_size * n, digit_size * n))

    # 設定潛在空間的取樣範圍 (可依據你的訓練結果微調範圍)
    grid_x = np.linspace(-30, 30, n)
    grid_y = np.linspace(20, -20, n)

    print("正在生成潛在空間連續漸變圖...")
    with torch.no_grad():
        for i, yi in enumerate(grid_y):
            for j, xi in enumerate(grid_x):
                z_sample = torch.tensor([[xi, yi]], dtype=torch.float32).to(device)

                # 只有用到 decoder 部分來無中生有
                decoded_img = model.decoder(z_sample)
                digit = decoded_img.view(digit_size, digit_size).cpu().numpy()

                figure[i * digit_size: (i + 1) * digit_size,
                j * digit_size: (j + 1) * digit_size] = digit

    plt.figure(figsize=(10, 10))
    plt.imshow(figure, cmap='Greys_r')
    plt.title("Continuous Variation in 2D Latent Space")
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # 1. 基礎設定
    BATCH_SIZE = 128
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用運算裝置: {device}")

    """
    # 2. 準備資料_手寫數字資料集
    transform = transforms.Compose([transforms.ToTensor()])
    train_dataset = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    """

    # 2. 準備資料 (將原本的 MNIST 替換成 FashionMNIST)
    transform = transforms.Compose([transforms.ToTensor()])

    # 這裡改成 torchvision.datasets.FashionMNIST
    train_dataset = torchvision.datasets.FashionMNIST(root='./data', train=True, transform=transform, download=True)
    test_dataset = torchvision.datasets.FashionMNIST(root='./data', train=False, transform=transform, download=True)

    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=10000, shuffle=False)

    # 3. 實例化導入的模型
    deep_model = DeepAE().to(device)

    # 4. 執行訓練
    deep_model = train_model(deep_model, train_loader, device)

    # 5. 視覺化潛在空間
    visualize_latent_space(deep_model, device)