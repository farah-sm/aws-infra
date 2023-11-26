#!/bin/bash

AWS_PROFILE="your_aws_profile"  # Specify your AWS CLI profile
S3_BUCKET="tester-bucket-final"  # Specify your S3 bucket name

num_folders=490
num_files_per_type=3
file_types=("json" "xml")

function create_files() {
    file_type=$1
    num_files=$2
    folder_name=$3

    mkdir "$folder_name"
    for ((j=1; j<=num_files; j++)); do
        file_size=$((RANDOM % 1024 + 1))  # Generate random file size between 1 and 1024 bytes
        dd if=/dev/urandom of="$folder_name/file_${j}.$file_type" bs=$file_size count=1
    done
}

function zip_folder() {
    folder_name=$1
    zip -r "$folder_name.zip" "$folder_name"
}

function upload_to_s3() {
    folder_name=$1
    folder_zip="$folder_name.zip"
    DataFeedId=$2
    taskId=$3
    aws s3 cp $folder_zip "s3://$S3_BUCKET/archive/GroupId=none/$folder/DataFeedId=$DataFeedId/DataFeedTaskId=$taskId/$folder_zip"
}

function main() {
    # Initial date
    YYYY=2020
    MM=10
    DD=12

    # Create the base directory in S3 bucket
    aws s3api put-object --bucket "$S3_BUCKET" --key "archive/GroupId=none/"

    for ((i=0; i<num_folders; i++)); do
        export folder="CollectionDate=$YYYY-$MM-$DD"

        # Set feedId for every 4th iteration
        if ((i % 4 == 0)); then
            feedId=2
        else
            feedId=$((RANDOM%3))
        fi

        aws s3api put-object --bucket "$S3_BUCKET" --key "archive/GroupId=none/$folder/"
        aws s3api put-object --bucket "$S3_BUCKET" --key "archive/GroupId=none/$folder/DataFeedId=$feedId/"
       
        taskId1=$((RANDOM%100000))
        aws s3api put-object --bucket "$S3_BUCKET" --key "archive/GroupId=none/$folder/DataFeedId=$feedId/DataFeedTaskId=$taskId1/"
        
        taskId2=$((RANDOM%100000))
        aws s3api put-object --bucket "$S3_BUCKET" --key "archive/GroupId=none/$folder/DataFeedId=$feedId/DataFeedTaskId=$taskId2/"

        for file_type in "${file_types[@]}"; do
            for j in {1..3}; do
                folder_name="${file_type}_folder_${j}"
                create_files "$file_type" "$num_files_per_type" "$folder_name"
                zip_folder "$folder_name"
                upload_to_s3 "$folder_name" "$feedId" "$taskId1"
                rm -rf "$folder_name"  # Remove the folder after zipping

                folder_name="${file_type}_folder_${j}"
                create_files "$file_type" "$num_files_per_type" "$folder_name"
                zip_folder "$folder_name"
                upload_to_s3 "$folder_name" "$feedId" "$taskId2"
                rm -rf "$folder_name"  # Remove the folder after zipping
            done
        done

        # Increment the date
        if [ $YYYY -gt 2019 ] && [ $YYYY -lt 2023 ]; then
            ((YYYY++))
        elif [ $YYYY -gt 2023 ] || [ $YYYY -eq 2023 ]; then
            ((YYYY-=5))
        fi

        if [ $MM -gt 3 ] && [ $MM -lt 11 ]; then
            ((MM++))
        elif [ $MM -gt 11 ] || [ $MM -eq 11 ]; then
            ((MM-=5))
        fi

        if [ $DD -gt 3 ] || [ $DD -lt 29 ]; then
            ((DD++))
        else
            ((DD-=17))
        fi
    done
}

main
