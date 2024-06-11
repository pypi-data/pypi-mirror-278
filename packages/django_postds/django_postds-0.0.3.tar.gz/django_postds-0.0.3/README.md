### django-medicio-dental

#### Introduction 
my demiansoft post & portfolio parts

블로그 포스트를 위해 admin에서 markdown 형식으로 글작성이 가능하다. 단, 이미지 삽입시 responsive 를 위해 class=img-fluid 클래스명 설정이
필요하며 마크다운 에디터에서 이미지 마크 다운에 {: .img-fluid}를 넣어줘야 적용이 된다.

---
#### Requirements

Django >= 4.2.11
libsass>=0.23.0
django-mdeditor >= 0.1.20
django-hitcount >= 1.3.5
django-taggit >= 5.0.1
django-light >= 0.1.0   # 밝은 admin 화면
pillow >= 10.3.0    # 데이터베이스에서 이미지 사용하기위해


---
#### Install
urls.py
```python
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
    path('postds/', include('django_postds.urls')),
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

settings.py  
```python
import os

INSTALLED_APPS = [
    'django_light', # django.contrib.admin 위에 위치
    ...
    'django.contrib.sitemaps',   # 사이트맵 만들기
    
    'django_analyticsds',  
	'django_utilsds',  
	'django_calendards',  
	'django_modalds', 
	
	'mdeditor',  # markdown WYSIWYG 에디터 사용하기
    'hitcount', 
    'taggit', 
    
	'django_medicio_dental',
]

...

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '_static/'),
]

MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  
X_FRAME_OPTIONS = 'SAMEORIGIN'  
  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# mdeditor 설정
MDEDITOR_CONFIGS = {
    'default': {
        'width': '100% ',  # Custom edit box width
        'height': 700,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "image", "code", "html-entities", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_folder': 'editor',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': False,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'sequence': True,  # Whether to open the sequence diagram function
        'watch': True,  # Live preview
        'lineWrapping': False,  # lineWrapping
        'lineNumbers': False,  # lineNumbers
        'language': 'en'  # zh / en / es
    }
    
}
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            'a',
            'abbr',
            'acronym',
            'b',
            'blockquote',
            'em',
            'i',
            'li',
            'ol',
            'p',
            'strong',
            'ul',
            'h1',
            'h2',
            'h3',
            'h5',
            'h6',
            'ul',
            'hr',
            'img',
            'code',
        ],
        "WHITELIST_ATTRS": [
            'src',
            'class',
            'href',
            'id',
        ],
        "MARKDOWN_EXTENSIONS": [
            "fenced_code",
            "attr_list",
        ],
    }
} 
```

in the shell
```shell
>> pip install django-postds
>> python manage.py makemigrations
>> python manage.py migrate
>> python manage.py createsuperuser
```

---
#### Composition

프로젝트 내의 \_data 폴더 안에 postds.py 파일을 생성하고 다음과 같은 형식으로 작성한다.(예제 파일 참조)

```python
active_template = "mediciodental"
```
---

