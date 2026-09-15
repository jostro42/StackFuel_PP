import pandas as pd
from IPython.display import display

# ----------------------------------------------------------------------------


def overview(df, transpose_overview=False):
    """
    Create first overview of data set as well as descriptive metrics for numerical variables
    VARs
        df: pd.DataFrame to be viewed
    RETURNS:
        None
    """
    df = df.copy()

    # Check for duplicate rows
    dupl_mask = df.duplicated()
    n_duplicates = dupl_mask.sum()
    dup_indices = df.index[dupl_mask].tolist()
    print(f"Duplicates: {n_duplicates}\n")
    if n_duplicates:
        print(f"Duplicate indices: {dup_indices}")

    # Gather information on dtype, missing values, uniques, etc.
    ov = pd.DataFrame(
        {
            "dtype": df.dtypes,
            "total": df.count(),
            "missing_n": df.isna().sum(),
            "missing_%": df.isna().mean() * 100,
            "uniques_n": df.nunique(),
            "uniques": [df[col].unique() for col in df.columns],
        }
    )

    print("Auto Sales Data - Variable Overview")
    if transpose_overview:
        display(ov.transpose())
    else:
        display(ov)
    print()

    # extract objects containing only numerical and non-numerical/non-datetype variables
    num_vars = df.select_dtypes(include="number").dtypes.to_frame(name="dtype")
    non_num = df.select_dtypes(exclude=["number", "datetime"])
    cat_vars = pd.DataFrame({"dtype": non_num.dtypes, "n_uniques": non_num.nunique()})

    # print out information
    print("Descriptive Metrics on numeric variables")
    display(df.describe())
    print()
    print("Numeric Variables in the data set")
    display(num_vars)
    print()
    print("Non-numeric variables in the data set")
    display(cat_vars)

    return ov, num_vars, cat_vars
