# 목차
1. jdk 설치

[docker용]
1. gitea 설치
2. jenkins 설치
3. git repository 생성 
4. springboot 프로젝트 생성
5. jenkins pipeline 생성 
6. Gitea - Jenkins Webhook 설정 
7. NEXUS 구축
<br/><br/>
	
---

# JMX 설정 
##### 자바 프로세스에 기본 JMX 설정  
java -Dcom.sun.management.jmxremote \
     -Dcom.sun.management.jmxremote.port=12345 \
     -Dcom.sun.management.jmxremote.rmi.port=12346 \
     -Dcom.sun.management.jmxremote.authenticate=true \
     -Dcom.sun.management.jmxremote.password.file=/path/to/jmxremote.password \
     -Dcom.sun.management.jmxremote.access.file=/path/to/jmxremote.access \
     -Djava.rmi.server.hostname=your_server_ip \
     -Dcom.sun.management.jmxremote.ssl=false \
     -jar your-application.jar

##### jmxremote.password 파일 예시
monitorRole    secret_password
controlRole    another_password

##### jmxremote.password 파일 예시
monitorRole    secret_password
controlRole    another_password

# OpenJDK 설치
dnf search openjdk
dnf install java-17-openjdk-devel.x86_64
java -version

# gitea 설치

dnf install git -y
wget -c https://dl.gitea.io/gitea/1.23.5/gitea-1.23.5-linux-amd64
chmod +x gitea-1.18.0-linux-amd64
mv gitea-1.18.0-linux-amd64 /usr/local/bin/gitea

Gitea 관련 디렉토리 생성
mkdir -p /var/lib/gitea
mkdir -p /etc/gitea
mkdir -p /var/log/gitea
디렉토리 권한 설정
chown -R gitea:gitea /var/lib/gitea
chown -R gitea:gitea /etc/gitea
chown -R gitea:gitea /var/log/gitea
service 파일 생성
nano /etc/systemd/system/gitea.service

방화벽 설정 
firewall-cmd --zone=public --add-port=3000/tcp --permanent
firewall-cmd --reload

systemd를 통해 Gitea 서비스 등록
systemctl daemon-reload
Gitea 서비스 시작
sudo systemctl start gitea
Gitea 서비스 자동 시작 설정
systemctl enable gitea

2. webhook 을 위해 app.ini 를 생성
windows 일 경우 도움말을 확인하여 configFile 경로를 알 수 있다.<br/>
> gitea-1.22.0-gogit-windows-4.0-amd64.exe help[enter]<br/>
해당 위치에 app.ini 를 생성한다. 
<pre><code>
[webhook]
ALLOWED_HOST_LIST=*
</pre></code>
    	
# Jenkins 설치 
##### yum 로 설치 
1. jenkins GPG 설치, yum repo 설치
rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
dnf config-manager --add-repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
dnf install jenkins -y

포트변경
vi /usr/lib/systemd/system/jenkins.service

방화벽 포트 열기
 firewall-cmd --zone=public --add-port=18081/tcp --permanent
 firewall-cmd --reload

systemctl start jenkins
systemctl enable jenkins
systemctl status jenkins => 최초비번 복사 

##### Docker 로 설치 
1. /dkdocs/docs/kube/Dockerfile-jenkins 파일로 Jenkins 설치
2. /dkdocs/
    
##### 플러그인 설치
1. maven
2. gitea plugin
3. generic webhook trigger
4. Multibranch Scan Webhook Trigger 
    
##### Credential 설정
Jenkins 관리 > Credentials
    
##### Tools 설정    
1. maven 설정 
    
##### SCM 설정
Jenkins 관리 > System > Gitea Servers
    
##### TimeZone 설정
1. global 설정 <br/>
아래처럼 Environment 에 설정을 추가한다. 
<pre><code>
$ systemctl edit jenkins[enter]<br/>
[Service]
Environment="JAVA_OPTS=-Dorg.apache.commons.jelly.tags.fmt.timeZone=Asia/SEOUL"
동작하지 않으면
Environment="JAVA_OPTS=-Duser.timezone=Asia/SEOUL"
</code></pre>
    
2. ID 별 설정<br/> 
우측상단 ID > 설정 > User Defined Time Zone 에서 설정 
	 
##### Kubernetes 로 설치 

# Jenkins pipeline 생성

1. Declarative 방식으로 생성 
<pre><code>
environment {
    ACTIVE_PROFILE = "Dev"
}

