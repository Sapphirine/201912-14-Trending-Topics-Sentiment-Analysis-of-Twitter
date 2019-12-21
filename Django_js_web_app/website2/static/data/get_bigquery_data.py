from django.http import HttpResponse
from django.shortcuts import render
import pandas_gbq
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('final_project\\big-data-sh3907-48db3bfb1540.json')

pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "big-data-sh3907"

SQL = "SELECT * FROM `big-data-sh3907.final_project.test`"
df = pandas_gbq.read_gbq(SQL)
print(df)

