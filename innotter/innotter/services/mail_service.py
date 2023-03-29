import boto3
from django.conf import settings

def send_email(subject, body, recipient_list):
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME
    )

    response = ses_client.send_email(
        Destination={
            'ToAddresses': recipient_list,
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source='innotter.test.mail@gmail.com',
    )

    print('send')

    return response['MessageId']

