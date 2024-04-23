from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser as User
from projects.models import Project, Solution
from projects.permissions import IsOwner
from projects.serializers import ProjectSerializer, SolutionSerializer

class Projects(APIView):
    model = Project
    serializer_class = ProjectSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.model.objects.all()
            queryset = self.serializer_class(queryset, many=True)
            return Response(queryset.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectDetail(APIView):
    model = Project
    serializer_class = ProjectSerializer
    
    def get(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(self.model, project_slug=project_slug)
        try:
            solutions = Solution.objects.filter(project=project)

            project = self.serializer_class(project)
            solutions = SolutionSerializer(solutions, many=True)
            return Response(project.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CreateProject(APIView):
    model = Project
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            request.data['creator'] = request.user.id
            project = self.serializer_class(data=request.data)
            
            if project.is_valid():
                project.save()
                return Response(project.data, status=status.HTTP_201_CREATED)
            return Response(project.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class Enroll(APIView):
    model = Project
    permission_classes = [IsAuthenticated]
    
    def post(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(self.model, project_slug=project_slug)
        try:
            user = request.user
        
            if project.enrolled_users.contains(user):
                return Response({
                    'response': 'already enrolled'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if not (user == project.creator):
                project.enrolled_users.add(user)
                
                return Response({
                    'response': 'enrollment succesful'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'project creator can\'t enroll in project'
                }, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class UpdateProject(APIView):
    model = Project
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = ProjectSerializer
    
    def put(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(self.model, project_slug=project_slug)
        try:
            project = self.serializer_class(project, data=request.data, partial=True)
            
            if project.is_valid():
                project.save()
                return Response(project.data, status=status.HTTP_200_OK)
            return Response(project.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteProject(APIView):
    model = Project
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(self.model, project_slug=project_slug)
        try:
            project.delete()
            return Response({
                'response': 'project deleted'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Solutions(APIView):
    model = Solution
    serializer_class = SolutionSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            solutions = self.model.objects.all()
            solutions = self.serializer_class(solutions, many=True)
            return Response(solutions.data, status=status.HTTP_200_OK) 
               
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class SolutionDetail(APIView):
    model = Solution
    serializer_class = SolutionSerializer
    
    def get(self, request, uid, *args, **kwargs):
        solution = get_object_or_404(self.model, uid=uid)
        try:
            solution = self.serializer_class(solution)
            return Response(solution.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class CreateSolution(APIView):
    model = Solution
    permission_classes = [IsAuthenticated]
    serializer_class = SolutionSerializer
    
    def post(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(Project, project_slug=project_slug)
        try:

            if not project.creator == request.user or not project.enrolled_users.contains(request.user.id):
                return Response({
                    'error': 'enroll in this project to create a solution for it'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            request.data['project'] =  project.id
            request.data['creator'] = request.user.id
            solution = self.serializer_class(data=request.data)
            
            if solution.is_valid():
                solution.save()
                
                return Response(solution.data, status=status.HTTP_201_CREATED)
            return Response(solution.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateSolution(APIView):
    model = Solution
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = SolutionSerializer
    
    def put(self, request, uid, *args, **kwargs):
        try:
            if len(request.data.keys()) < 1:
                return Response({
                    'error': 'request data can not be empty'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            solution = get_object_or_404(self.model, uid=uid)
            solution = self.serializer_class(solution, data=request.data, partial=True)
            
            if solution.is_valid():
                solution.save()
                return Response(solution.data, status=status.HTTP_200_OK)
            return Response(solution.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class DeleteSolution(APIView):
    model = Solution
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, uid, *args, **kwargs):
        solution = get_object_or_404(self.model, uid=uid)
        try:
            solution.delete()
            return Response({
                'response': 'solution deleted'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
projects = Projects.as_view()
project_detail = ProjectDetail.as_view()
create_project = CreateProject.as_view()
enroll = Enroll.as_view()
update_project = UpdateProject.as_view()
delete_project = DeleteProject.as_view()

solutions = Solutions.as_view()
solution_detail = SolutionDetail.as_view()
create_solution = CreateSolution.as_view()
update_solution = UpdateSolution.as_view()
delete_solution = DeleteSolution.as_view()