from rest_framework.decorators import api_view
from rest_framework.response import Response
from .task import analyze_repo_task
from celery.result import AsyncResult

@api_view(['POST'])
def start_task(request):
    repo_url = request.data.get('repo_url')
    pr_number = request.data.get('pr_number')
    github_token = request.data.get('github_token')
    analyze_repo_task.delay(repo_url, pr_number, github_token)
    return Response({'status': 'Task started', "task_id": analyze_repo_task.request.id})

@api_view(['GET'])
def task_status(request, task_id):
    task = AsyncResult(task_id)
    return Response({'status': task.status, 'result': task.result, 'task_id': task.id, 'task':task})