from flask import Flask, request, render_template
from cgpaCalculator import calculate_cgpa  # Import the renamed function

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # Get the input data from the form
    user_input = request.form.get('user_input')

    # Call the calculate_cgpa function to process the input
    try:
        df, resultDataframe, cgpa = calculate_cgpa(user_input)
    except Exception as e:
        return f"Error processing input: {e}"

    # Prepare data for rendering in result.html
    gpa_boxes = {}
    for _, row in resultDataframe.iterrows():
        key = f"Level {int(row['Level'])} Term {int(row['Term'])}"
        gpa_boxes[key] = row['GPA']

    # Convert the dataframe to HTML
    df_html = df.to_html(classes='dataframe', header=True, index=False)

    return render_template('result.html', cgpa=cgpa, gpa_boxes=gpa_boxes, df_html=df_html)
if __name__ == '__main__':
    app.run(debug=True)
