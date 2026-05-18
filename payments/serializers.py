from rest_framework import serializers
from .models import Payment   # ← Must be Capital P

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'song', 'payment_method', 'transaction_reference', 
                  'proof_image', 'status', 'submitted_at']
        read_only_fields = ['status']