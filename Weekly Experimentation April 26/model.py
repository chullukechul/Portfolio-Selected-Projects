import torch.nn as nn

class DeepAE(nn.Module):
    def __init__(self):
        super(DeepAE, self).__init__()
        # 編碼器：壓縮特徵至 2 維
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 1000), nn.ReLU(),
            nn.Linear(1000, 500), nn.ReLU(),
            nn.Linear(500, 250), nn.ReLU(),
            nn.Linear(250, 2)
        )
        # 解碼器：從 2 維還原回 784 維圖片
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