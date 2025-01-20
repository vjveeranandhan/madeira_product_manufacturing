from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from order.models import Order
from django.http import JsonResponse
from inventory.models import Material
from inventory.MaterialSerializer import MaterialSerializer
from .models import CarpenterEnquire
from .carpenter_enquire_serializer import CarpenterEnquireSerializer
from order.OrderSerializer import OrderSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_carpenter_requests(request, carpenter_id):
    try:
        unique_order_ids = CarpenterEnquire.objects.filter(
            carpenter_id=carpenter_id).values_list('order_id', flat=True).distinct()
        print(unique_order_ids)
        orders_data = []
        for order_id in unique_order_ids:
            order = Order.objects.filter(id = order_id).first()
            order_data = {
                'order_id': order.id,
                'product_name': order.product_name,
                'product_name_mal': order.product_name_mal,
                'product_description': order.product_description,
                'product_description_mal': order.product_description_mal,
                'status': order.enquiry_status
            }
            orders_data.append(order_data)
        return JsonResponse({'order_data': orders_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def carpenter_request_accept(request, order_id):
    try:
        carpenter_enquiries = CarpenterEnquire.objects.filter(order_id=order_id)
        for enquiry in carpenter_enquiries:
            enquiry.status = 'checking'
        order = Order.objects.filter(id = order_id).first()
        order.enquiry_status = 'checking'
        order.save()
        serializer = CarpenterEnquireSerializer(carpenter_enquiries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def carpenter_request_view(request, order_id):
    try:
        order = Order.objects.filter(pk=order_id).first()
        order_serializer = OrderSerializer(order)
        material_ids = order_serializer.data['material_ids']
        material_data = []
        for material in material_ids:
            material_obj = Material.objects.filter(id= material).first()
            material_serializer = MaterialSerializer(material_obj)
            materials = material_serializer.data
            materials.pop('price', None)
            materials.pop('quantity', None)
            materials.pop('category', None)
            materials.pop('stock_availability', None)
            material_data.append(materials)
        order_data = {
            'order_id': order.id,
            'priority': order.priority,
            'images': order_serializer.data['images'],
            'product_name': order.product_name,
            'product_name_mal': order.product_name_mal,
            'product_description': order.product_description,
            'product_description_mal': order.product_description_mal,
            'product_length': order.product_length,
            'product_height':order.product_height,
            'product_width':order.product_width,
            'materials':material_data,
            'finish':order.finish,
            'event':order.event,
            'status': order.enquiry_status,
        }
        return JsonResponse({'data':order_data}, status=status.HTTP_200_OK)
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

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def carpenter_request_material_creation(request, order_id, carpenter_id, carpenter_request_id, material_id):
#     try:
#         carpenter_enquiry = CarpenterEnquire.objects.filter(
#             id=carpenter_request_id,
#             order_id=order_id,
#             carpenter_id=carpenter_id,
#             material_id=material_id,
#             status = 'checking'
#         ).first()
#         if not carpenter_enquiry:
#             return JsonResponse({'error': 'Carpenter Enquiry not found'}, status=404)
#         serializer = CarpenterEnquireSerializer(carpenter_enquiry, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse({'error': serializer.errors}, status=400)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
