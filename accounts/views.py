# views.py
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone  # Add this import
from django.conf import settings
import requests
from datetime import datetime
from core.models import *


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Please provide both email and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(email=email, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get or create meter token
        # this code will get the meter readings
        # ==================================this  code should be uncommented to get data from 
        try:
            meter_token = self.get_or_refresh_meter_token(user)
            pass
        except Exception as e:
            return Response(
                {'error': f'Error with meter token: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Generate Django JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'email': user.email,
                'username': user.username,
                'id': str(user.id)
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

    def get_or_refresh_meter_token(self, user):
        """Get or refresh meter API token"""
        # Check for existing valid token
        token = AuthenticationToken.objects.filter(
            user=user,
            created_at__gt=timezone.now() - timezone.timedelta(seconds=7200)
        ).first()
        
        if token and not token.is_expired():
            return token
            
        # Get new token from meter API
        response = requests.post(
            'http://122.224.159.102:6709/hservice/oauth/token',
            params={
                'client_id': settings.METER_API_CLIENT,
                'client_secret': settings.METER_API_SECRET
            }
        )

        print(response)
        try:
            data = response.json()
            
            # Ensure it's a list and has at least one element
            if not isinstance(data, list) or len(data) == 0:
                raise Exception(f'Unexpected response format: {data}')
            
            # Get the first object in the list
            token_data = data[0]
            
            if "access_token" not in token_data or "expires_in" not in token_data:
                raise Exception(f'Missing expected keys in response: {token_data}')
            
        except ValueError:
            raise Exception(f'Invalid JSON response: {response.text}')

        if response.status_code != 200 or token_data.get("code") != "0":
            raise Exception(f"Meter API error: {token_data.get('error', 'Unknown error')}")

        token, created = AuthenticationToken.objects.update_or_create(
            user=user,
            defaults={
                "access_token": token_data["access_token"],
                "expires_in": int(token_data["expires_in"]),
            }
        )
        token.access_token = token_data["access_token"]
        token.save()
        print(token_data["access_token"])

        return token  # Or whatever you need to do with the token

class MeterAPIView(views.APIView):
    """Base class for meter API views"""
    
    def get_meter_token(self, user):
        """Get valid meter token"""
        login_view = LoginView()
        return login_view.get_or_refresh_meter_token(user)
        
    def get_headers(self, user):
        """Get headers for meter API requests"""
        token = self.get_meter_token(user)
        return {
            'content-Type': 'application/json',
            'charset': 'UTF-8',
            'access_token': token.access_token,
            'client_id': str(user.id)
        }

class MeterDataView(MeterAPIView):
    """View for getting meter data"""
    
    def get(self, request):
        try:
            params = {
                'dataType': request.query_params.get('dataType', '1'),
                'meterType': '1'
            }
            
            # Add optional parameters
            meter_no = request.query_params.get('meterNo')
            if meter_no:
                params['meterNo'] = meter_no
                
            if params['dataType'] == '2':
                params['beginTime'] = request.query_params.get(
                    'beginTime', 
                    (timezone.now() - timezone.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
                )
                params['endTime'] = request.query_params.get(
                    'endTime',
                    timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            
            response = requests.post(
                f"{settings.METER_API_BASE_URL}/remoteData/getMeterData",
                headers=self.get_headers(request.user),
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                self.store_meter_readings(data)
                return Response(data)
                
            return Response(
                {"error": "Failed to fetch meter data"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def store_meter_readings(self, data):
        """Store meter readings in database"""
        if data['code'] == 0 and 'data' in data:
            for reading_data in data['data']:
                meter, created = WaterMeter.objects.get_or_create(
                    meter_no=reading_data['meterNo'],
                    defaults={
                        'user_code': reading_data['userCode'],
                        'signal_strength': float(reading_data['signalStrength'])
                    }
                )
                
                meter.last_reading = float(reading_data['currentReading'])
                meter.last_read_time = datetime.fromtimestamp(
                    int(reading_data['sysReadTime'])
                )
                meter.save()
                
                MeterReading.objects.create(
                    meter=meter,
                    reading=float(reading_data['currentReading']),
                    timestamp=datetime.fromtimestamp(
                        int(reading_data['sysReadTime'])
                    )
                )

class ValveControlView(MeterAPIView):
    """View for controlling valves"""
    
    def post(self, request):
        try:
            meter_no = request.data.get('meterNo')
            valve_state = request.data.get('valveState')
            
            if not all([meter_no, valve_state]):
                return Response(
                    {"error": "meterNo and valveState are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            response = requests.post(
                f"{settings.METER_API_BASE_URL}/remoteData/setValveState",
                headers=self.get_headers(request.user),
                params={
                    'meterNo': meter_no,
                    'valveState': valve_state
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Store valve control record
                meter = WaterMeter.objects.get(meter_no=meter_no)
                ValveControl.objects.create(
                    meter=meter,
                    state=int(valve_state),
                    command_status=data['cmdState']
                )
                
                return Response(data)
                
            return Response(
                {"error": "Failed to control valve"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
