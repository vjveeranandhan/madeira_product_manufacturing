from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Process, ProcessMaterials
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

# ---------------------PROCESS DETAILS--------------------------------------------------------------
# Create process details by ADDING a new order to a process
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_process_details(request):
    try:
        data = request.data
        print(data)
        if ProcessDetails.objects.filter(order_id = data['order_id'], process_id = data['process_id']).exists():
            return Response({"error": 'Order is already added to the process '}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProcessDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_process_details(request, id):
    try:
        process_details = ProcessDetails.objects.get(id=id)
        process_details.delete()
        
        return Response({"message": "Process details deleted successfully"}, status=status.HTTP_200_OK)
    except ProcessDetails.DoesNotExist:
        return Response({"error": "Process details not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def retrieve_process_details(request, process_details_id):
#     try:
#         process_details = ProcessDetails.objects.get(pk=process_details_id)
#         if not process_details:
#             return Response({"error": "No process details found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProcessDetailsSerializer(process_details)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API for PROCESS MANAGER to list all there process_details in a particular process
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_process_details(request, process_manager_id, process_id):
    try:
        # Filter ProcessDetails based on process_manager_id and process_id
        process_details = ProcessDetails.objects.filter(
            process_manager_id=process_manager_id,
            process_id=process_id
        )
        
        if not process_details.exists():
            return Response({"error": "No process details found"}, status=status.HTTP_404_NOT_FOUND)
        
        list_data = []
        fields_to_remove = [
            # "id",
            # "product_name",
            # "product_name_mal",
            # "product_description",
            # "product_description_mal",
            # "product_length",
            # "product_height",
            # "product_width",
            # "reference_image",
            # "finish",
            # "event",
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
            # "order_stage_id",
            # "main_manager_id",
            # "carpenter_id",
            # "material_ids",
            "carpenter_workers_id",
            "completed_processes"
        ]           

        for detail in process_details:
            detail_data = {}
            
            # Serialize ProcessDetails
            detail_serializer = ProcessDetailsSerializer(detail)
            detail_data['process_details'] = detail_serializer.data
            
            # Get and serialize the related Order
            order = detail.order_id
            order_serializer = OrderSerializer(order)
            order_data = order_serializer.data
            for field in fields_to_remove:
                order_data.pop(field, None)
            detail_data['order_data'] = order_data
            
            # Get and serialize the Process Manager
            process_manager = detail.process_manager_id
            process_manager_serializer = ManagerSerializer(process_manager)
            detail_data['process_manager'] = process_manager_serializer.data
            
            # Get and serialize the Main Manager
            main_manager = detail.main_manager_id
            main_manager_serializer = ManagerSerializer(main_manager)
            detail_data['main_manager'] = main_manager_serializer.data

            # Get and serialize the Process Workers
            process_workers = []
            for worker_id in detail_serializer.data['process_workers_id']:
                worker_data = CustomUser.objects.get(id=worker_id)
                worker_serializer = WorksSerializer(worker_data)
                process_workers.append(worker_serializer.data)
            detail_data['workers_data'] = process_workers
            list_data.append(detail_data)
        
        return Response({'data': list_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API for PROCESS MANAGER to list all their process_details in a particular process and order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_process_details(request, process_manager_id, process_id, order_id):
    try:
        # Filter ProcessDetails based on process_manager_id, process_id, and order_id
        process_details = ProcessDetails.objects.filter(
            process_manager_id=process_manager_id,
            process_id=process_id,
            order_id=order_id
        )
        
        if not process_details.exists():
            return Response({"error": "No process details found for the given parameters"}, status=status.HTTP_404_NOT_FOUND)
        
        list_data = []
        fields_to_remove = [
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
            "completed_processes"
        ]           

        for detail in process_details:
            detail_data = {}
            
            # Serialize ProcessDetails
            detail_serializer = ProcessDetailsSerializer(detail)
            detail_data['process_details'] = detail_serializer.data
            
            # Get and serialize the related Order
            order = detail.order_id
            order_serializer = OrderSerializer(order)
            order_data = order_serializer.data
            for field in fields_to_remove:
                order_data.pop(field, None)
            detail_data['order_data'] = order_data
            
            # Get and serialize the Process Manager
            process_manager = detail.process_manager_id
            process_manager_serializer = ManagerSerializer(process_manager)
            detail_data['process_manager'] = process_manager_serializer.data
            
            # Get and serialize the Main Manager
            main_manager = detail.main_manager_id
            main_manager_serializer = ManagerSerializer(main_manager)
            detail_data['main_manager'] = main_manager_serializer.data

            # Get and serialize the Process Workers
            process_workers = []
            for worker_id in detail_serializer.data['process_workers_id']:
                worker_data = CustomUser.objects.get(id=worker_id)
                worker_serializer = WorksSerializer(worker_data)
                process_workers.append(worker_serializer.data)
            detail_data['workers_data'] = process_workers
            list_data.append(detail_data)
        
        return Response({'data': list_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API for PROCESS MANAGER to Accept their process_details in a particular process and order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_process_details(request, process_manager_id, process_id, order_id):
    try:
        process_details = ProcessDetails.objects.get(
            process_manager_id=process_manager_id,
            process_id=process_id,
            order_id=order_id,
            process_status='requested'
        )
        if not process_details:
            return Response({"error": "No process details found for the given parameters"}, status=status.HTTP_404_NOT_FOUND)
        
        process_details.process_status = 'in_progress'
        workers_ids = process_details.process_workers_id.all()

        current_date = date.today()
        number_of_working_days = (process_details.expected_completion_date - current_date).days
        workers_cost = 0
        
        for worker in workers_ids:
            worker_data = CustomUser.objects.get(id=worker.id)
            worker_serializer = WorksSerializer(worker_data)
            process_workers_data = worker_serializer.data
            total_work_hrs = number_of_working_days*8
            workers_cost+= total_work_hrs*process_workers_data['salary_per_hr']
        process_manager_data = CustomUser.objects.get(id=process_details.process_manager_id.id)
        process_manager_serializer = ManagerSerializer(process_manager_data)

        process_manager_data = process_manager_serializer.data
        workers_cost+=total_work_hrs*process_manager_data['salary_per_hr']

        process_details.workers_salary = workers_cost
        process_details.total_price += workers_cost
        process_details.save()
        order = Order.objects.get(id=order_id)
        process = Process.objects.get(id=process_id)
        order.order_stage_id = process
        process_work_expense = order.ongoing_expense
        process_work_expense += workers_cost
        order.ongoing_expense = process_work_expense
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
        
        # Check if the material exists
        material = get_object_or_404(Material, id=data['material_id'])

        # Validate the requested quantity
        if material.quantity < data['quantity']:
            return Response({"error": "Not enough material stock available."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update material price and calculate total price
        data['material_price'] = material.price
        data['total_price'] = material.price * data['quantity']

        print(data)

        process_details = ProcessDetails.objects.get(id=data['process_details_id'])
        process_details_material_price = process_details.material_price
        process_details_material_price+= material.price*data['quantity']
        process_details.material_price = process_details_material_price

        process_details_total_price = process_details.total_price
        process_details_total_price+= process_details.material_price*data['quantity']
        process_details.total_price = process_details_total_price
        process_details.save()
        # Save the material quantity
        material.quantity -= data['quantity']
        material.save()
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


# Update a ProcessMaterial
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_process_material(request, process_material_id):
    try:
        process_material = get_object_or_404(ProcessMaterials, id=process_material_id)
        data = request.data

        # Validate new quantity if it's provided
        if 'quantity' in data:
            material = process_material.material_id
            new_quantity = int(data['quantity'])
            quantity_diff = new_quantity - process_material.quantity

            if material.quantity < quantity_diff:
                return Response({"error": "Not enough material stock available."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update material stock
            material.quantity -= quantity_diff
            material.save()
        
            # Update total price
            data['total_price'] = material.price * new_quantity

        serializer = ProcessMaterialsSerializer(process_material, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

        process_material.delete()
        return Response({"message": "Process material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)