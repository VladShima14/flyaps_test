from rest_framework import serializers

from django.db.models import Min, Max

from core.models import Agreement


class AgreementSerializer(serializers.ModelSerializer):

    calendar = serializers.SerializerMethodField()

    class Meta:
        model = Agreement
        fields = ['calendar']

    def get_calendar(self, obj):
        all_agr = Agreement.objects.all()
        min_year = all_agr.aggregate(Min('start_date'))
        max_year = all_agr.aggregate(Max('stop_date'))
        return [i for i in range(min_year['start_date__min'].year, max_year['stop_date__max'].year + 1)]
