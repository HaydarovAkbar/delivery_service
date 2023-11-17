from django.shortcuts import render
from django.http import HttpResponse
from telegram import Update
from .bot.main import bot, dispatcher
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import TGUsers, Channel, Admin, User, Order, Category, Products, ProductSize, TgUserLocations, OrderItem
from django.views import View
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filter import FilterByDate
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.utils.timezone import make_aware
from datetime import datetime, timedelta


@method_decorator(csrf_exempt, name='dispatch')
class MainView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET request')

    def post(self, request, *args, **kwargs):
        try:
            body = request.body
            body_json = json.loads(body)
            update: Update = Update.de_json(body_json, bot)
            dispatcher.process_update(update)
        except Exception as e:
            print(e)
        return HttpResponse('POST request')


class UsersView(View):
    def get(self, request, *args, **kwargs):
        users = TGUsers.objects.all()
        return render(request, 'users.html', context={'user_list': users})


@method_decorator(csrf_exempt, name='dispatch')
class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # Get the user by username
            user = User.objects.get(username=username)
            is_correct_password = check_password(password, user.password)

            if is_correct_password:
                user_list = TGUsers.objects.all().order_by('-date_of_created')[0:20]
                admin_list = Admin.objects.all()
                return render(request, 'index.html', context={'user_list': user_list[::-1], 'admin_list': admin_list})
            else:
                return render(request, 'login.html', context={'error': 'Username or password is incorrect'})
        except User.DoesNotExist:
            return render(request, 'login.html', context={'error': 'Username or password is incorrect'})


class LogInView(TokenObtainPairView):
    """separate login api for admin panel || ADMIN PANEL UCHUN ALOHIDA LOGIN API"""

    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username', None) or request.query_params.get('username', None)
            password = request.data.get('password', None) or request.query_params.get('password', None)
            if password and username:
                try:
                    user = User.objects.get(username=username)
                except Exception:
                    return Response("Foydalanuvchi topilmadi!", status=status.HTTP_401_UNAUTHORIZED)
                if not user.check_password(password):
                    return Response("Foydalanuvchi topilmadi!", status=status.HTTP_401_UNAUTHORIZED)
                if user:
                    refresh = TokenObtainPairSerializer().get_token(user)
                    data = {}
                    data['access'] = str(refresh.access_token)
                    data['refresh'] = str(refresh)
                    data['is_superuser'] = user.is_superuser
                    data['is_staff'] = user.is_staff
                    return Response(data=data, status=status.HTTP_200_OK)
        except Exception:
            pass
        return Response("Xatolik yuz berdi", status=status.HTTP_401_UNAUTHORIZED)


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'fullname'):
            queryset = self.queryset.exclude(fullname__exact='')
        return queryset


class PiaFilterByDateView(CustomModalViewSet, generics.ListAPIView):
    """Included both viewset and generic. Search and Filter are not properly supported in viewset only"""
    queryset = TGUsers.objects.all()
    serializer_class = serializers.TgUserSerializers
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['search']
    filterset_class = FilterByDate

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        search = self.request.query_params.get('search', None)
        queryset = self.queryset
        if date_from and date_to:
            queryset = queryset.filter(date_of_created__range=[date_from, date_to])
        if search:
            queryset = queryset.filter(fullname__icontains=search)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # This will give you a queryset of TGUsers who have at least one order.
        active_users = queryset.annotate(num_orders=Count('order')).filter(num_orders__gt=0)

        # To get the count of all active TGUsers
        active_users_count = active_users.count()
        all_user_count = queryset.count()
        passiv_count = all_user_count - active_users_count
        labels = ['active', 'passiv']
        dataset = [active_users_count, passiv_count]
        payload = {
            'active': active_users_count,
            'passiv': passiv_count,
            'all': all_user_count,
            'labels': labels,
            'dataset': dataset
        }
        return Response(payload, status=status.HTTP_200_OK)


class GraphFilterByDateView(CustomModalViewSet, generics.ListAPIView):
    """Graph Filter By Date"""
    queryset = TGUsers.objects.all()
    serializer_class = serializers.TgUserSerializers
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['search']
    filterset_class = FilterByDate

    def get_queryset(self):
        """This will give you a filtered queryset of TgUsers."""
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        search = self.request.query_params.get('search', None)
        queryset = self.queryset
        if date_from and date_to:
            queryset = queryset.filter(date_of_created__range=[date_from, date_to])
        if search:
            queryset = queryset.filter(fullname__icontains=search)
        return queryset

    def list(self, request, *args, **kwargs):
        """This will give you a queryset of TGUsers who have at least one order."""
        queryset = self.get_queryset()
        # Define your date range for a month
        start_date = datetime.strptime(self.request.query_params.get('date_from', None), '%Y-%m-%d')
        end_date = datetime.strptime(self.request.query_params.get('date_to', None), '%Y-%m-%d')

        # Filter users joined within the month
        users_by_month = queryset.filter(date_of_created__range=(start_date, end_date))

        # Annotate each user with the day they joined
        users_by_day = users_by_month.annotate(join_day=TruncDay('date_of_created'))

        # Calculate the sum for every 5 days
        sums_by_5_days = {}
        for start in range(0, 30, 5):
            end = start + 5
            # Define the date range for 5-day intervals
            interval_start = start_date + timedelta(days=start)
            interval_end = start_date + timedelta(days=end)

            # Annotate and sum within the 5-day interval
            sum_in_interval = users_by_day.filter(date_of_created__range=(interval_start, interval_end)).count()

            # Store the sum in the dictionary with the interval as key
            sums_by_5_days[str(interval_start.date().strftime("%m.%d")) + ' - ' + str(
                interval_end.date().strftime("%m.%d"))] = sum_in_interval

        return Response(sums_by_5_days, status=status.HTTP_200_OK)
