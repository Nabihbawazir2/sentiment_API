import boto3
import zipfile
import os

LAMBDA_FUNCTION_NAME = 'SentimentAnalysisAPI'
ZIP_FILE = 'deployment_package.zip'
SOURCE_DIR = './src'  # your source code folder

def zip_source_code():
    with zipfile.ZipFile(ZIP_FILE, 'w') as z:
        for foldername, _, filenames in os.walk(SOURCE_DIR):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, SOURCE_DIR)
                z.write(filepath, arcname)
    print(f'Created deployment package: {ZIP_FILE}')

def deploy_lambda():
    client = boto3.client('lambda')
    with open(ZIP_FILE, 'rb') as f:
        zipped_code = f.read()
    response = client.update_function_code(
        FunctionName=LAMBDA_FUNCTION_NAME,
        ZipFile=zipped_code
    )
    print('Deployment response:', response)

if __name__ == '__main__':
    zip_source_code()
    deploy_lambda()
