from django.urls import path,include,re_path
import xadmin
from django.views.static import serve
from MxShop.settings import MEDIA_ROOT
# from goods.view_base import GoodsListView
from rest_framework.documentation import include_docs_urls
from goods.views import GoodsListViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from trade.views import ShoppingCartViewset, OrderViewset
from users.views import SmsCodeViewSet, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset

router = DefaultRouter()

#配置goods的url
router.register(r'goods', GoodsListViewSet, basename='goods')
#配置goods的url
router.register(r'users', UserViewset, basename='users')
# 配置Category的url
router.register(r'categorys', CategoryViewSet, basename="categorys")
# 配置codes的url
router.register(r'code', SmsCodeViewSet, basename="code")
# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, basename="userfavs")
# 配置用户留言的url
router.register(r'messages', LeavingMessageViewset, basename="messages")
# 配置收货地址
router.register(r'address', AddressViewset, basename="address")
# 配置购物车的url
router.register(r'shopcarts', ShoppingCartViewset, basename='shopcarts')
# 配置订单的url
router.register(r'orders', OrderViewset, basename="orders")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # token
    # path('api-token-auth/', views.obtain_auth_token),
    # jwt的token认证接口
    path('login/', obtain_jwt_token),
    # path('jwt-auth/', obtain_jwt_token),

    path('ueditor/', include('DjangoUeditor.urls')),
    #文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    #drf文档，title自定义
    path('docs', include_docs_urls(title='仙剑奇侠传')),
    #商品列表页
    re_path('^', include(router.urls)),
]
