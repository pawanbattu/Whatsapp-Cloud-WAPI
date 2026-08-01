from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from .views.messages import MessagesViewSet
from .views.templates import TemplatesViewSet
from .views.users import UsersViewSet
from .views.media import *
from .views.auth import *
from .views.ReceiveMessage import *
from .views.MessageStreamView import *
from rest_framework.routers import DefaultRouter

urlpatterns = [

    # ── User & Auth ──────────────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/users/health_check', UsersViewSet.as_view({'get': 'health_check'})),
    path(f'api/{settings.API_VERSION}/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'api/{settings.API_VERSION}/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'api/{settings.API_VERSION}/users/Getuser', UsersViewSet.as_view({'get': 'Getuser'})),
    path(f'api/{settings.API_VERSION}/users/PostFile/', UsersViewSet.as_view({'post': 'PostFile'})),
    path(f'api/{settings.API_VERSION}/users/Createuser/', UsersViewSet.as_view({'post': 'Createuser'})),
    path(f'api/{settings.API_VERSION}/users/Updateuser/<int:id>/', UsersViewSet.as_view({'patch': 'Updateuser'})),
    path(f'api/{settings.API_VERSION}/users/Deleteuser/<int:id>/', UsersViewSet.as_view({'delete': 'Deleteuser'})),
    path(f'api/{settings.API_VERSION}/users/refreshToken/', UsersViewSet.as_view({'get': 'refreshToken'})),
    path(f'api/{settings.API_VERSION}/users/subscribefields/', UsersViewSet.as_view({'post': 'subcribeApps'})),
    path(f'api/{settings.API_VERSION}/users/subscribeCallBackUrl/', UsersViewSet.as_view({'post': 'subscribeCallBackUrl'})),
    
    # ── Media ─────────────────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/start-chunk-upload/', StartChunkUploadView.as_view()),
    path(f'api/{settings.API_VERSION}/upload-chunk/', UploadChunkView.as_view()),
    path(f'api/{settings.API_VERSION}/complete-chunk-upload/', CompleteChunkUploadView.as_view()),
    path(f'api/{settings.API_VERSION}/cancel-chunk-upload/', CancelChunkUploadView.as_view()),
    path(f'api/{settings.API_VERSION}/whatsapp/upload-handle/', WhatsAppMediaUploadView.as_view(), name='whatsapp-upload-handle'),
    path(f'api/{settings.API_VERSION}/upload-media/', WhatsAppMediaUploadView.as_view(), name='whatsapp-media-upload'),
    
    # ── Messages ─────────────────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/messages/Getmessage/', MessagesViewSet.as_view({'get': 'Getmessage'})),
    path(f'api/{settings.API_VERSION}/messages/Sendmessage/', MessagesViewSet.as_view({'post': 'Sendmessage'})),
    path(f'api/{settings.API_VERSION}/messages/Schedulemessage/', MessagesViewSet.as_view({'post': 'Schedulemessage'})),
    path(f'api/{settings.API_VERSION}/messages/<int:user_id>/mark-read/', MessagesViewSet.as_view({'post': 'markMessageAsRead'})),
    path(f'api/{settings.API_VERSION}/messages/getMessagesByBatch/', MessagesViewSet.as_view({'get': 'Getconversations'}),name='messages-by-batch'),
    path(f'api/{settings.API_VERSION}/stream/messages/<int:admin_id>/', MessageStreamView.as_view(), name='message_stream'),
    path(f'api/{settings.API_VERSION}/messages/receiveMessages/<int:admin_id>/', ReceiveMessageView.as_view()),
    path(f'api/{settings.API_VERSION}/messages/Sendreaction/', MessagesViewSet.as_view({'post': 'Sendreaction'})),
    path(f'api/{settings.API_VERSION}/messages/GetSchedulemessage', MessagesViewSet.as_view({'get': 'GetSchedulemessage'})),
    path(f'api/{settings.API_VERSION}/messages/DeleteSchedulemessage/<int:id>/', MessagesViewSet.as_view({'delete': 'DeleteSchedulemessage'})),
    
    # ── Templates ────────────────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/templates/Savetemplate/', TemplatesViewSet.as_view({'post': 'Savetemplate'})),
    path(f'api/{settings.API_VERSION}/templates/Sendtemplate/', TemplatesViewSet.as_view({'post': 'Sendtemplate'})),
    path(f'api/{settings.API_VERSION}/templates/Submittemplate/', TemplatesViewSet.as_view({'post': 'Submittemplate'})),
    path(f'api/{settings.API_VERSION}/templates/Gettemplate', TemplatesViewSet.as_view({'get': 'Gettemplates'})),
    path(f'api/{settings.API_VERSION}/templates/Synctemplate/', TemplatesViewSet.as_view({'post': 'Synctemplate'})),
    path(f'api/{settings.API_VERSION}/templates/Deletetemplate/<str:template_name>/', TemplatesViewSet.as_view({'delete': 'Deletetemplate'})),
    path(f'api/{settings.API_VERSION}/templates/Edittemplate/<int:template_id>/', TemplatesViewSet.as_view({'post': 'Edittemplate'})),
    path(f'api/{settings.API_VERSION}/templates/Scheduletemplate/', TemplatesViewSet.as_view({'post': 'Scheduletemplate'})),

    # ── Registration & Login ─────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/register/', RegisterView.as_view(), name='register'),
    path(f'api/{settings.API_VERSION}/login/', LoginView.as_view(), name='login'),
    path(f'api/{settings.API_VERSION}/logout/', LogoutView.as_view(), name='logout'),

    # ── Token ────────────────────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ── Email Verification ───────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path(f'api/{settings.API_VERSION}/resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),

    # ── Password Management ──────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path(f'api/{settings.API_VERSION}/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path(f'api/{settings.API_VERSION}/reset-password/validate/', ValidateResetTokenView.as_view(), name='validate-reset-token'),
    path(f'api/{settings.API_VERSION}/change-password/', PasswordChangeView.as_view(), name='change-password'),

    # ── Profile ──────────────────────────────────────────────────────────────
    path(f'api/{settings.API_VERSION}/me/', UserProfileView.as_view(), name='profile'),
    path(f'api/{settings.API_VERSION}/me/delete/', DeleteAccountView.as_view(), name='delete-account'),
]