import pandas as pd


def export_to_excel(df, output_path):
    """
    Export final dataset to Excel file.
    """

    df.to_excel(
        output_path,
        index=False
    )

    print(
        f"Output file created: {output_path}"
    )