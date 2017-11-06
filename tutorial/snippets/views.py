from django.http import JsonResponse, HttpResponse
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


@csrf_exempt
def snippet_detail(request, pk):
    # pk에 해당하는 Snippet이 존재하는지 확인 후 snippet 변수에 할당
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # GET 요청시에는 snippet을 serialize한 결과를 보여줌
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        # PUT 요청시에는 전달 된 데이터를 이용해서 snippet 인스턴스의 내용을 변경
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.erros, status=400)

    elif request.method == 'DELETE':
        # DELETE 요청시에는 해당 Snippet 인스턴스를 삭제
        snippet.delete()
        return HttpResponse(status=204)
