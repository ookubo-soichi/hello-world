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

① Nouveau ドライバの無効化
再起動後に lsmod | grep nouveau で nouveau が無効化されたか確認するとより確実です。
ドライバ無効化後、再起動してから次のドライバインストールに進むのが理想的です（現在は再起動がその後になっています）。

② ビルドツールの準備

sudo apt update
sudo apt -y install linux-headers-$(uname -r) build-essential dkms

③ NVIDIA ドライバのインストール

sudo ubuntu-drivers autoinstall
sudo update-initramfs -u
sudo reboot

④ CUDA 11.8 のインストール

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
apt-cache policy cuda-toolkit-11-8

改善点:
    sudo apt install cuda-11-8 にすると Driver や Runtime も一括 で入り便利な場合があります。
        ただし、ドライバを別で入れたい場合（例: TensorRT 用）には cuda-toolkit-11-8 の方が安全。

⑤ 環境変数の設定

echo 'export CUDA_HOME=/usr/local/cuda-11.8' >> ${HOME}/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:${LD_LIBRARY_PATH}' >> ${HOME}/.bashrc
echo 'export PATH=/usr/local/cuda-11.8/bin:${PATH}' >> ${HOME}/.bashrc


⑥ cuDNN のインストール

apt-cache policy libcudnn8
sudo apt install libcudnn8=8.9.7.29-1+cuda11.8
sudo apt install libcudnn8-dev=8.9.7.29-1+cuda11.8

apt list -a libcudnn8 でインストール可能なバージョンの確認も可能。
バージョンがマッチしないと依存エラーになることがあるため、apt-cache policy ではなく apt list -a の方が便利な場合があります。

✅ 最終確認チェックリスト

nvidia-smi                 # GPUとドライバの確認
nvcc --version             # CUDA toolkit バージョン確認
echo $LD_LIBRARY_PATH      # ライブラリパス確認

他にも TensorRT などを入れる予定があれば、その前提に合わせて Toolkit と Driver の整合性を保つよう注意してください。必要に応じて cuda-compat-11-8 のインストールも検討できます。

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
# CUDA 11.8 のパス設定（必要であれば）
export PATH=/usr/local/cuda-11.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH

import torch
print(torch.backends.cudnn.enabled)       # → True
print(torch.backends.cudnn.version())     # → 8600 など
```

```
sudo dpkg -i nv-tensorrt-local-repo-ubuntu2204-8.6.1-cuda-11.8_1.0-1_amd64.deb
sudo cp /var/nv-tensorrt-local-repo-*/nv-tensorrt-*-keyring.gpg /usr/share/keyrings/
sudo mv /etc/apt//sources.list.d/cuda-ubuntu2204-x86_64.list /etc/apt//sources.list.d/cuda-ubuntu2204-x86_64.list.disabled
sudo apt clean
sudo apt update

sudo apt install -y   tensorrt=8.6.1.6-1+cuda11.8   libnvinfer-dev=8.6.1.6-1+cuda11.8   libnvinfer-plugin-dev=8.6.1.6-1+cuda11.8   libnvparsers-dev=8.6.1.6-1+cuda11.8   libnvonnxparsers-dev=8.6.1.6-1+cuda11.8   libnvinfer8=8.6.1.6-1+cuda11.8   libnvinfer-plugin8=8.6.1.6-1+cuda11.8   libnvinfer-vc-plugin8=8.6.1.6-1+cuda11.8   libnvinfer-headers-dev=8.6.1.6-1+cuda11.8   libnvinfer-headers-plugin-dev=8.6.1.6-1+cuda11.8   libnvinfer-lean8=8.6.1.6-1+cuda11.8   libnvinfer-dispatch8=8.6.1.6-1+cuda11.8   libnvinfer-lean-dev=8.6.1.6-1+cuda11.8   libnvinfer-dispatch-dev=8.6.1.6-1+cuda11.8   libnvinfer-vc-plugin-dev=8.6.1.6-1+cuda11.8   libnvinfer-bin=8.6.1.6-1+cuda11.8   libnvinfer-samples=8.6.1.6-1+cuda11.8

tar -xvzf TensorRT-8.6.1.6.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz

仮想環境をactivateした上で、特定のpythonバージョンにあったpipをする
pip install ./TensorRT-8.6.1.6/python/tensorrt-8.6.1-cp38-none-linux_x86_64.whl 
pip install ./TensorRT-8.6.1.6/uff/uff-0.6.9-py2.py3-none-any.whl
pip install ./TensorRT-8.6.1.6/graphsurgeon/graphsurgeon-0.4.6-py2.py3-none-any.whl
pip install ./TensorRT-8.6.1.6/onnx_graphsurgeon/onnx_graphsurgeon-0.3.12-py2.py3-none-any.whl

export TRT_ROOT=/usr/lib/x86_64-linux-gnu
export PATH=$PATH:$TRT_ROOT
export TENSORRT_DIR="$HOME/tools/TensorRT-8.6.1.6" # 解凍後のライブラリは残しておく
export LD_LIBRARY_PATH=$TENSORRT_DIR/lib:$LD_LIBRARY_PATH

import tensorrt as trt
print(trt.__version__)  # → 8.6.x であることを確認
```
