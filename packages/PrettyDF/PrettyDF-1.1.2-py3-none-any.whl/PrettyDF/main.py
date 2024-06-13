
def hello():
    import os 
    name = os.popen("whoami").read().strip()
    print(f"Hello {name}")

def table(dict):
    import pandas as pd
    from tabulate import tabulate

    df = pd.DataFrame(dict)
    structure = tabulate(df, headers='keys', tablefmt='psql')
    print(structure)

def visual(dict, style, **kwargs):
    import pandas as pd
    import warnings
    import matplotlib.pyplot as plt

    try:
        warnings.filterwarnings("ignore")

        df = pd.DataFrame(dict)
        
        if df.empty:
            raise ValueError("Empty Dataframe. Please add some values.")
        
        if style not in ['line', 'bar', 'barh', 'hist', 'box', 'area', 'scatter']:
            raise ValueError(f"Invalid plot type '{style}'. Supported types: 'line', 'bar', 'barh', 'hist', 'box', 'area', 'scatter'.")
        
        plot = df.plot(kind=style, **kwargs)
        
        if 'xlabel' not in kwargs:
            plt.xlabel("Index")
        if 'ylabel' not in kwargs:
            plt.ylabel("Values")
        if 'title' not in kwargs:
            plt.title(f"{style.capitalize()} Plot")
        
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")