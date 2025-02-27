from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Process, ProcessMaterials, ProcessDetailsImage
from .ProcessSerializer import ProcessSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from process.process_details_serializer import ProcessDetailsSerializer
from process.models import ProcessDetails
from order.OrderSerializer import OrderSerializer
from order.models import Order
from user_manager.models import CustomUser
from user_manager.serializer import UserSerializer as ManagerSerializer
from user_manager.serializer import UserSerializer as WorksSerializer
from datetime import date, datetime
from .process_details_serializer import ProcessMaterialsSerializer
from django.shortcuts import get_object_or_404
from inventory.models import Material
from inventory.MaterialSerializer import MaterialSerializer

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
        if process is None:
                return JsonResponse({'error': 'Process not found'}, status=404)
        process.delete()
        return Response({"message": "Process deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Process.DoesNotExist:
        return Response({"error": "Process not found"}, status=status.HTTP_404_NOT_FOUND)

# ---------------------PROCESS DETAILS--------------------------------------------------------------    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_process_details(request, process_details_id):
    try:
        process_details = ProcessDetails.objects.filter(id=process_details_id).first()
        if process_details is None:
                return JsonResponse({'error': 'Process Details not found'}, status=404)
        process_details.delete()
        return Response({"message": "Process details deleted successfully"}, status=status.HTTP_200_OK)
    except ProcessDetails.DoesNotExist:
        return Response({"error": "Process details not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# List process details request by manager
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_process_details(request, process_manager_id):
    try:
        # Filter ProcessDetails based on process_manager_id and process_id
        process_details = ProcessDetails.objects.filter(
            process_manager_id=process_manager_id
        ).all()
        
        if not process_details.exists():
            return Response({"error": "No process details found"}, status=status.HTTP_404_NOT_FOUND)
        
        fields_to_remove = [
            # "id",
            # "product_name",
            # "product_name_mal",
            # "product_description",
            # "product_description_mal",
            "images",
            "product_length",
            "product_height",
            "product_width",
            "reference_image",
            "finish",
            "event",
            # "estimated_delivery_date",
            "estimated_price",
            "customer_name",
            "contact_number",
            "whatsapp_number",
            "email",
            "address",
            "carpenter_work_hr",
            "carpenter_work_cost",
            "carpenter_work_completion_date",
            "enquiry_status",
            "total_material_cost",
            "ongoing_expense",
            "order_stage_id",
            "main_manager_id",
            "carpenter_id",
            "material_ids",
            "carpenter_workers_id",
            "completed_processes",
            "material_cost",

        ]           
        list_data = []
        for detail in process_details:
            detail_data = {}
            # Get and serialize the related Order
            order = detail.order_id
            order_serializer = OrderSerializer(order)
            process_serializer = ProcessSerializer(detail.process_id)
            order_data = order_serializer.data
            for field in fields_to_remove:
                order_data.pop(field, None)
            detail_data['order_data'] = order_data
            detail_data['process_details'] = ProcessDetailsSerializer(detail).data
            detail_data['process']= process_serializer.data
            list_data.append(detail_data)
        
        return Response({'data': list_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API for PROCESS MANAGER to list all their process_details in a particular process and order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_process_details(request, process_details_id):
    try:
        process_details = ProcessDetails.objects.filter(
            id=process_details_id
        ).first()
        if process_details is None:
            return Response({"error": "No process details found"}, status=status.HTTP_404_NOT_FOUND)
        order = Order.objects.filter(id=process_details.order_id.id).first()
        if order is None:
            return Response({"error": "Order found"}, status=status.HTTP_404_NOT_FOUND)
        order_fields_to_remove = [
            "estimated_price",
            "customer_name",
            "contact_number",
            "whatsapp_number",
            "email",
            "address",
            "carpenter_work_hr",
            "carpenter_work_cost",
            "carpenter_work_completion_date",
            "enquiry_status",
            "total_material_cost",
            "ongoing_expense",
            "carpenter_workers_id",
            "completed_processes",
            'material_cost',
            'current_process',
            'main_manager_id',
            'carpenter_id',
            # 'material_ids',
            'reference_image'
        ]           
        detail_data = {}

         # Get and serialize the related Order
        order_serializer = OrderSerializer(order)
        order_data = order_serializer.data
        for field in order_fields_to_remove:
            order_data.pop(field, None)
        detail_data['order_data'] = order_data
        
        main_manager_fields_to_remove=[
            'salary_per_hr',
            'age',
            'date_of_birth',
            'email'
        ]
         # Get and serialize the Main Manager
        main_manager = process_details.main_manager_id
        main_manager_serializer = ManagerSerializer(main_manager)
        main_manager_data = main_manager_serializer.data
        for field in main_manager_fields_to_remove:
            main_manager_data.pop(field, None)
        detail_data['main_manager'] = main_manager_data
        
        pro_manager_fields_to_remove=[
            'workers_salary',
            'material_price',
            'total_price',
            # 'process_id',
            'image',
            'order_id',
            'main_manager_id',
            'process_manager_id',
            'process_workers_id',
        ]
        #process
        detail_data['process'] = ProcessSerializer(process_details.process_id).data
        # Serialize ProcessDetails
        detail_serializer = ProcessDetailsSerializer(process_details)
        pro_details_data = detail_serializer.data
        for field in pro_manager_fields_to_remove:
            pro_details_data.pop(field, None)
        detail_data['process_details'] = pro_details_data
        
        # Get and serialize the Process Manager
        process_manager = process_details.process_manager_id
        process_manager_serializer = ManagerSerializer(process_manager)
        process_manager_serializer_data = process_manager_serializer.data
        for field in main_manager_fields_to_remove:
            process_manager_serializer_data.pop(field, None)
        detail_data['process_manager'] = process_manager_serializer_data

        workers_fields_to_remove=[
            'salary_per_hr',
            'age',
            'date_of_birth',
            'email'
        ]
        # Get and serialize the Process Workers
        process_workers = []
        for worker_id in detail_serializer.data['process_workers_id']:
            worker_data = CustomUser.objects.get(id=worker_id)
            worker_serializer = WorksSerializer(worker_data)
            worker_serializer_data = worker_serializer.data
            for field in workers_fields_to_remove:
                worker_serializer_data.pop(field, None)
            process_workers.append(worker_serializer_data)
        detail_data['workers_data'] = process_workers

         #Product Data
        product_data = {}
        if order.product:
            product_data = MaterialSerializer(order.product).data
        detail_data['product'] = product_data

        #process materials
        process_material_obj = ProcessMaterials.objects.filter(process_details_id=process_details.id).all()
        materials_used = []
        for material in process_material_obj:
            material_dict = {}  
            material_obj = Material.objects.filter(id = material.material_id.id).first()
            material_serialized = MaterialSerializer(material_obj)
            process_material_serialized = ProcessMaterialsSerializer(material)
            material_dict['material'] = material_serialized.data
            material_dict['material_used'] = process_material_serialized.data
            materials_used.append(material_dict)
        detail_data['used_materials'] = materials_used
        return Response({'data': detail_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API for PROCESS MANAGER to Accept their process_details in a particular process and order
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_process_details(request, order_id):
    try:
        current_date = date.today()
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        process_details = ProcessDetails.objects.filter(
            order_id=order_id, process_id=order.current_process.id).first()
        process_details.process_status = 'in_progress'
        process_details.request_accepted_date = current_date
        process_details.save()
        order.current_process_status = 'on_going'
        order.status = 'on_going'
        order.save()

        serializer = ProcessDetailsSerializer(process_details)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#------------------Process Materials API's-----------------------------------

# Create a new ProcessMaterial
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_process_material(request):
    try:
        data = request.data
        material = get_object_or_404(Material, id=data['material_id'])
        if material.quantity < data['quantity']:
            return Response({"error": "Not enough material stock available."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update material price and calculate total price
        data['material_price'] = material.price
        data['total_price'] = material.price * data['quantity']

        process_details = ProcessDetails.objects.get(id=data['process_details_id'])
        process_details_material_price = process_details.material_price
        process_details_material_price+= data['total_price']
        process_details.material_price = process_details_material_price

        process_details_total_price = process_details.total_price
        process_details_total_price+= data['total_price']
        process_details.total_price = process_details_total_price
        process_details.save()
        # Save the material quantity
        material.quantity -= data['quantity']
        material.save()
        
        order = Order.objects.filter(id=process_details.order_id.id).first()
        order_ongoing_expense = order.ongoing_expense
        order_ongoing_expense += data['total_price']
        order.ongoing_expense = order_ongoing_expense
        order.save()
        serializer = ProcessMaterialsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Retrieve a specific ProcessMaterial by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_process_material(request, process_material_id):
    try:
        process_material = get_object_or_404(ProcessMaterials, id=process_material_id)
        serializer = ProcessMaterialsSerializer(process_material)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete a ProcessMaterial
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_process_material(request, process_material_id):
    try:
        process_material = get_object_or_404(ProcessMaterials, id=process_material_id)

        # Restore material stock on deletion
        material = process_material.material_id
        material.quantity += process_material.quantity
        material.save()

        material_total_price = (process_material.quantity)*(process_material.material_price)
        process_details = ProcessDetails.objects.filter(id=process_material.process_details_id.id).first()

        pd_total_price = process_details.total_price
        pd_material_price = process_details.material_price

        process_details.total_price = pd_total_price-material_total_price
        process_details.material_price = pd_material_price-material_total_price

        process_details.save()
        process_material.delete()
        return Response({"message": "Process material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Delete a ProcessMaterial
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_to_process_verification(request, process_details_id):
    try:
        reference_images = request.FILES.getlist('image')
        process_details = ProcessDetails.objects.filter(id=process_details_id).first()
        process_details.process_status = 'verification'
        order = Order.objects.filter(id=process_details.order_id.id).first()
        order.current_process_status ='verification'
        order.save()
        for image in reference_images:
                ProcessDetailsImage.objects.create(
                    image=image,
                    process_details_id=process_details
                )
        process_details.save()
        return Response({"message": "Verification send successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)