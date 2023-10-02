from django import template
from website.models import Notification

register = template.Library()


@register.simple_tag
def get_my_notifications(user_id, notification_type):
    if notification_type == 'all' or notification_type == '' or notification_type is None:
        return Notification.objects.filter(to_user__id=user_id).order_by('-id')
    if notification_type == 'read':
        return Notification.objects.filter(to_user__id=user_id, read=True).order_by('-id')
    if notification_type == 'unread':
        return Notification.objects.filter(to_user__id=user_id, read=False).order_by('-id')


@register.simple_tag
def get_my_unread_notifications_count(user_id):
    return Notification.objects.filter(to_user__id=user_id, read=False).count()


@register.simple_tag
def get_admin_notifications(notification_type):
    if notification_type == 'all' or notification_type == '' or notification_type is None:
        return Notification.objects.filter(to_admin=True).order_by('-id')
    if notification_type == 'read':
        return Notification.objects.filter(to_admin=True, read=True).order_by('-id')
    if notification_type == 'unread':
        return Notification.objects.filter(to_admin=True, read=False).order_by('-id')


@register.simple_tag
def get_admin_unread_notifications_count():
    return Notification.objects.filter(to_admin=True, read=False).count()


