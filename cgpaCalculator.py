import pandas as pd
from io import StringIO

def calculate_cgpa(data):
    res = data
    start_idx = res.find("Course type") + len("Course type")
    end_idx = res.find("Showing")

    result = res[start_idx:end_idx].strip()
    import re

    formatted_data = []
    for line in result.strip().split("\n"):
        # Search for the first occurrence of three consecutive digits
        match = re.search(r"\d{3}", line)
        if match:
            # Extract the part up to and including the digits
            start_part = line[:match.end()]
            # Extract the remaining part and normalize it
            rest_part = "/".join(line[match.end():].split())
            # Combine the two parts
            line = start_part + "/" + rest_part if rest_part else start_part
        else:
            # Normalize the entire line if no digits are found
            line = "/".join(line.split())
        
        # Append the formatted line to the result
        formatted_data.append(line)

    # Combine all formatted lines
    resultTarget = "\n".join(formatted_data)

    # Display the result
    print(resultTarget)


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
    df['Grade'] = df['Result']
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
    df.drop(columns=['Result'], inplace=True)
    return df, resultDataframe, cgpa  # Return df along with the summary dataframe and CGPA
