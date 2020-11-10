from pprint import pprint
import boto3


def updateItems(table):
    for hr in range(24):
        date_time = f'20200823{hr:02}00'
        new_s3_loc = f's3://dl-pipeline-mart-east1-mod-dev/lld/MD_2099/quality/logs/2020/08/23/{hr:02}/impressions'
        search_key = {
            'REPORT_NAME': 'QLOG-impressions',
            'DATA_DATE_TIME': date_time
        }

        response = table.get_item( Key=search_key) 
        if 'Item' in response:
            #print(f"{date_time}: {response['Item']}")
            response = table.update_item(
                Key=search_key,
                UpdateExpression="set S3_DATA_LOCATION=:r",
                ExpressionAttributeValues={
                    ':r': new_s3_loc
                },
                ReturnValues="UPDATED_NEW"
            )
            print(f"updated {date_time}: {response}")
        else:
            new_item = {
              'S3_DATA_LOCATION': new_s3_loc,
              'DATA_DATE_TIME': date_time,
              'REPORT_NAME': 'QLOG-impressions'}
            response = table.put_item( Item=new_item )
            print(f"add new item {date_time}: {response}")
            #print(f"not exist {date_time}")


def viewItems(table):
    for hr in range(24):
        date_time = f'20200823{hr:02}00'
        search_key = {
            'REPORT_NAME': 'QLOG-impressions',
            'DATA_DATE_TIME': date_time
        }

        response = table.get_item( Key=search_key) 
        if 'Item' in response:
            print(f"{date_time}: {response['Item']}")
        else:
            print(f"not exist {date_time}")


def deleteItems(table):
    for hr in range(24):
        date_time = f'20200823{hr:02}00'
        search_key = {
            'REPORT_NAME': 'QLOG-impressions',
            'DATA_DATE_TIME': date_time
        }

        response = table.delete_item( Key=search_key) 
        print(f"deleting {date_time} {response}")


if __name__ == '__main__':
    session = boto3.session.Session(profile_name='saml', region_name='us-east-1')
    dynamodb = session.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('MoD-Signal-Bus-Messages')
    #updateItems(table)
    viewItems(table)
    #deleteItems(table)

