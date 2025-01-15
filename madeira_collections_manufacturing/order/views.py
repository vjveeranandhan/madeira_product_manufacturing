from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order, OrderImage
from .OrderSerializer import OrderSerializer, OrderImageSerializer
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
        data = request.data
        print(data)
        reference_images = request.FILES.getlist('reference_image') 
        data.pop('reference_image', None)
        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            order_obj = Order.objects.filter(id=serializer.data['id']).first()
            for image in reference_images:
                order_image = OrderImage.objects.create(
                    image = image,
                    order = order_obj
                )
                order_image.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

# List all orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request, order_status):
    try:
        orders = Order.objects.filter(status= order_status)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_order(request, pk):
    try:
        order = Order.objects.filter(pk=pk).first()
        order_serializer = OrderSerializer(order)
        carpenter_enquiry = CarpenterEnquire.objects.filter(order_id=order.id)
        main_manager = CustomUser.objects.filter(id=order.main_manager_id.id)
        manager_serialized = UserSerializer(main_manager, many= True)
        carpenter = CustomUser.objects.filter(id=order.carpenter_id.id)
        carpenter_serialized = UserSerializer(carpenter, many= True)
        images = OrderImage.objects.filter(order= pk).all()
        image_serilized = OrderImageSerializer(images, many=True)
        
        material_list = []
        for material in order.material_ids.all():
            material_data = Material.objects.get(id = material.id)
            serialized_material =  MaterialSerializer(material_data)
            material_list.append(serialized_material.data)

        # carpenter_enq_data = {}
        carpenter_data = []
        for carpenter_enquiry_item in carpenter_enquiry:
            carpenter_enquiry_serializer = CarpenterEnquireSerializer(carpenter_enquiry_item)
            carpenter_data.append(carpenter_enquiry_serializer.data)
        
        #Current process data
        process_details = ProcessDetails.objects.filter(order_id=pk).first()
        if process_details:
            process_details_serialized = ProcessDetailsSerializer(process_details)

            workers_list=[]
            for worker in process_details.process_workers_id.all():
                worker_obj = CustomUser.objects.get(id=worker.id)
                worker_serialized = UserSerializer(worker_obj)
                workers_list.append(worker_serialized.data)

            process_materials = ProcessMaterials.objects.filter(process_details_id = process_details_serialized.data['id'])
            
            process_material_dict = {}
            current_process_materials=[]
            for process_material in process_materials:
                material_data = Material.objects.get(id = process_material.material_id.id)
                process_material_dict['process_material_id'] = process_material.material_id.id
                process_material_dict['material_id'] = material_data.id
                process_material_dict['material_name'] = material_data.name
                process_material_dict['material_quantity'] = process_material.quantity
                process_material_dict['material_price'] = material_data.price
                process_material_dict['total_price'] = process_material.total_price
                current_process_materials.append(process_material_dict)

            process = Process.objects.get(id= order.order_stage_id.id)
            process_serialised = ProcessSerializer(process)

            current_process = {
                    'process': process_serialised.data,
                    'process_details': process_details_serialized.data,
                    'process_materials': current_process_materials,
                    'workers_list': workers_list
            }
            return Response({'order_data': order_serializer.data,
                            # 'images': image_serilized.data,
                        'materials': material_list,
                        'carpenter_enquiry_data': carpenter_data,
                        'main_manager': manager_serialized.data,
                        'carpenter': carpenter_serialized.data,
                        'current_process': current_process
                        },
                            status=status.HTTP_200_OK)
        return Response({   'order_data': order_serializer.data,
                            # 'images': image_serilized.data,
                            'main_manager': manager_serialized.data,
                            'materials': material_list,
                            'carpenter': carpenter_serialized.data,
                            'carpenter_enquiry_data': carpenter_data,
                        #   'current_process': current_process
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
        if order.status != 'enquiry' and order.enquiry_status != 'Initiated':
            return Response({'error': 'Order is confirmed can\'t modify it'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            reference_images = request.FILES.getlist('reference_image')
            if reference_images:
                images = OrderImage.objects.filter(order= order.id)
                images.delete()
                for image in reference_images:
                    order_image = OrderImage.objects.create(
                        image = image,
                        order = order
                    )
                    order_image.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

# Delete an order
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    try:
        order = Order.objects.filter(pk=pk).first()
        if order.status != 'enquiry' and order.enquiry_status != 'Initiated':
            return Response({'error': 'Order is confirmed can\'t delete it'}, status=status.HTTP_400_BAD_REQUEST)
        order.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

#----------------Carpenter Request------------------------------

# Create a new order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_carpenter_request(request, order_id):
    try:
        order = Order.objects.filter(id = order_id).first()    
        serializer = OrderSerializer(data=order)
        for material_id in serializer.data['material_ids']:
            material_instance = Material.objects.filter(id=int(material_id)).first()
            CarpenterEnquire.objects.create(
                order_id=order,
                material_id=material_instance,
                carpenter_id=serializer.data['carpenter_id'],
                status='requested'
            )
        order.enquiry_status = 'requested'
        order.save()
        return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

#----------------Main Manager API's-----------------------------

# Retrieve manager order list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_manager_orders(request, manager_id, order_status):
    try:
        orders = Order.objects.filter(main_manager_id=manager_id, status=order_status)
        if not orders.exists():
            return Response(
                {"message": "No orders found for the given manager."}, 
                status=status.HTTP_200_OK
            )
        serializer = OrderSerializer(orders, many=True)
        for order in serializer.data:
            order.pop('images', None)  # Removes 'field1' if it exists
            order.pop('estimated_price', None)
            order.pop('customer_name', None)
            order.pop('contact_number', None)
            order.pop('whatsapp_number', None)
            order.pop('email', None)
            order.pop('material_cost', None)
            order.pop('ongoing_expense', None)
            order.pop('main_manager_id', None)
            order.pop('material_ids', None)
            order.pop('carpenter_id', None)
            order.pop('current_process', None)
            order.pop('completed_processes', None)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)