# Set the URL of the Google Drive file
id="12705EBf4KgPR5Q3aYeJP_3EcM73pPmd4"
destination_path="archive.tar.gz"

echo "Downloading datasets"
# Download the file
gdown $id -O $destination_path

echo "Extracting datasets..."

# Extract the tar.gz file
tar -xzvf $destination_path

#### MODELS ####
mkdir "pretrained_models"

id="1CajAbbmrNZo_TNc24VVg8j2Qdz8hJn0N"
destination_path="pretrained_models/model_specter.tar.gz"

echo "Downloading model: specter"
# Download the file
gdown $id -O $destination_path

echo "Extracting model: specter..."

# Extract the tar.gz file
tar -xzvf $destination_path

id="1D-e1qcM_bMHYPkl7vUFSL6a5PbaBfSZW"
destination_path="pretrained_models/model_spectroid.tar.gz"

echo "Downloading model: spectroid"
# Download the file
gdown $id -O $destination_path

echo "Extracting model: spectroid..."

# Extract the tar.gz file
tar -xzvf $destination_path
