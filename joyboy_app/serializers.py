from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = post_category
        fields = '__all__'  
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts
        fields = '__all__'
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = booking
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = register
        fields = ['user', 'address', 'email', 'name','photo']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Make password write-only

    class Meta:
        model = User
        fields = ['id','username', 'password']

    def create(self, validated_data):
        # Create a new user with a hashed password
        user = User.objects.create_user(**validated_data)
        return user
 
 
class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = '__all__'



class TurfsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = '_all_'   
             
    def update(self, instance, validated_data):
        # Update specific fields based on the validated_data
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        # You can add more fields to update as needed

        instance.save()
        return instance

class TurfmultiimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = '__all__'