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
                'material_ids': material_list,
                'product_length': order.product_length,
                'product_height': order.product_height,
                'product_width': order.product_width,
                'reference_image': order.reference_image.url if order.reference_image else None,
                'finish': order.finish,
                'event': order.event
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
            enquiry.status = 'responded'
        serializer = CarpenterEnquireSerializer(carpenter_enquiries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
