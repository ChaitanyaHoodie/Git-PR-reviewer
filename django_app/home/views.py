from rest_framework.decorators import api_view
from rest_framework.response import Response
from .task import analyze_repo_task
from celery.result import AsyncResult

@api_view(['POST'])
def start_task(request):
    repo_url = request.data.get('repo_url')
    pr_number = request.data.get('pr_number')
    github_token = request.data.get('github_token')
    task=analyze_repo_task.delay(repo_url, pr_number, github_token)
    return Response({'status': 'Task started', "task_id": task.id})

@api_view(['GET'])
def task_status(request, task_id):
    task = AsyncResult(task_id)
    response={
        "task_id":task_id,
        "status":task.state,
        "result":task.result
    }
    return Response(response)