import json  
from django.http import JsonResponse  
from django.shortcuts import get_object_or_404
from .models import *  

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

@swagger_auto_schema(
        method="POST", 
        tags=["첫번째 view"],
        operation_summary="post 생성", 
        operation_description="post를 생성합니다.",
        request_body= PostSerializer,
        responses={
            201: '201에 대한 설명', 
            400: '400에 대한 설명',
            500: '500에 대한 설명'
        }
)

@api_view(['POST']) # !! 추가 부분 !!
def create_post(request):
    title = request.data.get('title')  # request.body 대신 request.data 사용
    content = request.data.get('content')

    if not title or not content:
        return Response({'message': '제목과 내용을 입력해주세요.'}, status=400)

    post = Post.objects.create(title=title, content=content)
    
    return Response({'message': 'success'}, status=201)
    # JsonResponse 대신 Response 사용

@api_view(['POST'])
def create_post_v2(request):
    serializer = PostSerializer(data=request.data) # JSON → Python 객체 변환 (역직렬화)
    
    if serializer.is_valid():  # 데이터 유효성 검사
        post = serializer.save()  # DB 저장
        message = f"id: {post.pk}번 포스트 생성 성공"
        return Response({'message': message, 'post': serializer.data}, status=201)

    return Response(serializer.errors, status=400)  # 유효성 검사 실패 시 오류 반환

from rest_framework.views import APIView

class PostApiView(APIView) :
    def get(self, request, pk=None):
        if pk: # 특정 pk 조회
            post = get_object_or_404(Post, pk=pk)

            postSerializer = PostSerializer(post) # Python -> JSON 변환 (직렬화)
            message = f"id: {post.pk}번 포스트 조회 성공"
            return Response({'message': message, 'post': postSerializer.data}, status=status.HTTP_200_OK)
            # status=status.HTTP_200_OK 이런식으로도 작성 가능
            # status=200도 가능!(저는 이렇게 쓰긴 합니당)
        
        posts = Post.objects.all() # 전체 조회
        postSerializer = PostSerializer(posts, many=True) # 여러 객체일 땐 many=True 필수!
        return Response({'posts': postSerializer.data}, status=200)
    
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        
        message = f"id: {pk}번 포스트 삭제 성공"
        return Response({'message': message}, status=200)    

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'post': serializer.data,
                'message': f'id: {pk}번 게시글 수정 성공'
            }, status=200)
        
        return Response(serializer.errors, status=400)

def get_post(request, pk):  # 특정 Post 객체를 조회하는 함수
	if request.method == 'GET':  # HTTP 요청 메서드가 GET인지 확인
		post = get_object_or_404(Post, pk=pk)  # Post 모델에서 pk에 해당하는 객체를 가져옴, 없으면 404 오류 발생
		data = {  # 응답으로 보낼 데이터를 딕셔너리 형태로 구성
			'id': post.pk,  # Post 객체의 ID
			'제목': post.title,  # Post 객체의 제목
			'내용': post.content,  # Post 객체의 내용
			'메시지': '조회 성공'  
		}
		return JsonResponse(data, status=200) 
	else:  
		return JsonResponse({'message':'GET 요청만 허용됩니다.'}) 

def get_posts_all(request): 
    if request.method == 'GET': # GET 요청으로만 동작하도록 제한
        posts = Post.objects.all()  # all() 메서드로 모든 Post 객체 조회 
        data = []  # 응답으로 보낼 데이터를 담을 리스트 초기화

        for post in posts: # 각 Post 객체 정보 추출
            data.append({ # 추출된 정보 ->  data 리스트에 추가
                'id': post.id,
                '제목': post.title, 
                '내용': post.content,
                '메시지': '조회 성공' # "메시지" 필드 추가
            })
        return JsonResponse({'posts': data}, status=200) 
    else: 
        return JsonResponse({'message': 'GET 요청만 허용됩니다.'}) 

def update_post(request, pk):
    if request.method == 'POST':  
        post = get_object_or_404(Post, pk=pk)  # Post 모델에서 pk에 해당하는 객체를 가져옴, 없으면 404 오류 발생
        data = json.loads(request.body)  

        if 'title' in data:  # 요청 데이터에 'title' 내용이 있는지 확인
            post.title = data['title']  # Post 객체의 'title' 필드를 요청 데이터의 값으로 업데이트
        if 'content' in data:  # 요청 데이터에 'content' 내용이 있는지 확인
            post.content = data['content']  # Post 객체의 'content' 필드를 요청 데이터의 값으로 업데이트

        post.save()  # 변경된 Post 객체를 데이터베이스에 저장

        data = {  
            'post': {  # 수정된 게시글 정보
                'id': post.id,  
                '제목': post.title, 
                '내용': post.content, 
            },
            'message': f'id: {pk}번 게시글 수정 성공' 
        }
        return JsonResponse(data, status=200)  
    return JsonResponse({'message': 'POST 요청만 허용됩니다.'}) 

def delete_post(request, pk):
    if request.method == 'DELETE':
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        data = {
            "message" : f"id: {pk} 포스트 삭제 완료"
        }
        return JsonResponse(data, status=200)
    return JsonResponse({'message':'DELETE 요청만 허용됩니다.'})

from django.http import HttpResponse

def get_comment(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        comment_list = post.comments.all()
        return HttpResponse(comment_list, status=200)

def click_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        data = json.loads(request.body)
        user_id = data.get("user_id")
        member = get_object_or_404(Member, pk=user_id)
        UserPost.objects.get_or_create(member_id=member, post_id=post) #UserPost 테이블에 추가
        return HttpResponse(status=204)

def get_like_count(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        like_count = UserPost.objects.filter(post_id=post).count() #해당 포스트의 좋아요 수를 UserPost에서 가져옴
        data = {
            'like_count' : like_count
		} 
        return JsonResponse(data, status=200)

def sort_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        
        posts_with_comment_count = []
        for post in posts:
            comment_count = post.comments.count()
            posts_with_comment_count.append((post, comment_count)) #(게시물, 댓글 수) 리스트 만듦
        
        posts_sorted = sorted(posts_with_comment_count, key=lambda x: x[1], reverse=True) #댓글 수를 기준으로 내림차순 정렬. x[1]이 댓글 수를 뜻함. 
        
        data = []
        for post in posts_sorted:
            data.append({
                'id': post.id,
                '제목': post.title,
                '내용': post.content,
                '메시지': '조회 성공'
            })
        return JsonResponse({'posts': data}, status=200)
