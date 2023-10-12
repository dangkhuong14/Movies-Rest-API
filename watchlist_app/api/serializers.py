from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    # source là core argument dùng để populate giá trị của serializer field
    # Khai báo ReadOnlyField cho field watchlist của Review là vì:
    # không cho phép người dùng thay đổi nội dung và không yêu cầu nhập
    # field này khi request
    # watchlist = serializers.ReadOnlyField(
    #     source='watchlist.pk', required=False)

    # source argument dùng để khai báo giá trị custom cho field
    watchlist = serializers.StringRelatedField(
        read_only=True, required=False, source='watchlist.pk')

    # Không khai báo review_user field cho serializer class cũng được
    # nhưng kết quả trả về sẽ là PK của instance User
    # Không thêm tham số source cũng được kết quả vẫn là user name (__str__ của user model)
    review_user = serializers.StringRelatedField(
        read_only=True, required=False, source='review_user.username')

    class Meta:
        model = Review
        fields = '__all__'
        # exclude = ('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    # Related name cua Model
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     # Name cua URLs.py
    #     view_name='watch-detail'
    # )

    class Meta:
        model = StreamPlatform
        fields = '__all__'

# class MovieSerializer(serializers.ModelSerializer):
#     # Thêm các trường custom để tính toán và response client
#     name_len = serializers.SerializerMethodField()

#     class Meta:
#         model = Movie
#         fields = '__all__'
#         # fields = ['id', 'name', 'description']
#         # exclude = ['active']

#     # Định nghĩa Method cho custom field:
#     def get_name_len(self, obj):
#         return len(obj.name)

#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('Name is too short!')
#         else:
#             return value

#     def validate_description(self, value):
#         if len(value) < 5:
#             raise serializers.ValidationError('Description is too short!')
#         else:
#             return value

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 'Name and description should not be the same!')
#         else:
#             return data

# def description_length(value):
#     if len(value) < 5:
#         raise serializers.ValidationError('Description is too short!')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[description_length])
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get('active')
#         # Neu model da ton tai trong db thi ham save() se tao UPDATE statement nguoc lai se tao INSERT statement
#         instance.save()
#         return instance

#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('Name is too short!')
#         else:
#             return value

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 'Name and description should not be the same!')
#         else:
#             return data
