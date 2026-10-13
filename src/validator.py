def validate_columns(df, required_columns): 
    # check required columns in df

    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)
    if missing_columns == []:
        return "there is not missing column"
    return missing_columns


def check_missing_values(df):
    # find missing values in df 

    missing_values = df.isnull().sum()
    return missing_values[missing_values>0]


def check_negative_amount(df, amount_column):
    # check  negative amounts

    if amount_column not in df.columns:
        return None
    
    negative_rows = df[df[amount_column]<0]
    if negative_rows.empty:
        return "No negative amounts found"
    return negative_rows


# warning whenever there is a nan or negative valuses
def validate_numeric_values(df):
    """
    Check numeric columns for zero or negative values
    and return warnings.
    """

    warnings = []

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns


    for column in numeric_columns:

        zero_values = df[
            df[column] == 0
        ]

        if not zero_values.empty:
            warnings.append(
                f"Warning: Zero values found in column '{column}'"
            )


        negative_values = df[
            df[column] < 0
        ]

        if not negative_values.empty:
            warnings.append(
                f"Warning: Negative values found in column '{column}'"
            )

    for warning in warnings:
        print(warning)


def check_period_consistency(df):
    """
    Warn when some rows carry a period different from the one used by most rows
    of the file (for example a row of the previous month inside this month's file).
    Returns the rows that differ.
    """

    if "period" not in df.columns or df.empty:
        return df.iloc[0:0]

    main_period = df["period"].mode()[0]
    different = df[df["period"] != main_period]

    if not different.empty:
        print(
            f"Warning: {len(different)} row(s) have a period different "
            f"from the rest of the file ({main_period}):"
        )
        print(different)

    return different
