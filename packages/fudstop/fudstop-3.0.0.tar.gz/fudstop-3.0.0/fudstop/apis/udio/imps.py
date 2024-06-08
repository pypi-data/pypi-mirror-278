import pandas as pd
import asyncio
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from .models.udio_models import MySongs

db = PolygonDatabase(host='localhost', database='sound', user='chuck', password='fud', port=5432)

import httpx

import requests


headers =  {
    "Cookie": "_ga=GA1.1.628748314.1714795411; sb-ssr-production-auth-token.0=%7B%22access_token%22%3A%22eyJhbGciOiJIUzI1NiIsImtpZCI6IlJHVktoVzNNcSsyVzhxcDkiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzE0Nzk5MDQwLCJpYXQiOjE3MTQ3OTU0NDAsImlzcyI6Imh0dHBzOi8vbWZtcHhqZW1hY3NoZmNwem9zbHUuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImU2ZDU2MjE2LWE5M2YtNDc4ZC1hMjJhLWI5MGYyNDUxYWZjZSIsImVtYWlsIjoiY2h1Y2tkdXN0aW4xMkBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6Imdvb2dsZSIsInByb3ZpZGVycyI6WyJnb29nbGUiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xQeFdCY2JSaVdQWm55WFozZ1ZTZl9PeDdrUWltaml0aGNkWFZxRkp6UkpuQWFMeThSM2c9czk2LWMiLCJlbWFpbCI6ImNodWNrZHVzdGluMTJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6IkNoYXJsaWUgVmlkcyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiJDaGFybGllIFZpZHMiLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMUHhXQmNiUmlXUFpueVhaM2dWU2ZfT3g3a1FpbWppdGhjZFhWcUZKelJKbkFhTHk4UjNnPXM5Ni1jIiwicHJvdmlkZXJfaWQiOiIxMDU1ODc0Nzc1MDc0MTQzNDY1ODIiLCJzdWIiOiIxMDU1ODc0Nzc1MDc0MTQzNDY1ODIifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJvYXV0aCIsInRpbWVzdGFtcCI6MTcxNDc5NTQ0MH1dLCJzZXNzaW9uX2lkIjoiMzhhZDJkNTYtOGFiMi00NDhiLTlhZWQtOGVmZTVkOTRkYzdiIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.dl_nuHRnPAAjcrTJmdv1odb0nbmfjUJ64uhFyoYRtTo%22%2C%22token_type%22%3A%22bearer%22%2C%22expires_in%22%3A3600%2C%22expires_at%22%3A1714799040%2C%22refresh_token%22%3A%22eFRWH8GQZCW68FO2y2Tq9A%22%2C%22user%22%3A%7B%22id%22%3A%22e6d56216-a93f-478d-a22a-b90f2451afce%22%2C%22aud%22%3A%22authenticated%22%2C%22role%22%3A%22authenticated%22%2C%22email%22%3A%22chuckdustin12%40gmail.com%22%2C%22email_confirmed_at%22%3A%222024-05-03T03%3A57%3A05.150222Z%22%2C%22phone%22%3A%22%22%2C%22confirmed_at%22%3A%222024-05-03T03%3A57%3A05.150222Z%22%2C%22last_sign_in_at%22%3A%222024-05-04T04%3A04%3A00.289598718Z%22%2C%22app_metadata%22%3A%7B%22provider%22%3A%22google%22%2C%22providers%22%3A%5B%22google%22%5D%7D%2C%22user_metadata%22%3A%7B%22avatar_url%22%3A%22https%3A%2F%2Flh3.googleusercontent.com%2Fa%2FACg8ocLPxWBcbRiWPZnyXZ3gVSf_Ox7kQimjithcdXVqFJzRJnAaLy8R3g%3Ds96-c%22%2C%22email%22%3A%22chuckdustin12%40gmail.com%22%2C%22email_verified%22%3Atrue%2C%22full_name%22%3A%22Charlie%20Vids%22%2C%22iss%22%3A%22https%3A%2F%2Faccounts.google.com%22%2C%22name%22%3A%22Charlie%20Vids%22%2C%22phone_verified%22%3Afalse%2C%22picture%22%3A%22https%3A%2F%2Flh3.googleusercontent.com%2Fa%2FACg8ocLPxWBcbRiWPZnyXZ3gVSf_Ox7kQimjithcdXVqFJzRJnAaLy8R3g%3Ds96-c%22%2C%22provider_id%22%3A%22105587477507414346582%22%2C%22sub%22%3A%22105587477507414346582%22%7D%2C%22identities%22%3A%5B%7B%22identity_id%22%3A%2223013be0-e0cd-4a11-8c23-fbf06e89f3a0%22%2C%22id%22%3A%22105587477507414346582%22%2C%22user_id%22%3A%22e6d56216-a93f-478d-a22a-b90f2451afce%22%2C%22identity_data%22%3A%7B%22avatar_url%22%3A%22https%3A%2F%2Flh3.googleusercontent.com%2Fa%2FACg8ocLPxWBcbRiWPZnyXZ3gVSf_Ox7kQimjithcdXVqFJzRJnAaLy8R3g%3Ds96-c%22%2C%22email%22%3A%22chuckdustin12%40gmail.com%22%2C%22email_verified%22%3Atrue%2C%22full_name%22%3A%22Charlie%20Vids%22%2C%22iss%22%3A%22https%3A%2F%2Faccounts.google.com%22%2C%22name%22; sb-ssr-production-auth-token.1=%3A%22Charlie%20Vids%22%2C%22phone_verified%22%3Afalse%2C%22picture%22%3A%22https%3A%2F%2Flh3.googleusercontent.com%2Fa%2FACg8ocLPxWBcbRiWPZnyXZ3gVSf_Ox7kQimjithcdXVqFJzRJnAaLy8R3g%3Ds96-c%22%2C%22provider_id%22%3A%22105587477507414346582%22%2C%22sub%22%3A%22105587477507414346582%22%7D%2C%22provider%22%3A%22google%22%2C%22last_sign_in_at%22%3A%222024-05-03T03%3A57%3A05.147174Z%22%2C%22created_at%22%3A%222024-05-03T03%3A57%3A05.147222Z%22%2C%22updated_at%22%3A%222024-05-04T04%3A04%3A00.175832Z%22%2C%22email%22%3A%22chuckdustin12%40gmail.com%22%7D%5D%2C%22created_at%22%3A%222024-05-03T03%3A57%3A05.145454Z%22%2C%22updated_at%22%3A%222024-05-04T04%3A04%3A00.292386Z%22%2C%22is_anonymous%22%3Afalse%7D%2C%22provider_token%22%3A%22ya29.a0AXooCgsVB_5eMaOZPfpqhDeDt-7A7uMWQSu97MyXUgjllynT50JH6L33iTnHchRHmzcr2LBv40gINIEZuv3nEZV_moRGEx8CKw0rnzAAcTlIkemQ-QJdH9Ft71zgk3JSCDu36VP6nh2LcQuNk9-dAQqmOjmYhgAjN8AaCgYKAVcSARESFQHGX2Mi5vbLKTygpanzK7as3BmMLw0170%22%7D; _ga_RF4WWQM7BF=GS1.1.1714795410.1.1.1714795420.50.0.0"
}