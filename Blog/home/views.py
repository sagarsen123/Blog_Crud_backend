from rest_framework import status
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Blog


class PublicBlogView(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')
            # blogs = Blog.objects.all()

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

            # pagination
            page_number = request.GET.get('page', 1)
            paginator = Paginator(blogs , 1)
            serializer = BlogSerializer(paginator.page(page_number), many=True)

             
            return Response({
                    'data': serializer.data,
                    'message': 'Blog fetched Successfully'
                },status = status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'Something Went Wrong or Invalid Page No'
                },status = status.HTTP_400_BAD_REQUEST)

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user = request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))
            serializer = BlogSerializer(blogs , many = True)
            return Response({
                    'data': serializer.data,
                    'message': 'Blog fetched Successfully'
                },status = status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'Something Went Wrong'
                },status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))

            # Check if Blog exists or not
            if not blog.exists():
                return Response({
                        'data': {},
                        'message': 'Invalid Blog Uid'
                    },status = status.HTTP_404_NOT_FOUND)

            #  if blog exists check if the user is owner or not
            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'You are not Authorized'
                },status = status.HTTP_400_BAD_REQUEST)

            # Check the sent data is valid not
            serializer = BlogSerializer(blog[0], data=data, partial = True)

            # if not return message
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                },status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            # return the response
            return Response({
                    'data': serializer.data,
                    'message': 'Blog Updated Successfully'
                },status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'Something Went Wrong'
                },status = status.HTTP_400_BAD_REQUEST)



    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            print("user",request.user)
            serializer = BlogSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                },status = status.HTTP_400_BAD_REQUEST)
            serializer.save()

            return Response({
                    'data': serializer.data,
                    'message': 'Blog Created Successfully'
                },status = status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'Check Credentials'
                },status = status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))

            # Check if Blog exists or not
            if not blog.exists():
                return Response({
                        'data': {},
                        'message': 'Invalid Blog Uid'
                    },status = status.HTTP_404_NOT_FOUND)

            #  if blog exists check if the user is owner or not
            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'You are not Authorized'
                },status = status.HTTP_400_BAD_REQUEST)

            #  if user is owner delete the blog
            blog[0].delete()

            return Response({
                    'data': {},
                    'message': 'Blog Deleted Successfully'
                },status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'Something Went Wrong'
                },status = status.HTTP_400_BAD_REQUEST)