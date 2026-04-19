import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# ==========================================
# 1. 從你建立的獨立檔案中導入模型
# ==========================================
# 確保檔名大小寫完全一致，且沒有附檔名 .py
from ModelA_FatNetwork import FatNetwork
from ModelB_DeepNetwork import DeepNetwork

# ==========================================
# 2. 準備資料與環境
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"目前使用的運算設備: {device}\n")

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

# 下載並載入 Fashion-MNIST
train_set = torchvision.datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
test_set = torchvision.datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=64, shuffle=False)


# ==========================================
# 3. 訓練核心邏輯 (與之前相同)
# ==========================================
def train_and_evaluate(model, name, epochs=15):
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    history = {'train_loss': [], 'test_acc': []}

    print(f"--- 開始訓練 {name} ---")
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        avg_train_loss = running_loss / len(train_loader)
        history['train_loss'].append(avg_train_loss)

        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        test_acc = 100 * correct / total
        history['test_acc'].append(test_acc)

        print(f"Epoch [{epoch + 1}/{epochs}] | Train Loss: {avg_train_loss:.4f} | Test Acc: {test_acc:.2f}%")

    return history


# ==========================================
# 4. 實例化導入的模型並執行對決
# ==========================================
model_a = FatNetwork()
model_b = DeepNetwork()

history_a = train_and_evaluate(model_a, "Model A (Fat Network)")
print("\n")
history_b = train_and_evaluate(model_b, "Model B (Deep Network)")

# 繪製圖表
epochs_range = range(1, 16)
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(epochs_range, history_a['train_loss'], label='Fat Network', marker='o')
plt.plot(epochs_range, history_b['train_loss'], label='Deep Network', marker='s')
plt.title('Training Loss (Lower is Better)')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs_range, history_a['test_acc'], label='Fat Network', marker='o')
plt.plot(epochs_range, history_b['test_acc'], label='Deep Network', marker='s')
plt.title('Test Accuracy (Higher is Better)')
plt.xlabel('Epochs')
plt.ylabel('Accuracy (%)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.tight_layout()
plt.savefig('Deep_vs_Fat_Result.png', dpi=300)
plt.show()