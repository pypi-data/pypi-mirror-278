import pandas as pd
import json
from storage_tool.s3 import S3Storage, S3Authorization
    
from storage_tool import Storage, Auth

with open('secrets/secret_aws.json') as json_file:
    data = json.load(json_file)
    KEY = data['KEY']
    SECRET = data['SECRET']
    REGION = data['REGION']

STORAGE_TYPE = 'S3'

auth = Auth(STORAGE_TYPE)
auth = auth.authenticator
auth.set_credentials(KEY, SECRET, REGION)

storage = Storage(STORAGE_TYPE, auth)
storage = storage.get_model()

## Create Storage
#storage.create_repository("local_storage")

## List Storages
print(storage.list_repositories())

# SET Storage
#storage.set_repository(repository='import-data-glue')

## List Objects
#print(storage.list())

## PUT Object
#data_fake = [{'col1': 1, 'col2': 2},{'col1': 1, 'col2': 2}]
#storage.put(file_path='teste_A.csv', content=data_fake)
#storage.put(file_path='teste_B.json', content=data_fake)
#storage.put(file_path='teste_C.parquet', content=data_fake)

## Read Object
#data = storage.read(file_path='teste_B.json', return_type=dict)
#print(data)

## Delete 
#ata = storage.delete(file_path='teste_BX.json')

## Move
#data = storage.move(src_path='teste_A.csv', dest_path='folder_teste/teste_A.csv')

## Move Between Repositories
#data = storage.move_between_repositories(src_repository='local_storage', src_path='folder_teste/teste_A.csv', dest_repository='local_storage_2', dest_path='folder_teste/teste_A_move.csv')

## Copy
#data = storage.copy(src_path='folder_teste/teste_D.csv', dest_path='folder_teste/teste_D_copy.csv')

## Copy Between Repositories
#data = storage.copy_between_repositories(src_repository='local_storage', src_path='folder_teste/teste_D.csv', dest_repository='local_storage_2', dest_path='folder_teste_x/teste_D_copy.csv')

## Exists
#print(storage.exists(file_path='folder_teste/teste_D.csv'))

## Get Metadata
#print(storage.get_metadata(file_path='folder_teste/teste_D.csv'))

## Get File URL
#print(storage.get_file_url(file_path='folder_teste/teste_D.csv'))
