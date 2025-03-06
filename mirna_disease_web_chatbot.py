import pandas as pd
from flask import Flask, request, render_template_string

app = Flask(__name__)

def load_matrix(file_path):
    """Load the adjacency matrix from a CSV file."""
    return pd.read_csv(file_path, index_col=0)

def get_mirnas_for_disease(matrix, disease):
    """Get all miRNAs associated with a disease where the matrix value is > 0."""
    if disease not in matrix.columns:
        return f"Disease '{disease}' not found in the matrix."
    associated_mirnas = matrix.index[matrix[disease] > 0].tolist()
    return associated_mirnas if associated_mirnas else f"No miRNAs associated with '{disease}'."

def get_diseases_for_mirna(matrix, mirna):
    """Get all diseases associated with a miRNA where the matrix value is > 0."""
    if mirna not in matrix.index:
        return f"miRNA '{mirna}' not found in the matrix."
    associated_diseases = matrix.columns[matrix.loc[mirna] > 0].tolist()
    return associated_diseases if associated_diseases else f"No diseases associated with '{mirna}'."

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <title>miRNA-Disease Chatbot</title>
        <h1>Welcome to the miRNA-Disease Chatbot</h1>
        <form action="/results" method="post">
            <label for="file_path">CSV File Path:</label><br>
            <input type="text" id="file_path" name="file_path"><br><br>
            <label for="query_type">Choose a query:</label><br>
            <select id="query_type" name="query_type">
                <option value="disease_to_mirnas">List miRNAs associated with a disease</option>
                <option value="mirna_to_diseases">List diseases associated with a miRNA</option>
            </select><br><br>
            <label for="query_value">Enter Disease or miRNA:</label><br>
            <input type="text" id="query_value" name="query_value"><br><br>
            <input type="submit" value="Submit">
        </form>
    ''')

@app.route('/results', methods=['POST'])
def results():
    file_path = request.form['file_path']
    query_type = request.form['query_type']
    query_value = request.form['query_value']

    try:
        matrix = load_matrix(file_path)
    except FileNotFoundError:
        return "File not found. Please check the file path and try again."
    except Exception as e:
        return f"An error occurred: {e}"

    if query_type == "disease_to_mirnas":
        result = get_mirnas_for_disease(matrix, query_value)
        return render_template_string(f'''
            <h1>Results</h1>
            <p>miRNAs associated with '{query_value}': {result}</p>
            <a href="/">Go Back</a>
        ''')
    elif query_type == "mirna_to_diseases":
        result = get_diseases_for_mirna(matrix, query_value)
        return render_template_string(f'''
            <h1>Results</h1>
            <p>Diseases associated with '{query_value}': {result}</p>
            <a href="/">Go Back</a>
        ''')
    else:
        return "Invalid query type."

if __name__ == "__main__":
    gunicorn main:app

