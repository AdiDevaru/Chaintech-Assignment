from django.urls import path
from .views import  QuoteList, CustomLoginView, RegisterUser, UserProfile, UserEditView, QuoteCreate, QuoteUpdate, QuoteDelete
from django.contrib.auth.views import LogoutView 


urlpatterns = [
    path('', QuoteList.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/',LogoutView.as_view(next_page='home'),name='logout'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('edit-profile/', UserEditView.as_view(), name='edit_profile'),
    path('add-quote/', QuoteCreate.as_view(), name='addQuote'),
    path('update-quote/<int:pk>', QuoteUpdate.as_view(), name='updateQuote'),
    path('delete-quote/<int:pk>', QuoteDelete.as_view(), name='deleteQuote'),
]