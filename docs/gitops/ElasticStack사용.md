# 목차
1. ElasticSearch 
    + 기본
        - 인덱스와 도큐먼트
        - 도큐먼트 CRUD
        - 벌크 (생략)
        - 매핑
        - 인덱스 템플릿
        - 분석기        
    + 검색
        - 쿼리 컨텍스트와 필터 컨텍스트
        - 쿼리
        - 전문쿼리와 용어 수준 쿼리
    + 집계 (생략)    
2. LogStash
3. Beats
4. Kibana
    
# ElasticSearch    
##### create index and document 
PUT index2/_doc/1
{
    "name": "mike",
    "age": 25,
    "gender": "male"
}

PUT index2/_doc/2
{
    "name": "jane",
    "country": "france"
}

PUT index2/_doc/3
{
    "name": "kim",
    "age": "30",
    "gender": "female"
}

##### update document
POST index2/_update/1
{
  "doc": {
    "name": "lee"
  }
}

DELETE index2/_doc/3

GET index2/_search

##### 명시적 매핑 : 인덱스를 생성할 때 mappings, properties 를 지정 
PUT index3
{
  "mappings": {
    "properties": {
      "age": {"type": "short"},
      "name": {"type": "text"},
      "gender": {"type": "keyword"}
    }
  }
}

GET index3/_mapping

##### 템플릿 : 파티션에 사용 

##### 분석기 
POST _analyze
{
  "analyzer": "simple",
  "text": "The 10 most loving dog breeds."
  
}
##### tokenizer
POST _analyze
{
  "tokenizer": "ngram",
  "text": "The 10 most loving dog breeds."
  
}
##### filter
POST _analyze
{
  "tokenizer": "standard",
  "filter": ["uppercase"],
  "text": "The 10 most loving dog breeds."
}

##### query context
GET kibana_sample_data_ecommerce/_search
{
  "query": {
    "match": {
      "category": "clothing"
    }
  }
}
##### filter context : query ctx 응답은 scoring 이지만 필터의 결과는 yes or no 이다.
GET kibana_sample_data_ecommerce/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "day_of_week": "Friday"
          }
        }
      ]
    }
  }
}

##### score. 
GET kibana_sample_data_ecommerce/_search
{
  "query": {
    "match": {
      "products.product_name": "Pants"
    }
  },
  "explain": true    # explain 은 실행된 수식을 보여줌
}

##### Full Text 쿼리와 Term level 쿼리
1. Full Text 쿼리
    + 매치 쿼리
        - 단일 용어로 검색 
    <pre><code>
GET kibana_sample_data_ecommerce/_search
{
  "_source": ["customer_full_name"],  # customer_full_name 필드만 결과로 반환 
  "query": {
    "match": {
      "customer_full_name": "Mary"
    }
  }
}
</code></pre>
        - 복수개의 용어로 검색 : "customer_full_name": "Mary bailey" 
            * 용어들 간 공백은 OR 로 인식. 
            * AND 를 사용하고 싶을 경우 operator 사용 
            <pre><code>
  "query": {
    "match": {
      "customer_full_name": {
        "query": "Mary bailey",
        "operator": "and"
       } 
    }
  }
            </code></pre>
    + Match Phrase 쿼리 
        - 2개 이상의 용어가 모두 포함되어야 하고 순서도 맞아야 함. 쿼리를 토큰화하기는 한다. [mary,bailey]
        - mary bailey 쿼리일 경우 중간에 다른 단어가 존재하면 (mary tony bailey) 결과에서 제외된다.

2. Term Level 쿼리
    + 용어 쿼리 
    <pre><code>    
GET kibana_sample_data_ecommerce/_search
{
  "_source": ["customer_full_name"],
  "query": {
    "term": {
      "customer_full_name.keyword": "Mary Bailey"  # 주의 : .keyword 필드까지 입력해야 한다.
    }
  }
}
    </code></pre>
    + 용어들 쿼리
    <pre><code>    
GET kibana_sample_data_ecommerce/_search
{
  "_source": ["day_of_week"],
  "query": {
    "terms": {                              # 주의 : term이 아니라 terms. s 를 붙이자. 
      "day_of_week": ["Monday","Sunday"]
    }
  }
}
    </code></pre>
    + 날짜/시간 데이터 타입 
    <pre><code>        
GET kibana_sample_data_flights/_search
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "2024-07-01||+1M",
        "lte": "2024-09-30||-1M"
      }
    }
  }
}
    </code></pre>
    + 범위데이터 타입 : integer_range, float_range, long_range, double_range, date_range, ip_range
    <pre><code>    
PUT range_test_index
{
  "mappings": {
    "properties": {
      "test_date": {
        "type": "date_range"  # 주의 : date 타입이 아니라 date_range 
      }
    }
  }
}
    </code></pre>
    
# LogStash

1. 파이프라인 
    + logstash -e "input {stdin{}} output {stdout{}}" [enter]
<pre><code>
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
    + 입력 : 다양한 플러그인을 활용. 파일, 트위터, syslog, kafka, jdbc 등
        - 파일 플러그인
            * config/logstash-test.conf 생성 (반드시 conf 일 필요 없음) > 참조
            * 실행 > logstash -f .\config\logstash-test.conf
    + 필터
        - mutate 
        <pre><code>
filter {
  mutate {
    split => { "message" => " "}                 # 공백으로 자르기
	add_field => {"id" => "%{[message][2]}" }     # 필드 추가 (id 가 필드명, 값은 message[2])
	remove_field => "message"                     # 필드 삭제 
  }
}
        </code></pre>
       
       - dissect : %{필드명} 으로 파싱. %{} 외 문자들은 모두 구분자 역할.
    
       - grok : 정규식을 이용해 문자열을 파싱. %{패턴:필드명} 형식으로 파싱. 자주 사용되는 패턴을 예약해 놓았다.           
           * NUMBER, SPACE, URI, IP, LOGLEVEL
           * TIMESTAMP_ISO8601(2020-01-01T12:00:00+09:00). patter_definitions 옵션을 사용해서 정규식 추가 가능 
           * DATA
           * GREEDYDATA : 표현식의 가장 뒤에 위치하면 해당 위치부터 이벤트의 끝까지를 값으로 인식 
           * 정규식
               > 변수명 뒤에 :int 는 변경시 정수형으로 변환. 
               > 정규 표현식 정의 
               <pre><code>
pattern_definitions => { "MY_TIMESTAMP" => "%{YEAR}[/-]%{MONTHNUM}[/-]%{MONTHDAY}[T ]%{HOUR}:?%{MINUTE}(?::?%{SECOND})?%{ISO8601_TIMEZONE}?" }
match => { "message" => "%{MY_TIMESTAMP:timestamp} * \[%{DATA:id} .. 
	            </code></pre>