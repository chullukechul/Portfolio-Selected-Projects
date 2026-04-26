import torch
import torch.nn as nn


class VAE(nn.Module):
    def __init__(self):
        super(VAE, self).__init__()
        # 1. 共享的編碼器特徵萃取層
        self.encoder_shared = nn.Sequential(
            nn.Linear(28 * 28, 1000), nn.ReLU(),
            nn.Linear(1000, 500), nn.ReLU(),
            nn.Linear(500, 250), nn.ReLU()
        )

        # 2. 分岔：分別預測 2 維的平均值 (mu) 與 2 維的對數變異數 (logvar)
        self.fc_mu = nn.Linear(250, 2)
        self.fc_logvar = nn.Linear(250, 2)

        # 3. 解碼器：和之前一樣，從 2 維還原回 784 維
        self.decoder = nn.Sequential(
            nn.Linear(2, 250), nn.ReLU(),
            nn.Linear(250, 500), nn.ReLU(),
            nn.Linear(500, 1000), nn.ReLU(),
            nn.Linear(1000, 28 * 28),
            nn.Sigmoid()
        )

    def reparameterize(self, mu, logvar):
        """重新參數化技巧：z = mu + std * epsilon"""
        std = torch.exp(0.5 * logvar)  # 將 logvar 轉回標準差 std
        eps = torch.randn_like(std)  # 從標準常態分佈抽樣常態雜訊 epsilon
        return mu + eps * std  # 組合出最終的潛在座標 z

    def forward(self, x):
        # 萃取特徵
        h = self.encoder_shared(x)

        # 算出 mu 與 logvar
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)

        # 透過重新參數化取得 z (只有在訓練時加入雜訊有意義，但為求簡化，這裡一律套用)
        z = self.reparameterize(mu, logvar)

        # 解碼生成圖片
        decoded = self.decoder(z)

        # 回傳解碼圖片，以及 mu、logvar (計算 KL Loss 時需要用到)
        return decoded, mu, logvar