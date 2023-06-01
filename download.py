import shutil
import urllib.request

url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
save_name = 'ml-100k.zip'

urllib.request.urlretrieve(url, save_name)
shutil.unpack_archive(save_name)
