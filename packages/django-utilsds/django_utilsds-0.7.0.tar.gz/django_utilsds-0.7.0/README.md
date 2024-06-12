### django-utilsds

#### Introduction

demiansoft 에서 사용하는 장고앱 django-utilsds

---
#### Requirements

Django >= 4.2.11

---
#### Install

```
>> pip install django-utilsds
```

settings.py

```
INSTALLED_APPS = [  
    ...
    
    'django_utilsds',
]
```

---
#### Composition

여러가지 유틸리티 태그 모음앱으로 현재 split 태그 사용가능하다.

html 파일 내에서 다음 코드를 삽입하여 사용한다.  
```html  
{% load django_utilsds_tags %}
{{ "test/utils/app"|split:"/" }}
-> ['test', 'utils', 'app']
```

```html 
{% load django_utilsds_tags %}
{{ "서울시 구로구 새말로"|add_br:"2" }}
-> 서울시 구로구<br>새말로
```

```html
{% load django_utilsds_tags %}
{{ "test_utils_app"|underscore_to_hypen }}
-> test-utils-app
```  

value 값을 / 을 단위로 나눠서 리스트 형식으로 반환한다.

또는 views.py 에서 직접 불러서 사용할수 있다.
```python
from django_utilsds import utils
```

get_json(path: str) - json 형식의 데이터 파일을 불러온다.

mail_to(title: str, text: str, mail_addr) - 메일을 보낸다.

views.py
def robots(request) - robots.txt를 만들어준다.
