i=0

S3_BUCKET="tester-bucket-final"  # Specify your S3 bucket name

numOfFolders=(`aws s3 ls s3://$S3_BUCKET/archive/GroupId=none/ | wc -l`)

((numOfFolders=$numOfFolders-1))

echo $numOfFolders

for ((i=0; i<numOfFolders; i++)); do
    aws s3 ls s3://$S3_BUCKET/archive/GroupId=none/CollectionDate=2018-10-102/



done
