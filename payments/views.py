import time
import uuid
import requests

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Gateway, Payment
from .serializers import GatewaySerializer

from subscriptions.models import Package, Subscription


class GatewayView(APIView):
    def get(self, request):
        gateway = Gateway.objects.filter(is_enable=True)
        serializer = GatewaySerializer(gateway, many=True)
        return Response(serializer.data)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gateway_id = request.query_params.get('gateway')
        package_id = request.query_params.get('package')

        try:
            gateway = Gateway.objects.get(pk=gateway_id, is_enable=True)
            package = Package.objects.get(pk=package_id, is_enable=True)
        except (Package.DoesNotExist, Gateway.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user=request.user,
            package=Package,
            gateway=gateway,
            price=package.price,
            phone_number=request.user.phone_number,
            token=str(uuid.uuid4())
        )

    # masir url bank ra midahim
        return Response({'token': payment.token,
                         'callback_url': 'https://my-bank-site.com'})

    def pot(self, request):
        token = request.data.get('token')
        st = request.data.get('status')

        try:
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if st != 10:
            payment.status = Payment.STATUS_CANCELED
            payment.save()
            # render(request, 'payment-result.html', contex={'staus': my_status})
            return Response({'detail: Payment canceled by user'},
                            status=status.HTTP_400_BAD_REQUEST)

        bank_r = requests.post('bank_verification_url', data={})
        if bank_r.status_code // 100 != 2:
            payment.status = Payment.STATUS_ERROR
            payment.save()
            # render(request, 'payment-result.html', contex={'status': mt_status})\
            return Response({'detail': 'Payment verification failed'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            payment.status = Payment.STATUS_PAID
            payment.save()
        # hala ke payment ok shod subscription misazim
            Subscription.objects.create(
                user=payment.user,
                package=payment.package,
                expire_time=timezone.now() + timezone.timedelta(days=payment.package.durations.days)
            )

            return Response({'detail': 'Payment is successful'})
