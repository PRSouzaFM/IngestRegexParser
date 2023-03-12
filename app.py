import os
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import datetime
import re
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Files'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_id():
    current_time = datetime.datetime.now()
    unique_id = current_time.strftime("%Y%m%d%H%M%S")
    return unique_id


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file")
        if 'file' not in request.files:
            flash('ERR - 01 - NO FILE PART')
            return redirect(request.url)
        if request.files['file'].filename == '':
            return 'Sem arquivos selecionados'
        folderPath = os.path.join(app.config["UPLOAD_FOLDER"],
                                  str(generate_unique_id()))
        # check if the post request has the file part
        merger = PdfMerger()
        os.mkdir(folderPath)
        for file in files:
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(folderPath, filename))
                merger.append(os.path.join(folderPath, filename))
        pautaPath = os.path.join(folderPath, "Pauta.pdf")  # Path to pdf file
        merger.write(pautaPath)
        reader = PdfReader(pautaPath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(text)
        pattern = r"^(\S+\s+)?(\d[0-9]+)\s+(?:\d[0-9]+)\s+([\w\s\W]+?)\s*(?=(?:Sim|Não|$))"
        result = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
        print(result)
        cmDict = {}
        for match in result:
            type = match[0]
            cmId = match[1]
            title = match[2]
            cmDict[cmId] = (type, title)
        date = datetime.datetime.today().strftime('%B %d, %Y')
        return render_template("cmlist.html", cmDict=cmDict, date=date)
    return render_template('template.html')


if __name__ == "__main__":
    app.run(debug=True)
