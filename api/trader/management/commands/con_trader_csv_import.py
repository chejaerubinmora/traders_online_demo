import glob
import logging
import os
import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User

from api.trader.models import Product

logger = logging.getLogger('django_project_api')


class Command(BaseCommand):
    help = 'CSV import product'

    def handle(self, *args, **options):
        root_dir = os.path.dirname(settings.BASE_DIR)
        csv_dir = os.path.join(root_dir, 'csv')
        csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
        df_list = [pd.read_csv(file) for file in csv_files]
        combined_df = pd.concat(df_list, ignore_index=True)

        for _, row in combined_df.iterrows():
            user_id = row.get('user')
            user = User.objects.filter(pk=user_id).first()

            if user:
                name = row.get('name')
                currency = row.get('currency')
                quantity = row.get('quantity')
                price = row.get('price')

                product_data = {
                    'user': user,
                    "quantity": quantity,
                    "name": name,
                    "currency": currency,
                    "price": price
                }
                Product.objects.create(**product_data)
