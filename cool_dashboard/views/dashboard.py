from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views import View
from ..models import *
from ..config import *

import os
import yaml

# def dashboard(request):
#     if request.method == "GET":
#         context = {}
#         context['username'] = request.user
#         context['last_user'] = 'peng'
#         context['last_dataset'] = 'AKI3269'
#         context['storage'] = 400
#         context['num_datasets'] = 1
#         context['num_users'] = 1
#         # print(request.user.email)
#         # user = User.objects.get(username=request.user)
#         return render(request, "dashboard.html", context)

def strTotime(name):
    return name[:4] + "/" + name[4:6] + "/" + name[6:8]


class Dashboard(View):
    # @login_required
    def get(self, request):
        logging.info(request.user)
        if request.user.is_superuser:
            all_users = User.objects.count()
            all_figures = analysis.objects.count()
            all_datasets = csv_file.objects.count()
            all_storage = 0
            root_flag =True
            for db in csv_file.objects.all():
                all_storage += db.file_size

        databases = {}
        count = 0
        selected_datasets = csv_file.objects.filter(user_id=request.user.id)
        user_datasets = selected_datasets.count()
        user_figures = 0
        user_storage = 0
        last_dataset = ""

        figures = {}
        figure_index = 0
        for dataset in selected_datasets:
            databases[count] = {}
            databases[count]["name"] = dataset.file_name
            last_dataset = dataset.file_name
            databases[count]['date'] = strTotime(dataset.file_save)
            databases[count]['num_ids'] = dataset.num_ids
            databases[count]['num_records'] = dataset.num_records
            databases[count]['involved_dates'] = dataset.involved_dates

            user_figures += analysis.objects.filter(file_id=dataset.file_id).count()
            user_storage += dataset.file_size

            with open(data_path + dataset.file_save + "/demographic.yaml", 'r') as stream:
                demographic_info = yaml.load(stream)

            databases[count]['figures'] = []

            figures[figure_index] = {
                "title": demographic_info['Event']['name'],
                "type": 'pie',
                "y_label": list(demographic_info['Event']['data'].keys()),
                "data": demographic_info['Event']['data'],

            }
            databases[count]['figures'].append(figure_index)
            figure_index += 1

            for value in demographic_info['Value']:
                if value['type'] == 'pie':
                    figures[figure_index] = {
                        "title": value['name'],
                        "type": 'pie',
                        "y_label": [str(i) for i in list(value['data'].keys())],
                        "data": value['data'],

                    }
                elif value['type'] == 'bar':
                    figures[figure_index] = {
                        "title": value['name'],
                        "type": 'bar',
                        "y_label": value['data']['y'],
                        "data": value['data']['x'],
                    }
                databases[count]['figures'].append(figure_index)
                figure_index += 1

            count += 1

        return render(request, "dashboard.html", locals())
