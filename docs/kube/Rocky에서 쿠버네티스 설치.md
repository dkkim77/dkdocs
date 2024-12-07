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
  * [설정](#2-6-configuration)
* [Kubernetes 설치](#install-kubernetes)

----------------------------------------------------

## Prerequisite

- 방화벽 및 리눅스 보안 프로그램 종료 (보안 프로그램이 쿠버 실행을 차단하여 정상적으로 작동하지 않음을 미연에 방지)
- 메모리 스왑 종료 (idle한 자원을 활용하기 위한 방법이지만 ,쿠버에선 정상작동 안될 가능성이 있어서 꺼놓음)
- 도메인 및 라우팅 설정 ( node끼리 통신하기 위해서 서로 알고있어야하며 iptable 라우팅 설정을 따르도록 해야함)
- 쿠버네티스 repository 추가 (yum으로 쿠버네티스 파일을 다운로드받을 때, 해당 파일을 들고 있는 저장소를 추가해줌)
- yum update (yum의 정상동작을 위해 update)
```bash
# hostnamectl set-hostname uncmaster
# swapoff -a && sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
# setenforce 0``
# sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/sysconfig/selinux
# systemctl disable firewalld
# systemctl stop firewalld
```

## CRI Runtime

### 2.1 download 
   https://github.com/containerd/containerd/releases   
### 2.2 Extract tar file
   ``# tar Cxzvf /usr/local containerd-1.6.2-linux-amd64.tar.gz``
### 2.3 Start containerd
   - containerd.service file 다운로드 : 
     https://raw.githubusercontent.com/containerd/containerd/main/containerd.service 를
     /usr/local/lib/systemd/system/containerd.service 로 다운로드.
     ```bash
     # systemctl daemon-reload
     # systemctl enable --now containerd
     ```   
### 2.4 Install runc
   -  https://github.com/opencontainers/runc/releases 다운로드  /usr/local/sbin/runc 에 설치
      ``# install -m 755 runc.amd64 /usr/local/sbin/runc``   
### 2.5 Install CNI 
   - https://github.com/containernetworking/plugins/releases 다운로드
     ```bash
     # mkdir -p /opt/cni/bin
     # tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.1.1.tgz
     ```     
### 2.6 Configuration 
    ```bash
    # containerd config default > /etc/containerd/config.toml
    # vi /etc/containerd/config.toml
         SystemdCgroup = true  <-- false 에서 true
    # systemctl restart containerd
    ```    
## Install Kubernetes
### 3.1 쿠버네티스 yum repo 추가
  ``# cat <<EOF | tee /etc/yum.repos.d/kubernetes.repo``
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF
### 3.2 설치
  # yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
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
   ``# kubeadm init --apiserver-advertise-address 192.168.219.212 --pod-network-cidr=192.168.219.0/24 --cri-socket /run/containerd/containerd.sock``
   - 결과 : kubeadm join 192.168.219.212:6443 --token le7rqm.vtgjyt3tuzz5qj2m --discovery-token-ca-cert-hash sha256:b10887df40585e20d2c9cd438d16f54262e87fb1e5306c10940fc069259b2fa4 
   /etc/sysctl.conf를 열어 net.ipv4.ip_forward=1행의 주석을 제거
   ```bash
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

