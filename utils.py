import pandas as pd
from io import BytesIO

def parse_csv(file_content: bytes, skip_rows: int = 0) -> pd.DataFrame:
    """
    Reads a CSV file from bytes, skips the specified number of rows,
    and returns a DataFrame

    :param file_content: The CSV file content as bytes
    :param skip_rows: The number of header rows to skip
    :return: pandas DataFrame
    """
    try:
        df = pd.read_csv(BytesIO(file_content), skiprows=skip_rows)
        return df
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")
from io import BytesIO
