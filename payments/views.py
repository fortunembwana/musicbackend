from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from songs.models import Song

class PaymentUploadView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        song_id = self.request.data.get('song')
        try:
            song = Song.objects.get(id=song_id, artist__user=self.request.user)
            serializer.save(song=song)
            
            # Update song status
            song.payment_status = 'pending'
            song.save()
            
            return Response({"message": "Payment proof uploaded successfully"}, status=status.HTTP_201_CREATED)
        except Song.DoesNotExist:
            return Response({"error": "Song not found or you don't own it"}, status=status.HTTP_404_NOT_FOUND)