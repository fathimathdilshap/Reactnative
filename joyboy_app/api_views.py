from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from django.middleware.csrf import get_token
from django.http import JsonResponse,Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('post_category')
        if category_id:
            return posts.objects.filter(post_category=category_id)
        return posts.objects.all()

class PostCategoryListAPIView(generics.ListAPIView):
    queryset = post_category.objects.all()
    serializer_class = PostCategorySerializer

# class BookingCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = BookingSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user  

        booking_data = {
            'user': user.id,
            'service_name': request.data.get('service_name'),
            'service_id': request.data.get('service_id'),
            'name': request.data.get('name'),
            'phone_number': request.data.get('phone_number'),
            'address': request.data.get('address'),
            'date': request.data.get('date'),
            'time': request.data.get('time'),
        }

        serializer = BookingSerializer(data=booking_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        register_data = {
            'user': user.id,
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'address': request.data.get('address'),
            'photo':request.data.get('photo'),
        }

        register_serializer = RegisterSerializer(data=register_data)
        if register_serializer.is_valid():
            register_serializer.save()
            return Response(register_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class ProfileAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        try:
            profile_instance = register.objects.get(user_id=user_id)
            user_instance = User.objects.get(id=user_id)

            profile_serializer = RegisterSerializer(profile_instance)
            user_serializer = UserSerializer(user_instance)

            serialized_data = {
                'profile': profile_serializer.data,
                'user': user_serializer.data,
            }

            return Response(serialized_data, status=status.HTTP_200_OK)

        except register.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


class CheckAuthAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'User is authenticated'}, status=status.HTTP_200_OK)


# class Booking_detailsAPIView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         user_id = request.user.id

#         try:
#             bookings = booking.objects.filter(user_id=user_id)
#             booking_serializer = BookingSerializer(bookings, many=True)

#             serialized_data = {
#                 'bookings': booking_serializer.data,
#             }
#             return Response(serialized_data, status=status.HTTP_200_OK)

#         except booking.DoesNotExist:
#             return Response({'error': 'booking not found'}, status=status.HTTP_404_NOT_FOUND)
        

class Booking_detailsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        try:
            bookings = booking.objects.filter(user_id=user_id)
            booking_serializer = BookingSerializer(bookings, many=True)

            serialized_data = {
                'bookings': booking_serializer.data,
            }
            return Response(serialized_data, status=status.HTTP_200_OK)

        except booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        booking_id = kwargs.get('booking_id')  # Assuming you have a booking_id in your URL
        try:
            booking_instance = booking.objects.get(id=booking_id)
            booking_instance.delete()
            return Response({'message': 'Booking deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('oldpassword')
        new_password = request.data.get('newpassword')
        confirm_password = request.data.get('conformpassword')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Important to keep the user logged in

        return Response({'success': 'Password updated successfully.'}, status=status.HTTP_200_OK)
    


class TurfAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TurfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
      
    
class TurfListCreateView(generics.ListCreateAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer    

class TurfRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer


class EditprofileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            user_edit = User.objects.get(id=user_id)
            
            try:
                profile_edit = register.objects.get(user_id=user_id)
            except register.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
            edituser_data = {
                'id': user_edit.id,
                'username': request.data.get('username')
            }
            editprofile_data={
                'user':request.user.id,
                'name':request.data.get('name'),
                'email':request.data.get('email'),
                'address': request.data.get('address'),
                'photo':request.data.get('photo'),
            }
            profileserilizer=RegisterSerializer(instance=profile_edit, data=editprofile_data)
            userserializer = UserSerializer(instance=user_edit, data=edituser_data)
            if userserializer.is_valid():
                userserializer.save()
                print('ok')
            if profileserilizer.is_valid():
                profileserilizer.save()
                return Response(userserializer.data, status=status.HTTP_200_OK)
            else:
                print('Validation errors:', profileserilizer.errors)
                return Response(userserializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error in post request: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class TurfUpdateAPIView(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
            turf = Turf.objects.get(id=id)
            turf.name = request.data.get('name', turf.name)
            turf.location = request.data.get('location', turf.location)
            turf.photo = request.data.get('photo', turf.photo)
            turf.save()
            serializer = TurfSerializer(turf)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Turf.DoesNotExist:
            return Response({'error': 'Turf not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in put request: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class DeleteserviceAPIView(APIView):

    def post(self, request, *args, **kwargs):
        service_id = request.data.get('service_id')

        try:
            # Use get_object_or_404 to raise a 404 response if the service doesn't exist
            edit = get_object_or_404(Turf, id=service_id)
            edit.delete()
            return JsonResponse({'message': 'Service deleted successfully'})
        except Turf.DoesNotExist:
            return JsonResponse({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TurfAPIView(APIView):
    def post(self, request, *args, **kwargs):
        da=request.data
        print(da)
        user = request.user  

        addservice_data = {
            'user': user.id,
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'photo': request.FILES.get('photo'),
            'amount': request.FILES.get('amount'),

            
        }

        serializer = TurfSerializer(data=addservice_data)
        if serializer.is_valid():
            service_instance = serializer.save()
            print(f'Service ID: {service_instance.id}')

            multi_photos = [value for key, value in request.FILES.items() if key.startswith('multiPhotos')]
            print(f'Multi Photos: {multi_photos}')
            for img in multi_photos:
                multimage_data = {
                    'turf_id': service_instance.id, 
                    'image': img,
                }
                multimage_serializer = TurfmultiimageSerializer(data=multimage_data)

                if multimage_serializer.is_valid():
                    multimage_serializer.save()
                else:
                    print(f'Multimage Serializer Errors: {multimage_serializer.errors}')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        