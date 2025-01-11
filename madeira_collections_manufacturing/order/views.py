from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order
from .OrderSerializer import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from carpenter_work.models import CarpenterEnquire
from inventory.models import Material
from user_manager.models import CustomUser
from user_manager.serializer import UserSerializer
from django.http import JsonResponse
from carpenter_work.carpenter_enquire_serializer import CarpenterEnquireSerializer
from inventory.models import Material
from inventory.MaterialSerializer import MaterialSerializer
from process.models import ProcessDetails, ProcessMaterials
from process.models import Process
from process.ProcessSerializer import ProcessSerializer
from process.process_details_serializer import ProcessDetailsSerializer, ProcessMaterialsSerializer


# Create a new order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        data = request.data
        carpenter_id = CustomUser.objects.get(id=data['carpenter_id'])
        if serializer.is_valid():
            serializer.save()
            order = Order.objects.get(id = serializer.data['id'])
            for material_id in serializer.data['material_ids']:
                material_instance = Material.objects.get(id=material_id)
                carpenter_enquire = CarpenterEnquire.objects.create(
                order_id= order,
                material_id=material_instance,
                carpenter_id=carpenter_id,
                status='requested'
                )
                carpenter_enquire.save()            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
    
# Retrieve a single order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order_serializer = OrderSerializer(order)
        carpenter_enquiry = CarpenterEnquire.objects.filter(order_id=order.id)
        main_manager = CustomUser.objects.filter(id=order.main_manager_id.id)
        manager_serialized = UserSerializer(main_manager, many= True)
        carpenter = CustomUser.objects.filter(id=order.carpenter_id.id)
        carpenter_serialized = UserSerializer(carpenter, many= True)

        carpenter_enq_data = {}
        carpenter_data = []
        for carpenter_enquiry_item in carpenter_enquiry:
            carpenter_enquiry_serializer = CarpenterEnquireSerializer(carpenter_enquiry_item)
            carpenter_enq_data['carpenter_enquiry_item'] = carpenter_enquiry_serializer.data
            material_data = Material.objects.filter(id = carpenter_enquiry_item.material_id.id)
            serialized_material =  MaterialSerializer(material_data, many=True)
            carpenter_enq_data['material'] = serialized_material.data
            carpenter_data.append(carpenter_enq_data)
        

        #Current process data

        process_details = ProcessDetails.objects.get(order_id= pk, process_id= order.order_stage_id)
        process_details_serialized = ProcessDetailsSerializer(process_details)

        process_materials = ProcessMaterials.objects.filter(process_details_id = process_details_serialized.data['id'])
        process_materials_serialized = ProcessMaterialsSerializer(process_materials, many= True)

        process = Process.objects.get(id= order.order_stage_id.id)
        process_serialised = ProcessSerializer(process)

        current_process = {
                'process': process_serialised.data,
                'process_details': process_details_serialized.data,
                'process_materials': process_materials_serialized.data
        }

        #Completed process Details
        # completed_process_list = []
        # for process in order.completed_processes.all():
        #     process_details = ProcessDetails.objects.get(order_id= pk, process_id= order.order_stage_id)
        #     process_details_serialized = ProcessDetailsSerializer(process_details)

        #     process_materials = ProcessMaterials.objects.filter(process_details_id = process_details_serialized.data['id'])
        #     process_materials_serialized = ProcessMaterialsSerializer(process_materials, many= True)

        #     process = Process.objects.get(id= order.order_stage_id.id)
        #     process_serialised = ProcessSerializer(process)

        #     current_process = {
        #             'process': process_serialised.data,
        #             'process_details': process_details_serialized.data,
        #             'process_materials': process_materials_serialized.data
        #     }

        return Response({'order_data': order_serializer.data,
                          'carpenter_enquiry_data': carpenter_data,
                          'main_manager': manager_serialized.data,
                          'carpenter': carpenter_serialized.data,
                          'current_process': current_process
                          },
                            status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

# Update an order
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        serializer = OrderSerializer(order, data=request.data)
        carpenter_id = CustomUser.objects.get(id=request.data['carpenter_id'])
        if serializer.is_valid():
            serializer.save()
            carpenter_enquiry = CarpenterEnquire.objects.filter(order_id=order.id)
            carpenter_enquiry.delete()
            for material_id in serializer.data['material_ids']:
                material_instance = Material.objects.get(id=material_id)
                carpenter_enquire = CarpenterEnquire.objects.create(
                order_id= order,
                material_id=material_instance,
                carpenter_id=carpenter_id,
                status='requested'
                )
                carpenter_enquire.save()       
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
    
# Delete an order
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order.delete()
        carpenter_enquiry = CarpenterEnquire.objects.filter(order_id=order.id)
        carpenter_enquiry.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
    
# List all orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    try:
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)