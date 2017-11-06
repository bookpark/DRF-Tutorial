from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Snippet
from ..serializers import SnippetSerializer

__all__ = (
    'snippet_list',
    'snippet_detail',
)


# api_view 형태로 동작함 (request에 HttpRequest가 아닌 Request가 주어짐)
# GET, POST 요청에 대해서만 동작
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        # 쿼리셋을 serialize 할 때는 many=True 옵션 추가
        serializer = SnippetSerializer(snippets, many=True)
        # 데이터를 적절히 렌더링해주는 Response 객체를 리턴
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        # 인스턴스에 주어진 데이터가 유효할 경우
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    # pk에 해당하는 Snippet이 존재하는지 확인 후 snippet 변수에 할당
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET 요청시에는 snippet을 serialize한 결과를 보여줌
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE 요청시에는 해당 Snippet 인스턴스를 삭제
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
