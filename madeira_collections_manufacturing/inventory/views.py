from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import InventoryCategory
from .InventoryCategorySerializer import InventoryCategorySerializer
from .MaterialSerializer import MaterialSerializer
from .models import Material

#__________ Inventory Category api's ________________

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_categories(request):
    try:
        categories = InventoryCategory.objects.all()
        serializer = InventoryCategorySerializer(categories, many=True)
        return Response(serializer.data)
    except:
        return Response({'message': "Somthing went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    try:
        serializer = InventoryCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': "Somthing went wrong"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category(request, pk):
    try:
        category = InventoryCategory.objects.get(pk=pk)
        serializer = InventoryCategorySerializer(category)
        return Response(serializer.data)
    except InventoryCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_category(request, pk):
    try:
        category = InventoryCategory.objects.get(pk=pk)
    except InventoryCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InventoryCategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, pk):
    try:
        category = InventoryCategory.objects.get(pk=pk)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except InventoryCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

#__________ Inventory Material api's ________________

# GET all materials
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_materials(request):
    try:
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)
    except:
        return Response({'message': "Somthing went wrong"}, status=status.HTTP_400_BAD_REQUEST)

# POST to create a new material
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_material(request):
    try:
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': "Somthing went wrong"}, status=status.HTTP_400_BAD_REQUEST)

# GET a specific material by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_material(request, pk):
    try:
        material = Material.objects.get(pk=pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)
    except Material.DoesNotExist:
        return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)

# PUT to update an existing material
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_material(request, pk):
    try:
        material = Material.objects.get(pk=pk)
    except Material.DoesNotExist:
        return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MaterialSerializer(material, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE a specific material by ID
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_material(request, pk):
    try:
        material = Material.objects.get(pk=pk)
        material.delete()
        return Response({"message": "Material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Material.DoesNotExist:
        return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
