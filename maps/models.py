from django.db import models

class RailwayProperty(models.Model):
    """
    korail_data.csv 파일의 데이터를 저장하기 위한 모델
    """
    regional_headquarters = models.CharField(max_length=50) # 지역본부
    address = models.CharField(max_length=255) # 재산 소재지
    line_name = models.CharField(max_length=100) # 노선명
    official_area = models.FloatField() # 공부상 면적
    type_classification = models.CharField(max_length=50) # 유형분류
    usage_status = models.CharField(max_length=50) # 사용여부
    purpose_2024 = models.CharField(max_length=100, blank=True, null=True) # 용도
    future_plan = models.TextField(blank=True, null=True) # 향후 사용계획 및 추진사항
    remarks = models.TextField(blank=True, null=True) # 비고

    def __str__(self):
        return f"[{self.regional_headquarters}] {self.address}"