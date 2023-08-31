from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_q.tasks import schedule
from django_q.models import Schedule

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CompaignSerializer, UrlEmailSerializer
from .serializers import CompaignSerializer, UrlEmailSerializer
from .models import Compaign, UrlEmail
from .utils import scrape_emails, run_campaigns


class CompaignCrud(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            compaign = get_object_or_404(Compaign, id=pk, user=request.user)
            serializer = CompaignSerializer(compaign)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            compaign = Compaign.objects.filter(user=request.user)
            serializer = CompaignSerializer(compaign, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompaignSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"Message": "Compaign created successfully"}, status=status.HTTP_201_CREATED)
            return Response({"Message": "Compaign created successfully"}, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        compaign = get_object_or_404(Compaign, id=pk, user=request.user)
        serializer = CompaignSerializer(
            compaign, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"Message": "Update successful"}, status=status.HTTP_200_OK)
            return Response({"Message": "Update successful"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        compaign = get_object_or_404(Compaign, id=pk, user=request.user)
        compaign.delete()
        return Response({"Message": "Delete successful"}, status=status.HTTP_200_OK)


class UrlEmailScraper(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        url = request.query_params.get('url')
        if url is None:
            return Response({"Message": "Kindly provide a url"}, status=status.HTTP_404_NOT_FOUND)
        email_list = scrape_emails(url)
        if len(email_list) > 0:
            for email in email_list:
                urlemail = UrlEmail.objects.create(
                    user=request.user, email=email, url=url)
                return Response({"Message": "Email saved successfully"}, status=status.HTTP_201_CREATED)
        return Response({"Message": "Url does not contain any email"}, status=status.HTTP_200_OK)


class AllEmail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            url_email = UrlEmail.objects.filter(
                id=pk, user=request.user).values('email')
            campaign = Compaign.objects.filter(user=request.user).order_by(
                '-id').values_list('title', 'description').first()
            if not url_email.exists():
                return Response({"Message": "details not found"}, status=status.HTTP_404_NOT_FOUND)
            next_run = timezone.now() + timedelta(seconds=10)
            schedule(
                func='compaign_crud.utils.run_campaigns',
                kwargs={'url_email': list(url_email),
                        'campaign': campaign},
                schedule_type=Schedule.ONCE,
                repeats=1,
                next_run=next_run,
            )
            return Response({"Message": "Campaign run successfully on specific url emails"}, status=status.HTTP_200_OK)
        else:
            url_email = UrlEmail.objects.filter(user=request.user)
            serializer = UrlEmailSerializer(url_email, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class AllEmailCampaign(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campaign = Compaign.objects.filter(user=request.user).order_by(
            '-id').values_list('title', 'description').first()
        url_emails = UrlEmail.objects.filter(
            user=request.user).values('email')
        next_run = timezone.now() + timedelta(seconds=10)
        schedule(
            func='compaign_crud.utils.run_campaigns',
            kwargs={'url_email': list(url_emails),
                    'campaign': campaign},
            schedule_type=Schedule.ONCE,
            repeats=1,
            next_run=next_run,
        )
        return Response({"Message": "Campaign run successfully on all url emails"}, status=status.HTTP_200_OK)
