from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import AllowAny
# from .authentication import *

class RegisterView(APIView):
    def post(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            address_data = serializer.validated_data.pop('address')
            account_data = serializer.validated_data.pop('account')
            position_data = serializer.validated_data.pop('position')

            if Account.objects.filter(username=account_data['username']).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            account_data['password'] = make_password(account_data['password'])
            address = Address.objects.create(**address_data)
            account = Account.objects.create(**account_data)
            position = Position.objects.create(**position_data)
            staff = Staff.objects.create(
                address=address,
                account=account,
                position=position,
                **serializer.validated_data
            )
            # access_token = generate_access_token(staff.id)
            # refresh_token = generate_refresh_token(staff.id)

            staff_serializer = StaffInfoSerializer(staff)

            return Response({
                'staff': staff_serializer.data,
                # 'refresh': refresh_token,
                # 'access': access_token,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.validated_data  
            # access_token = generate_access_token(staff.get('id'))
            # refresh_token = generate_refresh_token(staff.get('id'))

            staff_serializer = StaffInfoSerializer(staff)
            
            return Response({
                'staff': staff_serializer.data,
                # 'refresh': refresh_token,
                # 'access': access_token,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StaffDetailAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            staff = Staff.objects.get(id=id)
            serializer = StaffInfoSerializer(staff)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)
        

class StaffUpdateAPIView(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
            staff = Staff.objects.get(id=id)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StaffSerializer(staff, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StaffDeleteAPIView(APIView):
    def delete(self, request, id, *args, **kwargs):
        try:
            staff = Staff.objects.get(id=id)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)

        staff.delete()
        return Response({'message': f'Staff with id {id} has been successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    

class StaffSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        keywords = request.query_params.get('keywords', None)
        if not keywords:
            return Response({'error': 'Please provide keywords for search'}, status=status.HTTP_400_BAD_REQUEST)

        # Tìm kiếm nhân viên theo các trường first_name, last_name và name_position
        staff = Staff.objects.filter(
            models.Q(id__icontains=keywords) |
            models.Q(first_name__icontains=keywords) |
            models.Q(last_name__icontains=keywords) |
            models.Q(position__name__icontains=keywords)
        )
        
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class StaffLogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Thực hiện logout bằng cách gỡ bỏ session của người dùng hiện tại
        request.session.flush()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)