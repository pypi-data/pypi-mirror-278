
def hello():
    import os 
    name = os.popen("whoami").read().strip()
    print(f"Hello {name}")

def table(dict):
    import pandas as pd
    from tabulate import tabulate

    df = pd.DataFrame(dict)
    structure = tabulate(df, headers='keys', tablefmt='psql')

