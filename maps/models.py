from django.db import models

class RailwayProperty(models.Model):
    """ korail_data.csv 파일의 데이터를 저장하기 위한 모델 """
    regional_headquarters = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    line_name = models.CharField(max_length=100)
    official_area = models.FloatField()
    type_classification = models.CharField(max_length=50)
    usage_status = models.CharField(max_length=50)
    purpose_2024 = models.CharField(max_length=100, blank=True, null=True)
    future_plan = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    # GPS 기반 거리 계산을 위한 위도, 경도 필드 추가
    latitude = models.FloatField(null=True, blank=True)   # 위도
    longitude = models.FloatField(null=True, blank=True)  # 경도

    def __str__(self):
        return f"[{self.regional_headquarters}] {self.address}"
