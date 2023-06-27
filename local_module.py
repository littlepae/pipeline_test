import pandas as pd
from clearml import StorageManager
def test_print():
    print('use local module')
    # df = StorageManager.get_local_copy(remote_url="https://github.com/littlepae/pipeline_test/blob/main/test_csv.csv")
    # print(df)
    df = pd.read_csv("./test_csv.csv")
    print(df)
    print(type(df))
    return