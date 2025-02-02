# 環境構築

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y install gcc-12
sudo ln -nfs /usr/bin/gcc-12 /usr/bin/gcc
sudo chmod 777 NVIDIA-Linux-x86_64-550.127.05.run
sudo ./NVIDIA-Linux-x86_64-550.127.05.run
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install -y cuda-toolkit-11-8
sudo apt-get install docker.io
curl https://get.docker.com | sh && sudo systemctl --now enable docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
          sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
          sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
sudo curl -L "https://github.com/docker/compose/releases/download/v2.0.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose 
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

`git clone https://gitlab.com/nvidia/container-images/cuda.git`

### build.sh
```
-        run_cmd docker buildx build --pull ${LOAD_ARG} ${PUSH_ARG} ${PLATFORM_ARG} \
+        run_cmd docker build ${LOAD_ARG} ${PUSH_ARG} ${PLATFORM_ARG} \
             -t "${IMAGE_NAME}:${CUDA_VERSION}-base-${OS}${OS_VERSION}${IMAGE_SUFFIX:+-${IMAGE_SUFFIX}}" \
             "${BASE_PATH}/${OS_PATH_NAME}/base"
 
-        run_cmd docker buildx build --pull ${LOAD_ARG} ${PUSH_ARG} ${PLATFORM_ARG} \
+        run_cmd docker build ${LOAD_ARG} ${PUSH_ARG} ${PLATFORM_ARG} \
             -t "${IMAGE_NAME}:${CUDA_VERSION}-runtime-${OS}${OS_VERSION}${IMAGE_SUFFIX:+-${IMAGE_SUFFIX}}" \
             --build-arg "IMAGE_NAME=${IMAGE_NAME}" \
             "${BASE_PATH}/${OS_PATH_NAME}/runtime"
 
-        run_cmd docker buildx build --pull ${LOAD_ARG} ${PUSH_ARG} ${PLATFORM_ARG} \
+        run_cmd docker build ${LOAD_ARG} ${PUSH_ARG} ${PLATFORM_ARG} \
             -t "${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${OS_VERSION}${IMAGE_SUFFIX:+-${IMAGE_SUFFIX}}" \
             --build-arg "IMAGE_NAME=${IMAGE_NAME}" \
```
`cp -r dist/end-of-life/10.2 dist/`

`./build.sh -d --image-name nvidia/cuda --cuda-version 10.2 --os ubuntu --os-version 18.04 --arch x86_64 --load`

### docker-compose.yml
```
version: '3.8'

services:
  3dpose:
    image: nvidia/cuda:10.2-devel-ubuntu18.04  
    container_name: cuda10.2-container
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ./workspace:/workspace  # ローカルのworkspaceをマウント
      - ./setup.sh:/setup.sh  # setup.shをマウント
      - type: bind
        source: /tmp/.X11-unix
        target: /tmp/.X11-unix
    stdin_open: true
    tty: true
    network_mode: "host"
    user: ${USER_ID}:${GROUP_ID}
    environment:
      DISPLAY: $DISPLAY
    command: ["bash", "/setup.sh", "bash"]
```

### setup.sh
```
#!/bin/bash

exec "$@"
```
`docker-compose up --build`

`USER_ID="$(id -u)" GROUP_ID="$(id -g)" docker compose up -d`

`docker exec -it cuda10.2-container bash`

`docker exec -it -u root cuda10.2-container bash`

### bf
```
docker run --gpus all --name bevformer2  --shm-size=2gb --net=host -v /path/to/data:/workspace/data -it nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04 bash
docker exec -i -t bevformer2 bash
export DISPLAY=":1"

apt-get update
apt -y install wget
apt -y install git
apt -y install libopencv-dev

mkdir -p /home/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /home/miniconda3/miniconda.sh
bash /home/miniconda3/miniconda.sh -b -u -p /home/miniconda3/

/home/miniconda3/bin/conda init bash
bash

conda create -n bevf python=3.8 -y
conda activate bevf

pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html

git clone https://github.com/fundamentalvision/BEVFormer.git /workspace/bevformer
ln -s /workspace/data/ /workspace/bevformer/
conda install -c omgarcia gcc-6
pip install mmcv-full==1.4.0
pip install mmdet==2.14.0
pip install mmsegmentation==0.14.1

pip uninstall opencv-python
pip install opencv-python-headless

git clone https://github.com/open-mmlab/mmdetection3d.git
cd mmdetection3d
git checkout v0.17.1
pip install -r requirements/runtime.txt
python setup.py install

python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

pip install einops fvcore seaborn iopath==0.1.9 timm==0.6.13 typing-extensions==4.5.0 pylint ipython==8.12 numpy==1.19.5 matplotlib==3.5.2 numba==0.48.0 pandas==1.4.4 scikit-image==0.19.3 setuptools==59.5.0

cd /workspace/bevformer
mkdir ckpts
cd ckpts
wget https://github.com/zhiqi-li/storage/releases/download/v1.0/bevformer_tiny_epoch_24.pth
./tools/dist_test.sh ./projects/configs/bevformer/bevformer_tiny.py ./ckpts/bevformer_tiny_epoch_24.pth 1
```
