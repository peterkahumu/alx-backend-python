from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessageSignalTest(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create_user(username='alice', password='pass123')
        receiver = User.objects.create_user(username='bob', password='pass456')

        msg = Message.objects.create(sender=sender, receiver=receiver, content="Hey bro!")

        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.user, receiver)
        self.assertEqual(notif.message, msg)
