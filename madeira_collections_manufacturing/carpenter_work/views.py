from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from order.models import Order
from django.http import JsonResponse
from inventory.models import Material
from .models import CarpenterEnquire
from .carpenter_enquire_serializer import CarpenterEnquireSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_carpenter_requests(request, carpenter_id):
    try:
        orders = Order.objects.filter(carpenter_id=carpenter_id)
        orders_data = []
        for order in orders:
            material_list = []
            for material in order.material_ids.all():
                material_item = {
                    'material_id': material.id,
                    'material_name': material.name
                }
                material_list.append(material_item)
            order_data = {
                'order_id': order.id,
                'product_name': order.product_name,
                'product_name_mal': order.product_name_mal,
                'product_description': order.product_description,
                'product_description_mal': order.product_description_mal,
            }
            orders_data.append(order_data)
        return JsonResponse({'order_data': orders_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
    
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def carpenter_requests_delete(request, order_id):
#     try:
#         carpenter_eqr = CarpenterEnquire.objects.all()
#         carpenter_eqr.delete()
#         return Response({'message': 'Carpenter request deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#     except Order.DoesNotExist:
#         return Response({'error': 'Carpenter request'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def carpenter_request_accept(request, order_id, carpenter_id):
    try:
        carpenter_enquiries = CarpenterEnquire.objects.filter(order_id=order_id, carpenter_id = carpenter_id)
        for enquiry in carpenter_enquiries:
            enquiry.status = 'checking'
        order = Order.objects.get(id = order_id)
        order.enquiry_status = 'checking'
        serializer = CarpenterEnquireSerializer(carpenter_enquiries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def carpenter_request_respond(request, order_id, carpenter_id):
    try:
        carpenter_enquiries = CarpenterEnquire.objects.filter(order_id=order_id, carpenter_id = carpenter_id)
        for enquiry in carpenter_enquiries:
            if (
                enquiry.material_height is None or 
                enquiry.material_length is None or 
                enquiry.material_width is None
            ):
                e = 'Missing material details'
                return JsonResponse({'error': str(e)}, status=404)

        for enquiry in carpenter_enquiries:
            enquiry.status = 'completed'
        order = Order.objects.get(id = order_id)
        order.enquiry_status = 'completed' 
        serializer = CarpenterEnquireSerializer(carpenter_enquiries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def carpenter_request_material_creation(request, order_id, carpenter_id, carpenter_request_id, material_id):
    try:
        carpenter_enquiry = CarpenterEnquire.objects.filter(
            id=carpenter_request_id,
            order_id=order_id,
            carpenter_id=carpenter_id,
            material_id=material_id,
            status = 'checking'
        ).first()
        if not carpenter_enquiry:
            return JsonResponse({'error': 'Carpenter Enquiry not found'}, status=404)
        serializer = CarpenterEnquireSerializer(carpenter_enquiry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': serializer.errors}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
