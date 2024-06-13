import numpy as np
import pandas as pd

def shannon_diversity(
        df: pd.DataFrame, 
        column: str="frequency") -> float:
    # Convert the frequency list to a numpy array if it's not already one
    frequencies = df[column].values
    # Calculate the proportions
    proportions = frequencies / frequencies.sum()
    # Calculate the Shannon diversity index
    shannon_diversity = -np.sum(proportions * np.log(proportions))
    return shannon_diversity