import boto3

bucket_name = "tester-bucket-final"

s3_client = boto3.client('s3')

def print_zip_file_sizes(bucket, folder_key):
    print(f"Printing zip file sizes for folder: {folder_key}")

    # Use list_objects_v2 to get objects in the folder
    objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder_key)

    for obj in objects.get('Contents', []):
        file_size = obj['Size']
        print(f"Zip File: {obj['Key']} - Size: {file_size} bytes")

# Function to record zip file sizes
def record_zip_file_sizes(bucket, folder_key):
    print(f"Recording zip file sizes for folder: {folder_key}")

    sizes = []  # To store zip file sizes

    # Use list_objects_v2 to get objects in the folder
    objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder_key)

    for obj in objects.get('Contents', []):
        file_size = obj['Size']
        sizes.append(file_size)

    return sizes

# Use keyword arguments for list_objects_v2
objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="archive/GroupId=none/")

for obj in objects.get('Contents', []):
    folder_key = obj['Key']

    # Check if the object is a folder
    if obj['Size'] == 0 and folder_key.endswith('/'):
        # Split the folder path and extract CollectionDate and DataFeedId
        parts = folder_key.split('/')
        collection_date = None
        data_feed_id = None
        for part in parts:
            if part.startswith("CollectionDate="):
                collection_date = part
            elif part.startswith("DataFeedId="):
                data_feed_id = part

        # Check if the folder has CollectionDate and DataFeedId
        if collection_date and data_feed_id:
            # Extract the DataFeedId value
            data_feed_id_value = data_feed_id.split('=')[1]

            # Check if the DataFeedId is 2
            if data_feed_id_value == '2':
                # Extract DataFeedTaskId
                data_feed_task_id = None
                for part in parts:
                    if part.startswith("DataFeedTaskId="):
                        data_feed_task_id = part

                if data_feed_task_id:
                    # Print zip file sizes
                    print_zip_file_sizes(bucket_name, folder_key + data_feed_id + '/' + data_feed_task_id)
