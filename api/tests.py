from django.test import TestCase
#from .models import Data_Mapping_Files
# Create your tests here.
import pandas as pd
import os
import glob


def ABSOLUTE_PATH(x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), x)


if __name__ == "__main__":
    MEDIA_ROOT = ABSOLUTE_PATH('media\mapping')
    MEDIA_ROOT = MEDIA_ROOT[:1].upper()+MEDIA_ROOT[1:]
    print(MEDIA_ROOT)
    folder_path = r'C:\Users\Masterspace\Documents\projects\HealITProjects\middlewareapi\media\mapping'
    res = []
    # Iterate directory
    for path in os.listdir(folder_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    print(res)
    csvfile = os.path.join(folder_path, res[-1])
    print(csvfile)
    df = pd.read_csv(csvfile)
    df.head()
