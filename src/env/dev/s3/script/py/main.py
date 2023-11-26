import boto3

bucket_name = "tester-bucket-final"
s3_client = boto3.client('s3')

def record_zip_file_sizes(bucket, folder_key):
    # print(f"Recording zip file sizes for folder: {folder_key}")

    sizes = []  # To store zip file sizes

    # Use list_objects_v2 to get objects in the folder
    objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder_key)

    zip_files = []  # To store details about each zip file

    # Check if the object is directly within the specified folder
    for obj in objects.get('Contents', []):
        if not obj['Key'].endswith('/'):
            file_size = obj['Size']
            sizes.append(file_size)

            # Extract details of zip files
            if obj['Key'].endswith('.zip'):
                zip_files.append({
                    'name': obj['Key'],
                    'size': file_size
                })

    total_size_kb = sum(sizes) / 1024  # Convert total size to kilobytes

    # Print details about zip files
    print(f"Within {folder_key} there are {len(zip_files)} zip files.")
    print(f"The total file size is {total_size_kb:.2f} KB.")

    for zip_file in zip_files:
        print(f"  - {zip_file['name']}: {zip_file['size']} bytes")

    return sizes

# Use keyword arguments for list_objects_v2
objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="archive/GroupId=none/")

for obj in objects.get('Contents', []):
    folder_key = obj['Key']

    # Check if the object is a folder
    if obj['Size'] == 0 and folder_key.endswith('/'):
        # Split the folder path and extract CollectionDate, DataFeedId, and DataFeedTaskId
        parts = folder_key.split('/')
        collection_date = None
        data_feed_id = None
        data_feed_task_id = None
        for part in parts:
            if part.startswith("CollectionDate="):
                collection_date = part
            elif part.startswith("DataFeedId="):
                data_feed_id = part
            elif part.startswith("DataFeedTaskId="):
                data_feed_task_id = part

        # Check if the folder has CollectionDate, DataFeedId, and DataFeedTaskId
        if collection_date and data_feed_id and data_feed_task_id:
            # Extract the DataFeedId value
            data_feed_id_value = data_feed_id.split('=')[1]

            # Check if the DataFeedId is 2
            if data_feed_id_value == '2':
                # Record zip file sizes and details
                zip_sizes = record_zip_file_sizes(bucket_name, folder_key)

                # Calculate and print statistics
                if zip_sizes:
                    avg_size = sum(zip_sizes) / len(zip_sizes)
                    max_size = max(zip_sizes)
                    print(f"Average Zip File Size: {avg_size} bytes")
                    print(f"Max Zip File Size: {max_size} bytes")
                else:
                    print("No zip files found.")
                
                # Stop the loop when the first DataFeedTaskId is found
                break
