# 목차
1. SSL 
2. ElasticSearch
3. Kibana
4. LogStash
        
# SSL
1. 인증 관련 파일 확장자
    - PEM (Privacy Enhanced Mail)은 PKCS#1 Base64 로 인코딩한 텍스트 형식의 파일. 주로 인증서나 개인키 저장
        + 인증서 PEM 시작 : -----BEGIN CERTIFICATE-----
        + 개인키 PEM 시작 : -----BEGIN RSA PRIVATE KEY-----
    - CRT 는 인증서 파일이며 대부분 PEM 포맷이다. 
    - CER 은 windows 기반에서 인증서 파일임을 구분하기 위한 확장자. CRT 와 동일
    - DER (Distinguished Encoding Rules)형식으로 인코딩된 바이너리 파일로 주로 인증서
    - CSR(Certificate Signing Request) 은 인증기관(CA)에 인증서 발급 요청을 하는 파일.<br/>
          안에는 내 공개키 정보와 사용하는 알고리즘 정보등이 있음.<br/>
          CSR 생성시 보통 PEM 형식으로 인코딩해서 전달하며 다음과 같은 PEM 헤더가 있습니다<br/>
          -----BEGIN NEW CERTIFICATE REQUEST-----
    - PFX 또는 P12 는 PKCS#12 형식의 포맷으로 Personal Information Exchange Format 을 의미.<br/>
        용도는 인증서, 개인키 그리고 인증서 체인 정보를 하나의 묶어서 가져오기나 내보내기 용으로 많이 사용<br/>
        Java 소프트웨어는 기본 "Java 키스토어" 형식인 PKCS#12(PFX) 형식을 사용
    - KEY 파일은 개인키 파일을 알려주기 위해 사용한다. PEM 형식 일수도 있고 DER 형식인 바이너리 포맷인 경우도 있어
    - BEGIN PRIVATE KEY"PKCS#8" 키 형식을 의미. PEM 포맷의 보다 현대적인 대체물로 의도
    - BEGIN OPENSSH PRIVATE KEY는 OpenSSH를 위해 OpenSSH에서 발명한 형식이며, PEM/PKCS 형식과 달리 데이터 구조에 SSHv2 패킷 직렬화를 사용
    
2. 관련 개념 
    - Passphrase: 개인 키(private key)를 보호하기 위해 설정한 장문의 문자열. 공동/금융인증서 사용 시 입력하는 암호가 Passphrase에 해당   
    - CA : 인증서의 역할은 클라이언트가 접속한 서버가 클라이언트가 의도한 서버가 맞는지를 보장하는 역할 => 도메인명이 필요한 이유?
    - 인증서 내용 : 서버 정보, 서버측 공개키 
    - SSL handshake
        + client hello : 클라이언트가 서버에 접속하여 랜덤데이터, 자신이 가능한 암호화 방식, 이미 세션 연결중이면 세션아이디를 전송
        + server hello : 서버측 랜덤데이터, 클라이언트가 전송한 암호화 방식중 자신이 사용 가능한 암호화 방식, 인증서를 전송
        + 클라이언트 측 : 서버에서 받은 인증서가 CA 발급된 것인지 확인하기 위해 내장된 *CA 공개키를 이용해서 인증서를 복호화* 한다. 성공하면 CA가 개인키로 암호화한 인증서임.
                     *서버에서 수신한 인증서 안에 있는 공개키로 랜덤데이터를 암호화* 하여 서버로 송신
        + 서버 측 : 서버는 수신한 secret 값을 개인키로 복호화하여 session key 를 생성.
        + 세션 연결
        + 세션 종료 : 통신에서 사용한 대칭키인 session key 폐기    
3. OpenSSL 로 인증서 생성
    - windows 에서는 openssl 다운로드 필요
    - key pair 생성        
        + 개인키 생성 : openssl331\bin>openssl genrsa -out es-private.pem 2048 (passphrase 없음)
        + 공개키 생성 : openssl331\bin>openssl rsa -in es-private.pem -pubout -out es-public.pem
    - CSR 생성
<pre><code>
openssl331\bin>openssl req -new -key es-private.pem -out elastic.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:KR
State or Province Name (full name) [Some-State]:Kyunggi
Locality Name (eg, city) []:Koyang
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Uncharted DK
Organizational Unit Name (eg, section) []:overall infra
Common Name (e.g. server FQDN or YOUR name) []:infra.unchart.com
Email Address []:unchartwater@gmai.com
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
</code></pre>
    - CRT 생성 : openssl331\bin>openssl x509 -req -days 3650 -in elastic.csr -signkey es-private.pem -out elastic.crt
        + 위 과정 생략한 CSR 성성없이 CRT 생성 : openssl req -new -x509 -days 365 -nodes -keyout test.key -out test.crt
    - P12 생성
