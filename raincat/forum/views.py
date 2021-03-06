import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from forum.models import Post, User, Comment
from forum.serializers import PostSerializer, UserSerializer, CommentSerializer
from rest_framework import generics, status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication
#from rest_framework.permissions import IsAuthenticated

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = Post.objects.get(pk=post_id)
        print('The self.request.user is: ', self.request.user)
        serializer.save(author=self.request.user, article=post)
'''
    def get_query_set(self):
        post_id = self.request.data.get('post')
        comment_article = Post.objects.get(pk=post_id)
        return Comment.objects.filter(article=comment_article)
'''        
'''
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        author_name = request.data.get('author')
        author = User.objects.get(username=author_name)
        article_id  = request.data.get('post')
        article = Post.objects.get(pk=article_id)
        content = request.data.get('content')
        print('show some imformation about content data and article')
        print(content, article)
        instance = Comment(author=author, content=content, article=article)
        instance.save()
        return Response(serializer.initial_data)
'''

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def perform_create(self, serializer):
        print("This is the type of request.user", type(self.request.user))
        print("This is request._request.user", self.request._request.user)
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserList(generics.ListCreateAPIView):
#    authentication_classes = (BasicAuthentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def create(self, request):

        #print(request.data, request.data['username'], request.data.get('username'), request.POST, request.POST.get('username'))
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            print(username, email, password)
            instance = User(username=username, email=email)
            instance.set_password(password)
            instance.save()
            return Response(serializer.validated_data)
        else:
            print("validate error")
            return Response({
                'status': 'Bad request',
                'message': 'Account could not be created with received data.'
                }, status=status.HTTP_400_BAD_REQUEST)



class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfile(APIView):
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        print('what the request data now: ' , request.data, request.data.get('password'))
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()
            return Response(serializer.data)


class LoginView(views.APIView):
#    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        #data = json.load(request.body)
        '''        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        username = data.get('username', None)
        password = data.get('password', None)
        '''
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        account = authenticate(username=username, password=password)
        #print(account, account.password)
        print('The user is:', request.user)

        if account is not None:
            if account.is_active:
                print("before login:", request.user)
                login(request, account)
                print("after login:", request.user)

                serialized = UserSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled',
                    }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination valid'
                }, status=status.HTTP_401_UNAUTHORIZED)
