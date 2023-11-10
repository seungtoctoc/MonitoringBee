from flask import Flask, render_template, request
import os

app = Flask(__name__, static_folder='/server/download/image')

IMAGE_FOLDER = '/server/download/image'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search')
    
    image_names = os.listdir(app.config['UPLOAD_FOLDER'])
    image_names_filtered = [file for file in image_names if file.lower().endswith('.jpg')]
    image_names_sorted = sorted(image_names_filtered)

    if search_query:
        search_results = [image_name for image_name in image_names_sorted if search_query in image_name]
        
    else:
        search_results = image_names_sorted

    image_groups = [search_results[i:i + 4] for i in range(0, len(search_results), 4)]

    loaded_data = {}
    
    with open('/server/download/data.txt', 'r') as file:
        lines = file.readlines() 
        
        for line in lines:
            key, value = line.strip().split(': ')
            loaded_data[key] = value 

    return render_template('index.html', image_groups=image_groups, search_query=search_query, loaded_data = loaded_data)

if __name__ == '__main__':
    app.run(debug=True)