from bs4 import BeautifulSoup
from django_q.tasks import async_task
from django.core.mail import send_mail

import requests
import re


def extract_email(url):
    email_pattern = r'[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+'
    emails = re.findall(email_pattern, url)
    filtered_emails = []
    for email in emails:
        if not email.endswith("jpeg") and not email.endswith("png") and not email.endswith("jpg"):
            filtered_emails.append(email)
    return filtered_emails


def scrape_emails(url):

    res = requests.get(url)
    emails = set(extract_email(res.text))
    soup = BeautifulSoup(res.text, 'html.parser')
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if link_url and link_url.startswith('http'):
            link_res = requests.get(link_url)
            link_emails = set(extract_email(link_res.text))
            emails.update(link_emails)

    return list(emails)


def run_campaigns(email_id=None, **kwargs):

    url_email = kwargs['kwargs']['url_email']
    campaign = kwargs['kwargs']['campaign']
    subject, message = campaign[0], campaign[1]
    email_from = "no_reply@mail.com"

    if not subject and not message and not url_email:
        return None
    else:
        if email_id:
            email = url_email['email']
            send_mail(
                subject, message, email_from, [email]
            )
        else:
            for emails in url_email:
                email = emails['email']
                send_mail(
                    subject, message, email_from, [email]
                )
