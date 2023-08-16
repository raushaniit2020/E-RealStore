from re import template
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetConfirmForm, MyPasswordResetForm
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    path('customerregistration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='realstore/login.html', authentication_form=LoginForm), name='login'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='realstore/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/changepassworddone/'), name='changepassword'),
    path('changepassworddone/', auth_views.PasswordChangeDoneView.as_view(template_name='realstore/passwordchangedone.html'), name='changepassworddone'),
    path('resetpassword/', auth_views.PasswordResetView.as_view(template_name='realstore/resetpassword.html', form_class = MyPasswordResetForm), name='resetpassword'),

    path('resetpassword/done/', auth_views.PasswordResetDoneView.as_view(template_name='realstore/resetpassword_done.html'), name='password_reset_done'),

    path('resetpassword/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='realstore/resetpassword_confirm.html', form_class = MyPasswordResetConfirmForm), name='password_reset_confirm'),

    path('resetpassword/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='realstore/resetpassword_complete.html'), name='password_reset_complete'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add-to-cart/', views.addToCart, name='add-to-cart'),
    path('cart/', views.ShowCart, name='showcart'), 
    path('orders/', views.orders, name='orders'), 
    path('product-detail/<int:pk>', views.productDetailView.as_view(), name='product-detail'),
    path('address/', views.address, name='address'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('buy-now/', views.buyNow, name='buy-now'),    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)