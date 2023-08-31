from django.urls import path
from .views import CompaignCrud, UrlEmailScraper, AllEmail, AllEmailCampaign

urlpatterns = [

    path('compaign/', CompaignCrud.as_view(), name='compaign-list'),
    path('compaign/<int:pk>/', CompaignCrud.as_view(), name='compaign-detail'),
    path('urlemail/', UrlEmailScraper.as_view(), name='email-scraper'),
    path('allemail/', AllEmail.as_view(), name='all-email'),
    path('allemail/<int:pk>/', AllEmail.as_view(), name='all-email'),
    path('allemailcampaign/', AllEmailCampaign.as_view(),
         name='all-email-campaign'),
]
