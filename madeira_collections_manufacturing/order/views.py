from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import date
from .models import Order, OrderImage
from .OrderSerializer import OrderSerializer, OrderImageSerializer, OrderCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from carpenter_work.models import CarpenterEnquire
from inventory.models import Material
from user_manager.models import CustomUser
from user_manager.serializer import UserSerializer, CustomUserSerializer, UserRetrieveSerializer
from django.http import JsonResponse
from carpenter_work.carpenter_enquire_serializer import CarpenterEnquireSerializer
from inventory.models import Material
from inventory.MaterialSerializer import MaterialSerializer
from process.models import ProcessDetails, ProcessMaterials
from process.models import Process
from process.ProcessSerializer import ProcessSerializer
from process.process_details_serializer import ProcessDetailsSerializer, ProcessMaterialsSerializer
from inventory.models import InventoryCategory, Material
from inventory.InventoryCategorySerializer import InventoryCategorySerializer
from inventory.MaterialSerializer import MaterialSerializer
from process.ProcessSerializer import ProcessSerializer
from user_manager.serializer import UserSerializer

# Create a new order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        data = request.data.copy() 
        reference_images = request.FILES.getlist('reference_image') 
        data.pop('reference_image', None)
        serializer = OrderCreateSerializer(data=data)
        print(reference_images)
        if serializer.is_valid():
            order_obj = serializer.save()
            for image in reference_images:
                OrderImage.objects.create(
                    image=image,
                    order=order_obj
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

# List all orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request, order_status):
    try:
        orders = Order.objects.filter(status= order_status).all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_order(request, order_id):
    try:
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order_serializer = OrderSerializer(order)
        carpenter_enquiry = CarpenterEnquire.objects.filter(order_id=order.id).all()
        main_manager = CustomUser.objects.filter(id=order.main_manager_id.id).first()
        manager_serialized = UserSerializer(main_manager)
        carpenter = CustomUser.objects.filter(id=order.carpenter_id.id).first()
        carpenter_serialized = UserSerializer(carpenter)

        material_list = []
        material_ids = order_serializer.data['material_ids']
        for material_id in material_ids:
            material_data = Material.objects.get(id = material_id)
            serialized_material =  MaterialSerializer(material_data)
            material_list.append(serialized_material.data)

        carpenter_data = {}
        carpenter_data['carpenter_user'] = carpenter_serialized.data
        carpenter_data_list = []
        for carpenter_enquiry_item in carpenter_enquiry:
            carpenter_enquiry_serializer = CarpenterEnquireSerializer(carpenter_enquiry_item)
            carpenter_data_list.append(carpenter_enquiry_serializer.data)
        carpenter_data['carpenter_data']=carpenter_data_list
        
#------------------Completed Process Data-----------------------------------------------------
        completed_process_list = []
        completed_process_dict = {}
        materials_list = []
        if order.completed_processes:
            for completed_process in order.completed_processes.all():
                process_obj = Process.objects.filter(id = completed_process.id).first()
                process_serializer = ProcessSerializer(process_obj)
                completed_process_dict['completed_process'] = process_serializer.data
                process_details_obj =  ProcessDetails.objects.filter(order_id = order_id, process_id=process_serializer.data["id"]).first()
                process_details_serializer = ProcessDetailsSerializer(process_details_obj)
                completed_process_dict['completed_process_details'] = process_details_serializer.data
                #----- Material Data--------------------------
                process_materials_obj = ProcessMaterials.objects.filter(process_details_id = process_details_serializer.data['id']).all()
                material_dict = {}
                for material in process_materials_obj:
                    serialized_material = ProcessMaterialsSerializer(material)
                    materials_obj = Material.objects.filter(id=serialized_material.data['material_id']).first()
                    materials_obj_serializer = MaterialSerializer(materials_obj)
                    material_dict['completed_material_details']=materials_obj_serializer.data
                    material_dict['completed_material_used_in_process']=serialized_material.data
                    materials_list.append(material_dict)
                    material_dict={}
                completed_process_dict['materials_used'] = materials_list
                completed_process_list.append(completed_process_dict)

                workers_list=[]
                for worker in process_details_obj.process_workers_id.all():
                    worker_obj = CustomUser.objects.get(id=worker.id)
                    worker_serialized = CustomUserSerializer(worker_obj)
                    workers_list.append(worker_serialized.data)
                process_manager_obj = CustomUser.objects.filter(id=process_details_obj.process_manager_id.id).first()
                process_manager_serialized = CustomUserSerializer(process_manager_obj)
                workers_list.append(process_manager_serialized.data)
                completed_process_dict['workers_data']=workers_list

#----------------Current Process Data---------------------------------------------------------------------------------
        current_process_dict = {}
        if order.current_process:
            current_process_obj=Process.objects.filter(id = order.current_process.id).first()
            current_process_serializer = ProcessSerializer(current_process_obj)
            current_process_dict['current_process'] = current_process_serializer.data
            process_details = ProcessDetails.objects.filter(order_id = order_id, process_id=order.current_process.id).first()
            current_process_material_list=[]
            if process_details:
                current_process_details_serializer = ProcessDetailsSerializer(process_details)
                current_process_dict['current_process_details'] = current_process_details_serializer.data
                current_process_materials_obj = ProcessMaterials.objects.filter(process_details_id = current_process_details_serializer.data['id']).all()
                current_process_material_dict = {}
                for material in current_process_materials_obj:
                    serialized_material = ProcessMaterialsSerializer(material)
                    materials_obj = Material.objects.filter(id=serialized_material.data['material_id']).first()
                    materials_obj_serializer = MaterialSerializer(materials_obj)
                    current_process_material_dict['current_material_details']=materials_obj_serializer.data
                    current_process_material_dict['current_material_used_in_process']=serialized_material.data
                    current_process_material_list.append(current_process_material_dict)
                    current_process_material_dict={}
                current_process_dict['current_process_materials_used'] = current_process_material_list
                
                workers_list=[]
                for worker in process_details.process_workers_id.all():
                    worker_obj = CustomUser.objects.get(id=worker.id)
                    worker_serialized = CustomUserSerializer(worker_obj)
                    workers_list.append(worker_serialized.data)
                process_manager_obj = CustomUser.objects.filter(id=process_details.process_manager_id.id).first()
                process_manager_serialized = CustomUserSerializer(process_manager_obj)
                workers_list.append(process_manager_serialized.data)
                current_process_dict['current_process_workers'] = workers_list
        number_of_processes = Process.objects.count()
        completed_process = order.completed_processes.count()
        return Response({   'order_data': order_serializer.data,
                            'main_manager': manager_serialized.data,
                            'materials': material_list,
                            'carpenter_enquiry_data': carpenter_data,
                            'completed_process_data': completed_process_list,
                            'current_process': current_process_dict,
                            'completion_percentage': (completed_process/number_of_processes)*100
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
        if not order:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

#----------------Carpenter Request------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_carpenter_request(request, order_id):
    try:
        order = Order.objects.filter(id = order_id).first()    
        if order is None:
            return JsonResponse({'error': 'Order not found'}, status=404)
        for material_id in order.material_ids.all():
            material_instance = Material.objects.filter(id=int(material_id.id)).first()
            CarpenterEnquire.objects.create(
                order_id=order,
                material_id=material_instance,
                carpenter_id=order.carpenter_id,
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
            order.pop('images', None) 
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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_to_process(request):
    try:
        data = request.data
        if 'order_id' in data:
            order = Order.objects.filter(id = data['order_id']).first()
            if order is None:
                return JsonResponse({'error': 'Order not found'}, status=404)
            if order.enquiry_status != 'completed':
                return JsonResponse({'error': 'Carpenter enquiry is not completed'}, status=404)
            if order.current_process_status != 'initiated' and order.current_process_status != 'completed':
                return JsonResponse({'error': 'Previous process is not completed'}, status=404)
            data['main_manager_id'] = order.main_manager_id.id
        else:
            return JsonResponse({'error': 'Order id is missing'}, status=404)
        if ProcessDetails.objects.filter(order_id = data['order_id'], process_id = data['process_id']).exists():
            return Response({"error": 'Order is already added to the process '}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProcessDetailsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            order.current_process_status= 'requested'
            process_obj =  Process.objects.filter(id=data['process_id']).first()
            order.current_process = process_obj
            order.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_order_creation_data(request):
    """
    Get all necessary data for creating an order:
    - Categories
    - Materials
    - Processes
    - Managers
    """
    try:
        print("get_order_creation_data")
        # Get all active categories
        categories = InventoryCategory.objects.all()
        categories_data = InventoryCategorySerializer(categories, many=True).data

        # Get all active materials
        materials = Material.objects.all()
        materials_data = MaterialSerializer(materials, many=True).data

        # Get all active processes
        processes = Process.objects.all()
        processes_data = ProcessSerializer(processes, many=True).data

        # Get all managers
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        user_data = serializer.data

        response_data = {
            'categories': categories_data,
            'materials': materials_data,
            'processes': processes_data,
            'managers': user_data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
#-------------------------------Main manager verification API's------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verification_process_list(request, manager_id):
    try:
        orders = Order.objects.filter(main_manager_id=manager_id, current_process_status='verification').all()
        if not orders.exists():
            return Response(
                {"message": "No orders found for the given managers."}, 
                status=status.HTTP_200_OK
            )
        serializer = OrderSerializer(orders, many=True)
        for order in serializer.data:
            order.pop('images', None) 
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
            order.pop('completed_processes', None)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verification_process_view(request, order_id):
    try:
        orders = Order.objects.filter(id=order_id).first()
        if not orders:
            return Response(
                {"message": "No orders found for the given managerss."}, 
                status=status.HTTP_200_OK
            )
        serializer = OrderSerializer(orders)
        order=serializer.data
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

        process = Process.objects.filter(id=orders.current_process.id).first()
        process_details = ProcessDetails.objects.filter(order_id = orders.id,process_id=orders.current_process.id).first()
        process_materials = ProcessMaterials.objects.filter(process_details_id= process_details.id).all()

        process_serializer =ProcessSerializer(process)
        process_details_serializer = ProcessDetailsSerializer(process_details)
        process_materials_serializer = ProcessMaterialsSerializer(process_materials, many=True)
        material_data = {}
        material_list = []
        for material in process_materials_serializer.data:
            material_obj = Material.objects.filter(id = material['material_id']).first()
            material_serializer = MaterialSerializer(material_obj)
            material_data=material
            material_data['material']=material_serializer.data
            material_list.append(material_data)
        return Response({'data':{
            'order_data': order,
            'process': process_serializer.data,
            'process_details': process_details_serializer.data,
            'materials': material_list
        }}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Accept the completion request of a process

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def verification_process_view_accept(request, process_details_id):
    try:
        process_details_obj = ProcessDetails.objects.filter(id= process_details_id).first()
        if not process_details_obj:
            return Response(
                {"message": "Process Details not found."}, 
                status=status.HTTP_200_OK
            )
        if process_details_obj.process_status != 'verification':
            return Response(
                {"message": "Process Details not available for verification"}, 
                status=status.HTTP_200_OK
            )
        order_obj = Order.objects.filter(id=process_details_obj.order_id.id).first()
        if not order_obj:
            return Response(
                {"message": "Order not found."}, 
                status=status.HTTP_200_OK
            )
        completion_date = date.today()
        started_date = process_details_obj.request_accepted_date
        hrs = 8
        days = 1
        total_working_hrs = 8
        if started_date == completion_date:
            total_working_hrs = 8
        else:
            days = (completion_date - started_date).days
            total_working_hrs = days * hrs
        
        work_expense = 0
        for workers in process_details_obj.process_workers_id.all():
            worker_obj = CustomUser.objects.filter(id=workers.id).first()
            worker_serializer = CustomUserSerializer(worker_obj)
            user_data = worker_serializer.data
            work_expense += user_data['salary_per_hr'] * total_working_hrs

        process_manager_id = CustomUser.objects.filter(id=process_details_obj.process_manager_id.id).first()
        process_manager_serializer = CustomUserSerializer(process_manager_id)
        process_manager_data = process_manager_serializer.data
        work_expense += process_manager_data['salary_per_hr'] * total_working_hrs

        process_details_obj.workers_salary = work_expense
        # process_details_obj.total_price += work_expense
        process_details_obj.process_status = 'completed'
        process_details_obj.completion_date = completion_date
        process_details_obj.save()

        order_obj = Order.objects.filter(id=process_details_obj.order_id.id).first()
        # order_obj.ongoing_expense += work_expense
        order_obj.current_process_status = 'completed'
        on_going_expense = order_obj.ongoing_expense
        on_going_expense+=work_expense
        order_obj.ongoing_expense = on_going_expense
        order_obj.completed_processes.add(process_details_obj.process_id)
        order_obj.save()
        return Response({'data':{"Success"}}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def complete_order(request, order_id):
    try:
        order = Order.objects.filter(id=order_id).first()
        if order.current_process_status != 'completed':
            return Response({'error': 'Current process is not completed!'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        order.status = 'completed'
        order.save()
        return Response({'data': 'Order completed'}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
