import pandas as pd
import argparse
import re
from tabulate import tabulate
from termcolor import colored
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_requirements(file_path):
    """
    Parse a requirements.txt file into a dictionary of package names and version specifiers.

    Parameters:
    file_path (str): Path to the requirements.txt file.

    Returns:
    dict: A dictionary with package names as keys and version specifiers as values.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    requirements = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                match = re.match(r"([a-zA-Z0-9_-]+)([>=<~!]+[a-zA-Z0-9._-]+)?", line)
                if match:
                    pkg = match.group(1)
                    ver = match.group(2) if match.group(2) else "Any"
                    requirements[pkg.strip()] = ver.strip()
    return requirements


def compare_requirements(files):
    """
    Compare multiple requirements.txt files and return a DataFrame of the differences.

    Parameters:
    files (list of str): List of paths to the requirements.txt files.

    Returns:
    pd.DataFrame: A DataFrame showing the package versions from each file.
    """
    all_requirements = {}

    for file in files:
        requirements = parse_requirements(file)
        all_requirements[file] = requirements

    df = pd.DataFrame(all_requirements).fillna("Not Present")
    df.index.name = "Package"
    df.reset_index(inplace=True)
    return df


def highlight_differences(df):
    """
    Highlight differences in package versions in a DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame of package versions.

    Returns:
    pd.DataFrame: DataFrame with highlighted differences.
    """
    df_highlighted = df.copy()
    for idx, row in df.iterrows():
        versions = row[1:]
        if len(set(versions)) > 1:
            df_highlighted.loc[idx, row.index[1:]] = [
                colored(ver, "red") if ver != "Not Present" else colored(ver, "blue")
                for ver in versions
            ]
        elif "Not Present" in versions.values:
            df_highlighted.loc[idx, row.index[1:]] = [
                colored(ver, "blue") if ver == "Not Present" else ver
                for ver in versions
            ]
    return df_highlighted


def filter_differences(df):
    """
    Filter the DataFrame to only include packages with differing versions.

    Parameters:
    df (pd.DataFrame): DataFrame of package versions.

    Returns:
    pd.DataFrame: Filtered DataFrame with only differing package versions.
    """
    df_filtered = df[df.apply(lambda row: len(set(row[1:])) > 1, axis=1)]
    return df_filtered


def main():
    """
    Main function to parse arguments and compare requirements files.
    """
    parser = argparse.ArgumentParser(
        description="Compare multiple requirements.txt files."
    )
    parser.add_argument(
        "files",
        metavar="F",
        type=str,
        nargs="+",
        help="Paths to the requirements.txt files",
    )
    parser.add_argument(
        "--only-diff",
        action="store_true",
        help="Only show packages with differing versions",
    )

    args = parser.parse_args()
    try:
        comparison_df = compare_requirements(args.files)
    except FileNotFoundError as e:
        logging.error(e)
        return

    if args.only_diff:
        comparison_df = filter_differences(comparison_df)
    highlighted_df = highlight_differences(comparison_df)

    # Display the comparison with highlights
    logging.info(tabulate(highlighted_df, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
