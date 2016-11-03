
import pandas as pd






if __name__ == '__main__':
    xl = pd.ExcelFile("../corpus-final09.xls")
    print(xl.sheet_names)
    df = xl.parse("File list")
    print(df)