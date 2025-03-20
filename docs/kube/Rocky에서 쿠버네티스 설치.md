<h1>쿠버네티스 환경 구축</h1>

----------------------------------------------------

## 목 차
* [사전 준비](#prerequisite)
* [CRI Runtime](#cri-runtime)
  * [다운로드](#2-1-download)
  * [압축풀기](#2-2-extract-tar-file)
  * [containerd 시작](#2-3-start-containerd)
  * [runc 설치](#2-4-install-runc)
  * [CNI 설치](#2-5-install-cni)
* [Kubernetes 설치](#install-kubernetes)

----------------------------------------------------

## Prerequisite

- 모든 노드의 ntp 동기화
- 모든 노드가 2GB 메모리, 2 CPU 이상인지 확인
- 메모리 스왑 off

```bash
    # nproc (코어)
    # free -h (메모리)
    # ifconfig -a (MAC)
    # systemctl disable firewalld
    # systemctl stop firewalld
    # swapon -show
    # swapoff -a
    # grubby --update-kernel ALL --args selinux=0
    # sestatus
```

## CRI Runtime

### 2.1 download 
   - wget https://github.com/containerd/containerd/releases/download/v1.7.24/containerd-1.7.24-linux-amd64.tar.gz
   - docker 가 설치되면 containerd 가 자동 설치되므로 별도 설치 필요없이 아래 설정을 적용 후 restart 하면 됨 
   - Docker version 27.3.1 설치함 => containerd containerd.io 1.7.24 설치됨  
   ```bash
	    # containerd config default > /etc/containerd/config.toml
	    # vi /etc/containerd/config.toml
	         SystemdCgroup = true  <-- false 에서 true
	    # systemctl restart containerd
   ```     
   
### 2.2 Extract tar file
   ``# tar Cxzvf /usr/local containerd-1.7.24-linux-amd64.tar.gz``
   
### 2.3 Start containerd 
   - containerd.service file 다운로드 : 
     https://raw.githubusercontent.com/containerd/containerd/main/containerd.service 를
     /usr/local/lib/systemd/system/containerd.service 로 다운로드.
     ```bash
     # systemctl daemon-reload
     # systemctl enable --now containerd
     ```
        
### 2.4 Install runc (필요한가???)
   -  https://github.com/opencontainers/runc/releases 다운로드  
   -  /usr/local/sbin/runc 에 설치
      ``# install -m 755 runc.amd64 /usr/local/sbin/runc``   
      
### 2.5 Install CNI (필요한가???)
   - https://github.com/containernetworking/plugins/releases 다운로드
     ```bash
     # mkdir -p /opt/cni/bin
     # tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.1.1.tgz
     ```     
  
## Install Kubernetes

### 3.1 쿠버네티스 yum repo 추가

```bash
# cat <<EOF | tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF
```

### 3.2 설치
``# yum install -y kubelet kubeadm kubectl  --disableexcludes=kubernetes``
### 3.3 kubeadm 실행 전 kubelet 서비스 시작 
``# systemctl enable --now kubelet``
### 3.4 kubelet cgroup driver 설정
  - In v1.22 and later, if the user does not set the cgroupDriver field under KubeletConfiguration, kubeadm defaults it to systemd.
#### 3.4.1 브릿지 설정
	- modules-load.d/k8s.conf
        ```bash
	    # cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
		br_netfilter
		EOF
        ```
	- sysctl.d/k8s.conf
        ```bash
	    # cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
		net.bridge.bridge-nf-call-ip6tables = 1
		net.bridge.bridge-nf-call-iptables = 1
		EOF
	    # sudo sysctl --system
        ```
### 3.5 클러스터 생성
```bash
# kubeadm init --apiserver-advertise-address 192.168.219.212 --pod-network-cidr=192.168.219.0/24 --cri-socket /run/containerd/containerd.sock``
   결과 : kubeadm join 192.168.219.212:6443 --token le7rqm.vtgjyt3tuzz5qj2m --discovery-token-ca-cert-hash sha256:b10887df40585e20d2c9cd438d16f54262e87fb1e5306c10940fc069259b2fa4 
   /etc/sysctl.conf를 열어 net.ipv4.ip_forward=1행의 주석을 제거
        # vi /var/lib/kubelet/kubeadm-flags.env
	KUBELET_KUBEADM_ARGS="--container-runtime-endpoint=unix:///var/run/containerd/containerd.sock 
			--pod-infra-container-image=registry.k8s.io/pause:3.9 
			--cgroup-driver=systemd"
```
### 3.6 CNI (Pod network) add-on 설치
  - CNI 가 설치된 후에 CoreDNS 가 시작된다. 
  - Calico 설치
  ```bash
	# curl -O https://calico-v3-25.netlify.app/archive/v3.25/manifests/calico.yaml
	# vi calico.yaml
	  CALICO_IPV4POOL_CIDR 를 찾아서 각주 해제. kubeadm init 시 사용한 cidr 로 변경.(- name: FELIX_WIREGUARDMTU 와 같은 indent 로 조정)
  ```
### 3.7 재시작

