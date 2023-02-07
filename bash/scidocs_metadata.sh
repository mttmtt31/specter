# Downloads the data folder from GDrive. 
# Since the task performed is only classification, the data folder has a size of around 250MB.

# specify the URL of the file you want to download
folder_url='https://drive.google.com/drive/folders/1iP-LHbYIgcYQA_0_yij75ZeFJ85UmqwG'

# specify the destination path for the downloaded file
destination_path='project_data/scidocs_metadata'

# download the file using gdown
gdown --folder $folder_url -O $destination_path

# check if the file was successfully downloaded
if [ $? -eq 0 ]; then
  echo "File downloaded successfully."
else
  echo "Failed to download the file."
fi