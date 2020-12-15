import json
import boto3


def lambda_handler(event, context):
    records = event['Records']
    target_bucket = 'TARGET_BUCKET'
    print("Event :", event)

    extentions = [{'folder': 'ce_ebs_vols',
                   'str_slice': 'EBS-Vols.json'
                   },
                  {'folder': 'ce_ebs_snaps',
                      'str_slice': 'EBS-Snaps.json'
                   },
                  {'folder': 'ce_rds_storage',
                      'str_slice': 'RDS.json'
                   },
                  {'folder': 'ce_s3_storage',
                      'str_slice': 'S3.json'
                   },
                  {'folder': 'ce_ddb_storage',
                      'str_slice': 'DynamoDB.json'
                   }]

    for i in range(len(records)):
        encoded_name = event['Records'][i]['s3']['object']['key']
        file_name = encoded_name.replace('+', ' ')
        source_bucket = event['Records'][i]['s3']['bucket']['name']

        while True:
            for i in range(len(extentions)):
                s = len(extentions[i]['str_slice'])
                ext = extentions[i]['str_slice']
                folder = extentions[i]['folder']
                if file_name[-s:] == ext:
                    print(f'Match found. Extention type {ext}')
                    move(target_bucket, source_bucket, folder, file_name)
                    delete(source_bucket, file_name)
                    return True
                else:
                    continue
            print('Failed to find matching extention \n')
            print(f'Deleting file {file_name}')
            delete(source_bucket, file_name)
            return True
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def move(target_b, source_b, folder, filename):
    try:
        key = f'{folder}/{filename}'
        s3 = boto3.resource('s3')
        print(f'Attempting to move {filename} to {target_b}/{key}')
        response = s3.Object(target_b, key).copy_from(
            CopySource=f'{source_b}/{filename}')
        code = response['ResponseMetadata']['HTTPStatusCode']
        if code == 200:
            print(f'Successfully moved {filename}')
        else:
            print(f'Failed to move {filename}')
    except Exception as e:
        print(f'Failed to move {filename} {e}')
        pass


def delete(bucket, filename):
    try:
        s3 = boto3.resource('s3')
        print(f'Attempting to delete {filename}')
        response = s3.Object(bucket, filename).delete()
        code = response['ResponseMetadata']['HTTPStatusCode']
        print(f'response code {code}')
        print(response)
        if code == 200 or 204:
            print(f'Successfully deleted {filename}')
        else:
            print(f'Failed to delete {filename}')
    except Exception as e:
        print(f'Failed to delete {filename} {e}')
        pass
