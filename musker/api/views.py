from rest_framework.decorators import api_view
from rest_framework.response import Response
from musker.models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def getPost(request):
    routes = [
        'GET /api',
        'GET /api/posts',
        'GET /api/post/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getObjects(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getObject(request,pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)    

    