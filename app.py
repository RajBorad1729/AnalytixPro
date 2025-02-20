from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from utils.file_operations import save_uploaded_file, load_csv
from analysis.data_preprocessing import preprocess_data
from analysis.visualization import create_visualizations
from analysis.statistical_analysis import calculate_statistics
from analysis.machine_learning import train_model

app = Flask(__name__)
global_data = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global global_data
    if request.form.get('reset_filters') == 'true':
        global_data = None
    file = request.files.get('file')
    if file:
        file_path = save_uploaded_file(file)
        data = load_csv(file_path)
        if data is not None:
            processed_data = preprocess_data(data)
            global_data = processed_data

            filters = {
                'City': processed_data['City'].unique().tolist(),
                'Region': processed_data['Region'].unique().tolist(),
                'Category': processed_data['Category'].unique().tolist(),
                'Year': processed_data['Year'].unique().tolist(),
            }

            statistics = calculate_statistics(processed_data)
            visuals = create_visualizations(processed_data)

            return render_template(
                'dashboard.html',
                visuals=visuals,
                Filters=filters,
                statistics=statistics
            )
    return redirect(url_for('index'))

@app.route('/filter_data', methods=['GET'])
def filter_data():
    global global_data
    if global_data is None:
        return "Error: Data not loaded.", 400

    selected_cities = request.args.getlist('city[]')
    selected_regions = request.args.getlist('region[]')
    selected_categories = request.args.getlist('category[]')
    selected_year = request.args.get('year')

    filtered_data = global_data
    if selected_cities:
        filtered_data = filtered_data[filtered_data['City'].isin(selected_cities)]
    if selected_regions:
        filtered_data = filtered_data[filtered_data['Region'].isin(selected_regions)]
    if selected_categories:
        filtered_data = filtered_data[filtered_data['Category'].isin(selected_categories)]
    if selected_year:
        filtered_data = filtered_data[filtered_data['Year'] == int(selected_year)]

    filters = {
        'City': global_data['City'].unique().tolist(),
        'Region': global_data['Region'].unique().tolist(),
        'Category': global_data['Category'].unique().tolist(),
        'Year': global_data['Year'].unique().tolist(),
    }

    statistics = calculate_statistics(filtered_data)
    visuals = create_visualizations(filtered_data)

    return render_template(
        'dashboard.html',
        visuals=visuals,
        Filters=filters,
        statistics=statistics,
        selected_cities=selected_cities,
        selected_regions=selected_regions,
        selected_categories=selected_categories,
        selected_year=selected_year
    )

@app.route('/reset_filters', methods=['GET'])
def reset_filters():
    global global_data
    if global_data is None:
        return "Error: Data not loaded.", 400

    filters = {
        'City': global_data['City'].unique().tolist(),
        'Region': global_data['Region'].unique().tolist(),
        'Category': global_data['Category'].unique().tolist(),
        'Year': global_data['Year'].unique().tolist(),
    }

    statistics = calculate_statistics(global_data)
    visuals = create_visualizations(global_data)

    return render_template(
        'dashboard.html',
        visuals=visuals,
        Filters=filters,
        statistics=statistics
    )

@app.route('/predict_sales', methods=['GET'])
def predict_sales():
    global global_data
    if global_data is None:
        return "Error: Data not loaded.", 400

    fig1_html, fig2_html = train_model(global_data)
    statistics = calculate_statistics(global_data)

    return render_template('prediction.html', prediction_graph1=fig1_html, prediction_graph2=fig2_html, statistics=statistics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