<pre><code>
openssl331\bin>openssl x509 -req -days 3650 -in elastic.csr -signkey es-private.pem -out elastic.crt
Certificate request self-signature ok
subject=C=KR, ST=Kyunggi, L=Koyang, O=Uncharted DK, OU=overall infra, CN=infra.unchart.com, emailAddress=unchartwater@gmai.com
C:\develop\common\products\openssl331\bin>openssl pkcs12 -export -inkey es-private.pem -in elastic.crt -out elastic.p12
Enter Export Password:{비밀번호 입력 안해도 됨}
Verifying - Enter Export Password:{비밀번호 입력 안해도 됨}
</code></pre>

4. SSL 설정     
    - ca 인증서 생성
        + bin/elasticsearch-certutil ca --pem --o`ut config/certs/ca.zip [enter]
        + ca.zip 압축해제 
    - http 인증서 생성
        + bin/elasticsearch-certutil cert --out config/certs/elastic.zip --name elastic --ca-cert config/certs/ca/ca.crt --ca-key config/certs/ca/ca.key --dns infra.unchart.com --pem    
    ~~p12 인증서 파일을 복사 : $ES_PATH/config/certs~~
    
    - elasticsearch.yml 파일 수정
        + cluster.name: es-cluster 주석 해제
        + node.name: node-1 주석 해제 
        + network.host: infra.unchart.com 주석 해제 
        + http.port: 9200
        + http.host: 0.0.0.0
        + ssl 설정
        <pre><code>
        xpack.security.enabled: true
        xpack.security.http.ssl:
            enabled: true
            certificate: certs/elastic/elastic.crt
            key: certs/elastic/elastic.key
            certificate_authorities: certs/ca/ca.crt
            ~~keystore.path: certs/elastic.p12~~            
        </code></pre>   
        + xpack.license.self_generated.type: basic 
        + cluster.initial_master_nodes: ["node-1"]
        
    ~~~keystore 인증서 비밀번호 추가 : 
        cmd 창을 관리자모드로 실행
        $ES_PATH/bin> .\elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password [enter]
            p12 생성 시 입력한 비밀번호를 입력(없으면 그냥 enter)~~~

# Elastic Stack SSL 설정
    + https://www.elastic.co/kr/blog/configuring-ssl-tls-and-https-to-secure-elasticsearch-kibana-beats-and-logstash
# ElasticSearch
1. 설치
    - windows 용 zip 다운로드 > 압축풀기 
2. 설정 
    - /dkdocs/docs/gitops/elasticsearch.yml 참조
    - instances.yml 을 작성 후 아래처럼 CA 인증서 생성
        + elasticsearch-certutil ca --days 3650 (비밀번호 입력 안함)
    - elastic http 인증서 생성
        + elasticsearch-certutil cert --in config/instances.yml --out certs.zip --ca elastic-stack-ca.p12 --days 3650
    - hosts 에 elastic.unchart.com, kibana.unchart.com 추가.
        <pre><code>
			127.0.0.1 elastic.unchart.com
			127.0.0.1 kibana.unchart.com
			192.168.219.113 elastic.unchart.com
			192.168.219.113 kibana.unchart.com        
        </code></pre>
3. 실행
    - bin>elasticsearch.bat [enter]    
    - elastic 초기 패스워드 보관. kibana 를 위한 enroll token 은 필요없음. 
4. 확인
    -  패스워드 변경
        + bin>elasticsearch-reset-password -u elastic --url https://elastic.unchart.com:9200[enter]
    - 접속 (curl -u {id}:{password} https://)
        + curl -u elastic:{비번} https://elastic.unchart.com:9200 -k [enter]
            
# Kibana
1. 설치
    - windows 용 zip 다운로드 > 압축풀기 
2. 설정    
    - /dkdocs/docs/gitops/kibana.yml 참조.
3. 실행
    - bin>kibana.bat [enter]
4. 확인 및 추가 설정
    - 브라우저에서 https://kibana.unchart.com:5601 에 접속
    - enroll token 을 입력하지 않고 "Config manually"를 클릭하여 진행
    - elasticsearch의 접속 주소를 입력
    - kibana_system 계정의 비밀번호를 생성
        + elasticsearch 설치 경로에서 bin/elasticsearch-reset-password --username kibana_system -i --url https://elastic.unchart.com:9200[enter]
    - 브라우저에서 kibana_system 계정의 비밀번호를 입력
    - 로그인 폼이 표시되면 elastic 계정과 비밀번호를 입력함
                    
# LogStash
1. 설치
    - windows 용 zip 다운로드 > 압축풀기 
2. 설정    
    - logstash_system 계정의 비밀번호를 생성
        + elasticsearch 설치 경로에서 bin/elasticsearch-reset-password --username logstash_system -i --url https://elastic.unchart.com:9200[enter]
    - logstash.yml 수정
     
3. 실행
    - logstash -e "input {stdin{}} output {stdout{}}"
    - 실행한 창에서 hello world 를 입력한다.
    - 실행 결과
    <pre><code>
hello world [enter]
{
    "@timestamp" => 2024-08-18T08:47:23.183353600Z,
         "event" => {
        "original" => "hello world\r"
    },
      "@version" => "1",
          "host" => {
        "hostname" => "KDK-NB"
    },
       "message" => "hello world\r"
}
    </code></pre>