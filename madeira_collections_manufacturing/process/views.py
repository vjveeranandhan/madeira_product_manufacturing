from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Process
from .ProcessSerializer import ProcessSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# GET all processes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_processes(request):
    try:
        processes = Process.objects.all()
        serializer = ProcessSerializer(processes, many=True)
        return Response(serializer.data)
    except:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
# POST to create a new process
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_process(request):
    try:
        serializer = ProcessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
# GET a specific process by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_process(request, pk):
    try:
        process = Process.objects.get(pk=pk)
        serializer = ProcessSerializer(process)
        return Response(serializer.data)
    except Process.DoesNotExist:
        return Response({"error": "Process not found"}, status=status.HTTP_404_NOT_FOUND)

# PUT to update an existing process
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_process(request, pk):
    try:
        process = Process.objects.get(pk=pk)
    except Process.DoesNotExist:
        return Response({"error": "Process not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProcessSerializer(process, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE a specific process by ID
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_process(request, pk):
    try:
        process = Process.objects.get(pk=pk)
        process.delete()
        return Response({"message": "Process deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Process.DoesNotExist:
        return Response({"error": "Process not found"}, status=status.HTTP_404_NOT_FOUND)
