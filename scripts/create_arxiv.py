import json
from tqdm import tqdm
import os
import subprocess

def get_metadata(data_file:str):
    """Instead of loading the entire json in memory, scans through the lines one at the time.

    Args:
        data_file (str): path to the arxiv metadata json file

    Yields:
        str: non-parsed dictionary, contains one arxiv paper and its metadata.
    """
    with open(data_file, 'r') as f:
        for line in f:
            yield line

def get_kaggle_credentials(kaggle_cred_path:str):
    """Locates the kaggle.json file and retrieve the Kaggle API key

    Args:
        kaggle_cred_path (str): local path to the kaggle.json file

    Returns:
        str: Kaggle API key
    """
    # get kaggle api key. 
    with open(kaggle_cred_path) as f:
        kaggle_credentials = json.load(f)
    # retrieve key
    kaggle_username = kaggle_credentials["username"]
    kaggle_key = kaggle_credentials["key"]

    return kaggle_username, kaggle_key

def create_arxiv(data_dir:str=None, n_papers:int=50_000, kaggle_cred_path:str=None):
    """Create data.json and metadata.json as per SPECTER specifications using arXiv dataset.
    The original dataset can be retrieved either using a locally-saved json, or by interacting with the Kaggle API.
    The Kaggle API functionality is not supported on Windows.

    Args:
        data_dir (str, optional): path to local version of arxiv_metadata_json. Defaults to None.
        n_papers (int, optional): number of papers to consider in the subset. Defaults to 50_000.
        kaggle_cred_path (str, optional): path to kaggle API key. Defaults to None.

    Raises:
        ValueError: one (and only one) option between using a local version of the arXiv dataset and using the Kaggle API should be selected.
    """
    if data_dir is None and kaggle_cred_path is None:
        raise ValueError("If you want to use the kaggle API, please specify USERNAME, API KEY and URL\nIf you want to use a local directory, specify the path where the arxiv json is stored.")
    elif data_dir is not None and not kaggle_cred_path is None:
        raise ValueError("You specify both a local path and your kaggle credentials. Only one should be specified.")
    elif data_dir is not None:
        # obtain metadata file
        data_file = os.path.join(data_dir, 'arxiv-metadata-oai-snapshot.json')
    else:
        # obtain kaggle credentials
        kaggle_username, kaggle_key = get_kaggle_credentials(kaggle_cred_path)
        # connect to the API
        subprocess.run(["kaggle", "config", "set", "-n", "username", "-v", f"{kaggle_username}"])
        subprocess.run(["kaggle", "config", "set", "-n", "key", "-v", f"{kaggle_key}"])
        # Run the Kaggle API command to download the dataset
        subprocess.run(["kaggle", "datasets", "download", "-d", "Cornell-University/arxiv"])
        subprocess.run(["unzip", "arxiv.zip"])
        data_file = "arxiv-metadata-oai-snapshot.json"
   
    arxiv_metadata = get_metadata(data_file)
    # initialise counter: number of papers in the subset
    papers_in_subset = 0
    # initialise empty dictionary -> metadata.json will be built starting from this dictionary
    metadata = {}
    # create another dictionary, where the key is the paper_id and the value is the label (i.e., the category)
    labels = {}
    # iterate until you add `n_papers` papers in your subset
    with tqdm(total=n_papers) as pbar:
        for paper in arxiv_metadata:
            # load paper_information
            paper_dict = json.loads(paper)
            # try is necessary because not all fields are always defined
            try:
                # we only want to consider papers which belong to one and only one category
                # this should help obtaining us more reliable results for classification
                if len(paper_dict.get('categories').split(" ")) == 1:
                    # each paper's category is in the form category.topic (e.g., math.CO)
                    # we are restricting our analysis to the top-6 categories
                    if paper_dict.get('categories').split(".")[0] in ["astro-ph", "cs", "math", "physics", "q-bio", "stat"]:
                        # obtain paper_id. paper_id is slightly modified to make it more similar to Scidocs format 
                        paper_id = paper_dict.get('id').replace('.', '')[1:]
                        # add this papers to metadata.json
                        metadata[paper_id] = {
                            'paper_id' : paper_id, 
                            'title' : paper_dict.get('title'), 
                            'abstract' : paper_dict.get('abstract'), 
                        }
                        # add both category and topic to the labels dataframe
                        labels[paper_id] = {
                            'topic' : paper_dict.get('categories').split(".")[0],
                            'subtopic' : paper_dict.get('categories')
                            }
                        # increment number of papers in the subset
                        papers_in_subset += 1
                        pbar.update(1)
                        if papers_in_subset == n_papers:
                            break
            except:
                pass 

create_arxiv(data_dir=".")