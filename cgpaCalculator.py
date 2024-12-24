import pandas as pd
from io import StringIO

def calculate_cgpa(data):
    res = data
    start_idx = res.find("Course type") + len("Course type")
    end_idx = res.find("Showing")

    result = res[start_idx:end_idx].strip()
    formatted_data = []
    for line in result.strip().split("\n"):
        formatted_data.append("/".join(line.split()))
    resultTarget = "\n".join(formatted_data)

    columns = ["Course Code", "Course Credit", "Level", "LevelNo", "Hyphen",
               "Term", "TermNo", "Sessional", "Result", "Course Type"]

    df = pd.read_csv(StringIO(resultTarget), sep='/', header=None, names=columns, engine='python', index_col=None)
    df = df.drop(columns=["Hyphen"])

    map_result = {
        'A+': 4.00,
        'A': 3.75,
        'A-': 3.50,
        'B+': 3.25,
        'B': 3.00,
        'B-': 2.75,
        'C+': 2.50,
        'C': 2.25,
        'D': 2.00,
        'F': 0.00
    }

    df['Result'] = df['Result'].map(map_result)

    resultDataframe = pd.DataFrame(columns=["Level", "Term", "TotalCredit", "GPA"])
    cgpagradeSum = 0
    cgpacred = 0

    for i in range(1, 5):
        for j in range(1, 5):
            currentdf = df[(df['LevelNo'] == i) & (df['TermNo'] == j)]
            if currentdf.empty:
                continue
            cred = 0
            gradeSum = 0
            for _, row in currentdf.iterrows():
                if(row['Result'] == 0):
                    continue   
                cred += row['Course Credit']
                gradeSum += row['Course Credit'] * row['Result']
                cgpagradeSum += row['Course Credit'] * row['Result']
                cgpacred += row['Course Credit']
            gpa = round(gradeSum / cred, 2)
            resultDataframe.loc[len(resultDataframe)] = [i, j, cred, gpa]

    cgpa = round(cgpagradeSum / cgpacred, 2)

    # df.drop(columns=["Level", "Term"], inplace=True)
    df['Level'] = df['LevelNo']
    df['Term'] = df['TermNo']
    df.drop(columns=["LevelNo", "TermNo"], inplace=True)
    return df, resultDataframe, cgpa  # Return df along with the summary dataframe and CGPA
