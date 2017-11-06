from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from snippets.serializers import SnippetSerializer
from .models import Snippet


# CSRF 인증을 사용하지 않음
@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        # 쿼리셋을 serialize 할 때는 many=True 옵션 추가
        serializer = SnippetSerializer(snippets, many=True)
        # 기본적으로 JsonResponse는 dict형식으로 리턴하지만,
        # safe=False이면 주어진 데이터는 dict가 아니어도 됨 (지금의 경우 리스트 객체가 옴)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # request로 전달 된 데이터들을 JSONParse를 사용하여 파이썬 데이터 형식으로 파싱
        data = JSONParser().parse(request)
        # 처리 된 데이터를 사용해 SnippetSerialzier 인스턴스를 생성
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
