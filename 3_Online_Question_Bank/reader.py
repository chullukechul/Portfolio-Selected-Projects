import  pandas as pd
def read_excel(id):
    id = id - 1
    name = "schedule.xlsx"
    df = pd.read_excel(name)
    row_data = df.iloc[id].tolist()
    ret = row_data[1:6]
    return ret


def save_units_to_csv(units, file_path):
    df = pd.DataFrame(units, columns=["unit", "name", "status"])
    df.to_csv(file_path, index=False)


def load_units_from_csv(file_path):
    return pd.read_csv(file_path)