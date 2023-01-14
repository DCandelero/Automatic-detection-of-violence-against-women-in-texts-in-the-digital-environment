import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings


def initialize_storage_account(storage_account_name, storage_account_key):
    
    try:  
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)
    
    except Exception as e:
        print(e)

def create_file_system(container_name:str):
    try:
        global file_system_client

        file_system_client = service_client.create_file_system(file_system=container_name)
    
    except Exception as e:
        print(e)

def delete_file_system(container_name:str):
    try:
        service_client.delete_file_system(file_system=container_name)
    
    except Exception as e:
        print(e)

def create_directory(container_name:str, directory_name:str):
    try:

        file_system_client = service_client.get_file_system_client(file_system=container_name)
        file_system_client.create_directory(directory_name)
    
    except Exception as e:
     print(e)

def rename_directory(container_name:str, old_directory_name:str, new_directory_name:str):
    try:
       
       file_system_client = service_client.get_file_system_client(file_system=container_name)
       directory_client = file_system_client.get_directory_client(old_directory_name)
       
       new_dir_name = new_directory_name
       directory_client.rename_directory(new_name=directory_client.file_system_name + '/' + new_dir_name)

    except Exception as e:
     print(e)

def delete_directory(container_name:str, directory_name:str):
    try:
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        directory_client = file_system_client.get_directory_client(directory_name)

        directory_client.delete_directory()
    except Exception as e:
     print(e)

def upload_file_to_directory(container_name:str, directory_name:str, file_path:str, file_name_to_save:str):
    try:

        file_system_client = service_client.get_file_system_client(file_system=container_name)

        directory_client = file_system_client.get_directory_client(directory_name)
        
        file_client = directory_client.create_file(file_name_to_save)

        local_file = open(file_path,'r', encoding="utf8")
        file_contents = local_file.read()

        file_client.append_data(data=file_contents, offset=0, length=len(file_contents))

        file_client.flush_data(len(file_contents))

    except Exception as e:
      print(e)

def upload_file_to_directory_bulk(container_name:str, directory_name:str, file_path:str, file_name_to_save:str):
    try:

        file_system_client = service_client.get_file_system_client(file_system=container_name)

        directory_client = file_system_client.get_directory_client(directory_name)
        
        file_client = directory_client.get_file_client(file_name_to_save)

        local_file = open(file_path,'r')
        file_contents = local_file.read()

        file_client.upload_data(file_contents, overwrite=True)

    except Exception as e:
      print(e)

def download_file_from_directory(container_name:str, directory_name:str, file_name:str, path_to_save:str):
    try:
        file_system_client = service_client.get_file_system_client(file_system=container_name)

        directory_client = file_system_client.get_directory_client(directory_name)
        
        local_file = open(path_to_save,'wb')

        file_client = directory_client.get_file_client(file_name)

        download = file_client.download_file()

        downloaded_bytes = download.readall()

        local_file.write(downloaded_bytes)

        local_file.close()

    except Exception as e:
     print(e)

def list_directory_contents(container_name:str, directory_name:str):
    try:
        
        file_system_client = service_client.get_file_system_client(file_system=container_name)

        paths = file_system_client.get_paths(path=directory_name)

        for path in paths:
            print(path.name + '\n')

    except Exception as e:
     print(e)