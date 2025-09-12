import csv
from django.core.management.base import BaseCommand
from maps.models import RailwayProperty

class Command(BaseCommand):
    help = "Load railway data from korail_data.csv into RailwayProperty model"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='korail_data.csv',
            help='CSV file path (default: korail_data.csv in project root)'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        created_count = 0

        try:
            with open(file_path, newline='', encoding='euc-kr') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # 공부상 면적 처리 (쉼표 제거 + 숫자 변환)
                    official_area_str = row.get("공부상 면적") or "0"
                    try:
                        official_area_val = float(official_area_str.replace(",", "").strip())
                    except ValueError:
                        official_area_val = 0.0

                    RailwayProperty.objects.create(
                        regional_headquarters=row.get("지역본부") or "",
                        address=row.get("재산 소재지") or "",
                        line_name=row.get("노선명") or "",
                        official_area=official_area_val,   # ← 여기 반영
                        type_classification=row.get("유형분류") or "",
                        usage_status=row.get("사용여부") or "",
                        purpose_2024=row.get("2024년도 사용목적") or "",
                        future_plan=row.get("향후 사용계획 및 추진사항") or "",
                        remarks=row.get("비고") or "",
                    )
                    created_count += 1

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {created_count} records."))
