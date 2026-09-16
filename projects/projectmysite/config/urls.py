# ============================================================
# config/urls.py
#
# Django 프로젝트 전체의 최상위 URL 설정 파일이다.
#
# 각각의 앱이 담당하는 URL을 include()를 사용해 연결한다.
# ============================================================


# Django 관리자 화면을 사용하기 위해 가져온다.
from django.contrib import admin


# path:
# URL 경로를 등록한다.
#
# include:
# 앱 내부의 urls.py를 프로젝트 URL에 연결한다.
from django.urls import path, include


# 프로젝트 첫 화면에서 pybo 질문 목록을 표시하기 위해
# 분리된 base_views 모듈을 직접 가져온다.
from pybo.views import base_views


urlpatterns = [
    # Django 관리자 화면
    #
    # 주소:
    # /admin/
    path(
        'admin/',
        admin.site.urls,
    ),

    # pybo 앱의 URL을 연결한다.
    #
    # /pybo/로 시작하는 요청은
    # pybo/urls.py에서 나머지 주소를 처리한다.
    path(
        'pybo/',
        include('pybo.urls'),
    ),

    # common 앱의 로그인, 로그아웃, 회원가입 URL을 연결한다.
    #
    # /common/으로 시작하는 요청은
    # common/urls.py에서 처리한다.
    path(
        'common/',
        include('common.urls'),
    ),

    # 사이트의 기본 주소를 pybo 질문 목록에 연결한다.
    #
    # 주소:
    # /
    #
    # 실행 함수:
    # pybo/views/base_views.py의 index()
    path(
        '',
        base_views.index,
        name='index',
    ),
]