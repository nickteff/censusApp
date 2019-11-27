import pandas as pd


df = pd.read_csv("compute/static/census_raw.csv")

ages = df.iloc[:, range(10,23)]

ages = ages.assign(
    genZ = df.iloc[:, range(10,13)].sum(axis=1),
    millenial = df.iloc[:, range(13,16)].sum(axis=1),
    genX = df.iloc[:, range(16,18)].sum(axis=1),
    boomer = df.iloc[:, range(18,21)].sum(axis=1),
    silent = df.iloc[:, range(21,23)].sum(axis=1),
)

ages = ages.iloc[:, [-1, -2, -3, -4, -5]]

income = df.iloc[:, range(36,46)]

income = income.assign(
    lowIncome = df.iloc[:, range(36,40)].sum(axis=1),
    middleIncome = df.iloc[:, range(40,42)].sum(axis=1),
    highIncome = df.iloc[:, range(42,46)].sum(axis=1),
)

income = income.iloc[:, -3:]

house = df.iloc[:, [64, 67, 68, 69, 70]]

house = house.assign(HHLD_INDIV = house.iloc[:, -2:].sum(axis=1))

house = house.iloc[:, [0, 1, 2, -1]]

earnings = df.iloc[:, [31, 32, 34]]

edu = df.iloc[:, [75, 76]]

edu = edu.assign(
    COLLEGE_NO_BACH = df.iloc[: , [77, 72]].sum(axis=1),
    HS_DIP = df.iloc[:, 74],
    NO_HS_DIP = df.iloc[:, [73, 78]].sum(axis=1),
)

census = pd.concat(
    [
        df.iloc[:, [0, 3, 4, 5, 6, 7, 8, 9]],
        ages,
        income,
        house,
        edu,
        earnings
    ],
    axis=1
)

census = census.assign(Urban=[urban(row.MSA_CODE) for row in df.loc[:, ["MSA_CODE"]].itertuples()])



census.to_csv("compute/static/census.csv")


def urban(row):
    if row == 0:
        return 'rural'
    else:
        return 'urban'
