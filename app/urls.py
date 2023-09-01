from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from app import views
from .forms import LoginForm,MyPasswordChangeForm, MyPasswordResetForm, MysetPasswordForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ProductView.as_view(),name="home"),
  
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    path('cart/', views.show_cart, name='showcart'),
    
    path('pluscart/',views.plus_cart),
    
    path('minuscart/',views.minus_cart),
    
    path("removecart/", views.remove_cart,name="removecart"),

    path('buy/', views.buy_now, name='buy-now'), 
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('address/', views.address, name='address'),
    
    path('orders/', views.orders, name='orders'),
    
    path('passwordchange/', auth_views.PasswordChangeView.as_view(form_class=MyPasswordChangeForm,template_name='app/passwordchange.html',success_url='/passwordchangedone/'), name='passwordchange'),
    
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'), name='password_reset_done'),
    
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html',form_class=MysetPasswordForm), name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetcomplete.html'), name='password_reset_complete'),
    
    path('mobile/', views.mobile, name='mobile'),
    
    path('laptop/', views.laptop, name='laptop'),
    # path('bottomwear/', views.bottomwear, name='mobile'),
    # path('topwear/', views.topwear, name='topwear'),
    
    path('mobiledata/<slug:data>/', views.mobile, name='mobiledata'),
    
    path('laptopdata/<slug:data>/', views.laptop, name='laptopdata'),
    
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=LoginForm,template_name='app/login.html'), name='login'),
    
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    
    path('checkout/', views.checkout, name='checkout'),
    
    path('paymentdone/', views.payment_done, name='payment_done'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)