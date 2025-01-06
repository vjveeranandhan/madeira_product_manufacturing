from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order
from .OrderSerializer import OrderSerializer

# Create a new order
@api_view(['POST'])
def create_order(request):
    # try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # except:
    #     return Response({'error': 'Something went wrong'}, status=status.HTTP_404_NOT_FOUND)

# Retrieve a single order
@api_view(['GET'])
def retrieve_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

# Update an order
@api_view(['PUT'])
def update_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error': 'Something went wrong'}, status=status.HTTP_404_NOT_FOUND)

# Delete an order
@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

# List all orders
@api_view(['GET'])
def list_orders(request):
    try:
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Something went wrong'}, status=status.HTTP_404_NOT_FOUND)
