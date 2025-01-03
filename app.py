from flask import Flask, request, render_template
from cgpaCalculator import calculate_cgpa  

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    
    user_input = request.form.get('user_input')

    
    try:
        df, resultDataframe, cgpa = calculate_cgpa(user_input)
    except Exception as e:
        return f"Error processing input: {e}"

    
    gpa_boxes = {}
    for _, row in resultDataframe.iterrows():
        key = f"Level {int(row['Level'])} Term {int(row['Term'])}"
        gpa_boxes[key] = row['GPA']

    
    df_html = df.to_html(classes='dataframe', header=True, index=False)

    return render_template('result.html', cgpa=cgpa, gpa_boxes=gpa_boxes, df_html=df_html)
if __name__ == '__main__':
    app.run(debug=True)
