```
echo 'blacklist nouveau' | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
echo 'options nouveau modeset=0' | sudo tee -a /etc/modprobe.d/blacklist-nouveau.conf
sudo update-initramfs -u

sudo apt update
sudo apt -y install linux-headers-$(uname -r) build-essential dkms

sudo ubuntu-drivers autoinstall
sudo update-initramfs -u

sudo reboot

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
apt-cache policy cuda-toolkit-11-8

sudo apt install cuda-toolkit-11-8
echo 'export CUDA_HOME=/usr/local/cuda-11.8' >> ${HOME}/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:${LD_LIBRARY_PATH}' >> ${HOME}/.bashrc
echo 'export PATH=/usr/local/cuda-11.8/bin:${PATH}' >> ${HOME}/.bashrc

sudo reboot

apt-cache policy libcudnn8
sudo apt install libcudnn8=8.9.7.29-1+cuda11.8
sudo apt install libcudnn8-dev=8.9.7.29-1+cuda11.8
```

```
# 1. ダウンロードした .deb をインストール
sudo dpkg -i cudnn-local-repo-ubuntu2204-8.6.0.163_1.0-1_amd64.deb

# 2. キーファイルのコピー（信頼性確保）
sudo cp /var/cudnn-local-repo-*/cudnn-*-keyring.gpg /usr/share/keyrings/

# 3. リポジトリ更新
sudo apt update

# 4. cuDNN ライブラリと開発ヘッダをインストール
sudo apt install -y libcudnn8 libcudnn8-dev libcudnn8-samples
# cuDNN 環境変数（CUDA 11.8にインストールされている前提）
export CUDNN_ROOT=/usr/lib/x86_64-linux-gnu
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDNN_ROOT
export CPATH=$CPATH:/usr/include
# CUDA 11.8 のパス設定（必要であれば）
export PATH=/usr/local/cuda-11.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH

import torch
print(torch.backends.cudnn.enabled)       # → True
print(torch.backends.cudnn.version())     # → 8600 など
```