pipeline {
    
    agent any
    
    environment {
        PROJECT_NAME = "devops-test"
    }
    options {
        timestamps() 
        disableConcurrentBuilds(abortPrevious: true)
       //  skipStagesAfterUnstable()                                        // 없는게 낫다. 이후 stage 들도 모두 실패로 처리된다. 있을경우 실패하면 post.failure 수행 안됨.
        timeout(time: 1, unit: 'HOURS') 
        buildDiscarder(logRotator(daysToKeepStr: '60', numToKeepStr: '3'))  // console output을 보관할 일자, 보관 갯수 
        disableResume()                                                     // Jenkins가 다시 시작했을 경우 자동으로 시작하는 것을 방지
        // parallelsAlwaysFailFast() // Parallel 스테이지중 하나가 실패하는 경우 다른 parallel 스테이지도 멈추고 해당 Build의 상태를 실패로
    }

//    triggers {
//        upstream(upstreamProjects: 'job1,job2', threshold: hudson.model.Result.SUCCESS) 
//        cron('H */4 * * 1-5')
//    }
    // 해당 tool 을 자동 설치. tool 명은 Manage Jenkins → Tools 에 설정되어 있어야 한다 
    // ant,git,gradle,jdk, jgit, maven 을 사용 가능. dockerfile 에이전트에서 동작안하기때문에 도구가 설치된 이미지를 사용
    tools {
        maven 'maven-3.9.8'
    }
    
    stages {
        stage('Menu') {
            steps {
                script {
                    timeout(time: 60, unit: 'SECONDS') {
                 
                        def resp = input message: '입력하세요', parameters: [string(description: 'enter1', name: 'value1'), string(description: 'enter2', name: 'value2')]
                        env.ENV_VAL1 = resp['value1']
                        env.ENV_VAL2 = resp['value2']
                        echo "스크립트안에서 val1 : ${env.ENV_VAL1}"
                        echo "스크립트안에서 val2 : ${env.ENV_VAL2}"                    
                    }
                }
                echo "스크립트밖에서 val1 : ${env.ENV_VAL1}"
                echo "스크립트밖에서 val2 : ${env.ENV_VAL2}"
            }
        }
        
        stage('Sources') {
            steps {
                sh 'echo "download $PROJECT_NAME"'
                git branch: 'main', url: 'http://192.168.219.113:3000/dkkim/devops-test.git'
            }
        }     
        stage('Build') {
            // 해당 스테이지(Build)가 실행될 조건을 명시
            // and, or, not, allOf(and 처럼 동작), anyOf (or처럼 동작), 
            when {
                allOf {
                    environment name: "ACTIVE_PROFILE", value: "Dev"
                    branch 'origin'
                }
            }
            steps {
                echo 'build si-runtime'
            }
        }
        stage('Build') {
            steps {
                sh 'echo "build $PROJECT_NAME"'
                sh 'mvn -DskipTests clean package'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo "deploy $PROJECT_NAME"'
            }
        }
        stage('Restart') {
            steps {
                sh 'echo "restart $PROJECT_NAME"'
            }
        }                
    }
    post {
        always {
            sh 'echo "All steps is completed"'
        }
        failure {
            sh 'echo "Build Failed"'
            mail body: '$PROJECT_NAME build failed', subject: '$PROJECT_NAME build failed!', to: 'unchartwater@gmail.com'
        }
        success {
            sh 'echo "$PROJECT_NAME Build Succeeded"'
        }
    }
}
</code>
</pre>

2. build 성공 후 확인<br/>
$ cd /var/jenkins_home/workspace/devops-test<br/>
$ ls
    
# Gitea - Jenkins Webhook 설정     
1. singlebranch webhook 설정
- jenkins 에서 사용자 > 설정 > api token > token generate > token 명에 singlebranch-webhook 입력 
- job > 빌드를 원격으로 유발 체크 > auth token 에 api token 명 입력 
- gitea 에서 webhook 추가
<pre><code>
대상 URL : http://localhost:8080/job/devops-test/build?token=singlebranch-webhook => 403 오류 발생.
        오류 응답 : HTTP ERROR 403 No valid crumb was included in the request
        조치 내용 : {id}:{token}@{jenkins주소} 형태로 변경
                 > http://dkkim:11a581820e066ab651765be3335310a0ca@localhost:8080/job/devops-test/build?token=singlebranch-webhook
Branch Filter : stage
</pre></code>        
2. multibranch webhook 설정 
git 의 여러 branch 를 하나의 jenkins job 으로 관리. 빌드이력에 devops-multibranch-test » stage 으로 branch 가 표시됨
- jenkins 에서 새 item > multibranch pipeline 으로 생성<br/>
- 입력항목
<pre><code>
Branch Sources : Gitea Server, Credential, Owner(dkkim), Repository(devops-test), Discover Branches strategy(All Branches), Build Configuration scriptpath(Jenkinsfile), Trigger Token(devops-multibranch-test)
</code></pre>


# NEXUS 설치

1. windows 용일 경 
- nexus.zip 을 다운로드 후 압축해제
- bin 디렉토리에서 다음 명령 실행
    &nbsp; > nexus /install
    &nbsp; > nexus /run
- http://localhost:8081 에 접속

2. 
    
---

# Markdown
##### #으로 H1 ~ H6 의 제목을 표시
##### + 순서없는 목록을 표시할때 *,+,-을 이용한다
##### BlockQuote > 이메일에서 사용하는 인용부호 

##### 순서 목록
1. 순서있는 목록1
2. 순서있는 목록2

##### 코드 블록
<pre>
	<code>
	public static void codeblock() {
		int a = 0;
	}
	</code>
</pre>	

##### 링크
1. [GOOGLE](https://www.google.com)

##### 스타일 

*single asterisks*
_single underscores_
**double asterisks**
__double underscores__
~~cancelline~~

##### 이미지

<img src="/path/img.jpg" width="50%" height="50%" title="크기설정" alt="image"></img>
