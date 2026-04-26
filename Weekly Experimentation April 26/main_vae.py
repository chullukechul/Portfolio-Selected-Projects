import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# 導入我們剛剛寫好的 VAE
from model_VAE import VAE


# 定義 VAE 專用的 Loss 函數
def vae_loss_function(recon_x, x, mu, logvar):
    # 1. 重構誤差 (Reconstruction Loss)：使用 MSE，但這裡建議用 sum 把整個 Batch 加起來
    # 注意：在 VAE 中也常使用 Binary Cross Entropy (BCE) 作為重構誤差
    MSE = nn.functional.mse_loss(recon_x, x, reduction='sum')

    # 2. KL 散度 (KL Divergence Loss)：強迫潛在分佈接近 N(0, 1)
    # 數學公式推導結果：-0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    return MSE + KLD


def train_vae(model, train_loader, device, epochs=15, lr=0.001):
    optimizer = optim.Adam(model.parameters(), lr=lr)

    print("--- 開始訓練 VAE ---")
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for images, _ in train_loader:
            images = images.view(-1, 28 * 28).to(device)

            # 前向傳播
            recon_images, mu, logvar = model(images)

            # 計算 VAE Loss
            loss = vae_loss_function(recon_images, images, mu, logvar)

            # 反向傳播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        # 平均 Loss 要除以資料總筆數
        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {total_loss / len(train_loader.dataset):.4f}')
    return model


def visualize_vae_latent_space(model, device):
    """
    因為 VAE 已經把空間擠壓到了標準常態分佈 N(0, 1)
    根據統計學，大約 99.7% 的資料會落在正負 3 個標準差之內。
    所以我們的網格取樣範圍只需要設定在 [-3, 3] 即可！
    """
    model.eval()
    n = 15
    digit_size = 28
    figure = np.zeros((digit_size * n, digit_size * n))

    # 取樣範圍從 AE 的 [-30, 30] 大幅縮小為 [-3, 3]
    grid_x = np.linspace(-3, 3, n)
    grid_y = np.linspace(3, -3, n)

    print("正在生成 VAE 潛在空間連續漸變圖...")
    with torch.no_grad():
        for i, yi in enumerate(grid_y):
            for j, xi in enumerate(grid_x):
                z_sample = torch.tensor([[xi, yi]], dtype=torch.float32).to(device)

                # 直接交給 Decoder 生成
                decoded_img = model.decoder(z_sample)
                digit = decoded_img.view(digit_size, digit_size).cpu().numpy()

                figure[i * digit_size: (i + 1) * digit_size,
                j * digit_size: (j + 1) * digit_size] = digit

    plt.figure(figsize=(10, 10))
    plt.imshow(figure, cmap='Greys_r')
    plt.title("Continuous Variation in VAE Latent Space")
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    BATCH_SIZE = 128
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 繼續使用會讓標準 AE 破圖的 FashionMNIST
    transform = transforms.Compose([transforms.ToTensor()])
    train_dataset = torchvision.datasets.FashionMNIST(root='./data', train=True, transform=transform, download=True)
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    # 實例化 VAE 模型並訓練
    vae_model = VAE().to(device)
    vae_model = train_vae(vae_model, train_loader, device)

    # 視覺化
    visualize_vae_latent_space(vae_model, device)