# from rest_framework import serializers
# from rest_framework.response import Response
# from .models import *
# from accounts.models import CustomUser
# from restaurant.models import *
# from restaurant.serializers import *


# # User Serializer


# class userSerializer(serializers.ModelSerializer):
#     restaurant = RestaurantSerializer(read_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ["id", "username", "email", "name", "phone_number", "restaurant", "about_you",
#                   "is_restaurant", "is_staff", "is_customer", "is_driver", "date_joined",]


# class categorySerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Category
#         fields = '__all__'   

# # item image serialiser
# class itemImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = itemimage
#         fields = ['id', 'name', 'image']

# # item serialiser  
# class itemSerializer(serializers.ModelSerializer):
#     # infoimage = itemImageSerializer(read_only=False, many=True)
#     category = categorySerializer(read_only=True)
#     class Meta:
#         model = Item
#         fields = ["id", "title", "slug", "price", "discount_price",
#                   "category", "summary", "description", "information",
#                   "image", "best_selling", "popular", "infoimage", "restaurant", "created_at"
#                   ]



# class ItemSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = [
#             'id', 'title', 'slug', 'price', 'discount_price', 'category', 
#             'summary', 'description', 'information', 'image', 'infoimage', 
#             'best_selling', 'popular', 'restaurant', 'created_at'
#         ]
#         read_only_fields = ['id', 'slug', 'created_at']
  
# # Address serialiser   
# class addressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = ["id", "user", "description", "phone_number", "street_address", 
#                   "apartment_address", "zip", "address_type"
#                   ]

# # Coupon Serializer
# class couponSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Coupon
#         fields = ["id", "code", "amount"]



# # Order Item Serialiser
# class orderItemSerializer(serializers.ModelSerializer):
#     # user = userSerializer(read_only=True)
#     item = itemSerializer(read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ["id", "user", "ordered", "quantity", "item"]   
        
# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = '__all__'     

# # Order Serializer
# class orderSerializer(serializers.ModelSerializer):
#     user = userSerializer(read_only=True)
#     items = orderItemSerializer(read_only=True, many=True)
#     total = serializers.SerializerMethodField()
#     shipping_address = AddressSerializer()
#     coupon = couponSerializer()
#     class Meta:
#         model = Order
#         fields = [ 'id', 'user', 'items', 'total', 'canceled', 'shipping_address', 'ref_code', 'start_date', 'ordered',
#                   'ordered_date', 'coupon', 'being_delivered', 'received', 'refund_requested', 'refund_granted', 'slug']
    
#     def get_total(self, obj):
#         return obj.get_total()
    


# class orderUpdateSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#     items = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
#     shipping_address = serializers.PrimaryKeyRelatedField(read_only=True)
#     coupon = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'items',  'canceled', 'shipping_address', 'ref_code', 'start_date', 'ordered',
#                   'ordered_date', 'coupon', 'being_delivered', 'received', 'refund_requested', 'refund_granted', 'slug']

#     def update(self, instance, validated_data):
#         # Update the instance with the validated data
#         instance.ref_code = validated_data.get('ref_code', instance.ref_code)
#         instance.ordered = validated_data.get('ordered', instance.ordered)
#         instance.ordered_date = validated_data.get('ordered_date', instance.ordered_date)
#         instance.being_delivered = validated_data.get('being_delivered', instance.being_delivered)
#         instance.received = validated_data.get('received', instance.received)
#         instance.refund_requested = validated_data.get('refund_requested', instance.refund_requested)
#         instance.refund_granted = validated_data.get('refund_granted', instance.refund_granted)
#         instance.slug = validated_data.get('slug', instance.slug)
#         instance.canceled = validated_data.get('canceled', instance.canceled)
#         instance.save()
#         return instance


# # Refund Serializer
# class refundSerializer(serializers.ModelSerializer):
#     order = orderSerializer(read_only=True)
#     class Meta:
#         model = Refund
#         fields = ['id', 'reason', 'order', 'accepted', 'email']
        
        
        

# class RestaurantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Restaurant
#         fields = [
#             'id', 'name', 'logo', 'banner', 'description', 'short_description',
#             'size', 'is_verified', 'is_premium', 'location', 'school', 'is_banned',
#             'is_open', 'business_category', 'slug', 'date_created'
#         ]

# class CustomUserSerializer(serializers.ModelSerializer):
#     restaurant = RestaurantSerializer()

#     class Meta:
#         model = CustomUser
#         fields = [
#             'id', 'email', 'username', 'name', 'phone_number', 'about_you', 
#             'is_restaurant', 'is_admin', 'is_staff', 'is_customer', 'is_driver', 
#             'is_active', 'date_joined', 'is_available', 'time_available', 
#             'affiliate_code', 'is_affiliate', 'restaurant'
#         ]        