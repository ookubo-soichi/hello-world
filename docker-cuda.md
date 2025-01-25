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

`USER_ID="$(id -u)" GROUP_ID="$(id -g)" docker compose up -d`

`docker exec -it cuda10.2-container bash`

`docker exec -it -u root cuda10.2-container bash`
