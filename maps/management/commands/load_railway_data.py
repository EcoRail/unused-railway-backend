# maps/management/commands/load_railway_data.py

import csv
from django.core.management.base import BaseCommand
from maps.models import RailwayProperty

class Command(BaseCommand):
    help = 'Loads data from korail_data.csv into the RailwayProperty model'

    def handle(self, *args, **kwargs):
        RailwayProperty.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted existing railway properties.'))

        csv_file_path = '../unused-railway-frontend/public/korail_data.csv'

        try:
            # 여기를 수정했습니다! utf-8-sig -> cp949
            with open(csv_file_path, mode='r', encoding='cp949') as file:
                reader = csv.reader(file)
                next(reader)  # 헤더 행 건너뛰기

                properties_to_create = []
                for row in reader:
                    try:
                        official_area_val = float(row[4])
                    except (ValueError, IndexError):
                        official_area_val = 0.0

                    properties_to_create.append(
                        RailwayProperty(
                            regional_headquarters=row[1],
                            address=row[2],
                            line_name=row[3],
                            official_area=official_area_val,
                            type_classification=row[5],
                            usage_status=row[6],
                            purpose_2024=row[7],
                            future_plan=row[8],
                            remarks=row[9] if len(row) > 9 else None,
                        )
                    )
                
                RailwayProperty.objects.bulk_create(properties_to_create)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(properties_to_create)} railway properties.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found at {csv_file_path}. Please check the path.'))
        except UnicodeDecodeError:
            self.stdout.write(self.style.ERROR('Failed to decode the file with cp949. Try other encodings like "euc-kr".'))