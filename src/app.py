import os
import random

from werkzeug import secure_filename
from flask import Flask, flash, request, redirect, url_for
from azure.storage.filedatalake import (
    DataLakeServiceClient,
)

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

account_name = os.getenv('STORAGE_ACCOUNT_NAME', "")
account_key = os.getenv('STORAGE_ACCOUNT_KEY', "")

# set up the service client with the credentials from the environment variables
service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
    "https",
    account_name
), credential=account_key)

print("Connected to service client")

# generate a random name for testing purpose
fs_name = "testfs{}".format(random.randint(1, 1000))
print("Generating a test filesystem named '{}'.".format(fs_name))

# create the filesystem
filesystem_client = service_client.create_file_system(file_system=fs_name)

print("Created filesystem")

def upload_file(filesystem_client, file):
    # create a file before writing content to it
    print("Getting filename")
    file_name = file.filename
    print("Creating a file named '{}'.".format(file_name))
    file_client = filesystem_client.create_file(file_name)

    # prepare the file content with 4KB of random data
    print("Getting file contents")
    file_contents = file.read()

    print("Uploading data")
    file_client.append_data(data=file_contents, offset=0, length=len(file_contents))

    print("Flushing data")
    file_client.flush_data(len(file_contents))


def allowed_file(filename):
    #Check if file contains extension and if it is allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def homepage():
    
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print("Empty filename")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                upload_file(filesystem_client, file)
                return b'Upload Successful'
            except:
                return b'Upload Failed'
    
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')