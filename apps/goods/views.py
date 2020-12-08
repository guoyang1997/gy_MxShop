from rest_framework.views import APIView
from goods.serializers import GoodsSerializer,CategorySerializer
from .models import Goods,GoodsCategory
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .filters import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class GoodsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    #默认每页显示的个数
    page_size = 12
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'page'
    #最多能显示多少页
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,  viewsets.GenericViewSet):
    '''
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve：
        获取用户详情
    '''

    #这里必须要定义一个默认的排序,否则会报错
    queryset = Goods.objects.all()
    # 分页
    pagination_class = GoodsPagination
    #序列化
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)

    # 设置filter的类为我们自定义的类
    #过滤
    filter_class = GoodsFilter
    #搜索
    search_fields = ('name', 'goods_brief', 'goods_desc')
    #排序
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

User = get_user_model()

class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名和手机都能登录
            user = User.object.get(Q(username=username)|Q(mobile=username))
            if user.check_passwork(password):
                return user
        except Exception as e:
            return None


