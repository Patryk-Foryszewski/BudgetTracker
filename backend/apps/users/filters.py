from .models import User

from django.db.models import Q
import django_filters


class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='user_filter')

    class Meta:
        model = User
        fields = ['username', 'email']

    def user_filter(self, _, *, value):
        return User.objects.filter(Q(username__icontains=value) | Q(email__exact=value))
