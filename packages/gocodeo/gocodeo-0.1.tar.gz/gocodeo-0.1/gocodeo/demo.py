import os
import sys
import re
import threading
import time
from pymongo import MongoClient
import certifi
import platform
ca = certifi.where()

from vertexai.language_models import CodeGenerationModel
from google.oauth2 import service_account
import vertexai
import json
import requests
import subprocess

connection_url = "mongodb+srv://mohantysoumendraprasad15:roman2003@cli.e4umg8e.mongodb.net/"

# Initialize MongoDB client
client = MongoClient(connection_url, tlsCAFile=ca)

# Access the CLI database
db = client["CLI"]

collection = db['Demo_final']



credentials_data={
  "type": "service_account",
  "project_id": "symbolic-bit-398912",
  "private_key_id": "6cc13a1aa736855f25148aa6daa2f99374307180",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClM+Eub91x2IhM\nMw5sID2+JwvHI9cRtE5BpIq13BXlN87z8gnKDUIfRQslGpg2pIk+IvizweKy8lmq\nOrA7XPLVFQl3JEvzq9xKbMAaLoOUS6rOf9ik157TPDw+m3JnL4VwNrjhplqWbU+X\nmCXc1hxdX2cm5SM2VZUE5vgco32/IKKvv511E6JUQSeFzB95/4XKkPO2xADcmams\n+6ngxJMRkuF6u1DZyWFkpCzYB/gCaX+HnHEiPm3doYOdb+i3fXuVBZ5y0V2zEcpz\nZeDpbZO7hmWQxPOnjCLWHbqIeCJreDbDdHMelkyv67g1Q9NRwTCLb8RfmeGzMvTo\nv9KJkr0pAgMBAAECggEAARo3hnfN99SEvv1tkIsmiP5PCyUnakF/GYZfkUHGuPYx\nC1pcy7G1nz/MCJNaMK3TEfcUcclOxKLutj7DWPdl0huHKfm0CAw9jBbtsT8I4b8f\nhKvrENk01h6wyDor/pmdP60dzrkCzGjY/x9PdrR3EVMcUnDKVgfRgWwz0P0bpGAw\nnrl6OkOMlQX2Psk0ekWI/WS5Tvt4G3P5VJNeoOdtRQEKvR+qaR3CIJyGafX0RrE8\n0PT2bYUeRP3A2+p1Si7Y6j3E/Kor+mwOjzro2Yl5eANwZMc3sYRxB3hKKAv5StNB\njU804hfJkfMGn46yy1altAUG9s9bq4P+qllgko7+AQKBgQDhrtm/JUAoUh7ew3c6\n89L5rtqZIdZkDoyTFEqQEhu1pN+RILL5J5TLtACmCzBFnW0VNfh0B5bDCuRlstoU\nNK5bdeeQmmeZmP617XB4rakKw0yrOMdu77+RMaGPegVr/bs5xgQjPg5iOrxIEL0r\nduaWYVp5wjW+YksFzmGEu1NIlQKBgQC7ZSIwahplYWzb1WKXj+wy+rWNfEce/yyh\nM5lfHEknUZdd6cu8s6rhkjVEkIeO5OFiylr7pqDEH/5gD6r6YSr4db25sFH5m51u\nsl3yHk9Dam0AdeBdQ21rc1Khfl8ycuFzSwsgSYEWtZ3uoWkud6spxiS3Mqp9uz+i\nBgz75Fs5RQKBgBvSITemEO2nifSuJfGXgyeSfZIpELPO81diRfrSsKXIyGKspEOA\ntKAT9YyCjpXWXU8jExjCorwyiItc6/NXtzLBKyWxUxolOSkWNyo5RkB0aOwmmLc9\nSOFOO/ti8G4qnjz2AyaRDNbhJLrBjYBhLPXW1H90CIoKtfLmSTFConatAoGBAIfH\nDk+gAUIlphdedBI28MA7UWKTgoCeCTs/xMfaGdMIVjFwnfM7Bvxr0Ha+dcn+YqQO\n1H9zyxZvzALUN2E1GEpwHSi27Z56t0YmrNUqSuog6ZukzQ0mNtjc9SkYBGfsPxgn\nbodVWtgWfbkScMB/aqBY9e9bIZb6HnAKDExSuBo1AoGAJnAsYFHyeDs8ZFaVGhPO\nGeYXTMj9JGwZHR+wqFfuiBIqs/cra3xETIDyr6cGT9xTjQ0nVazvROBANgkU+YIO\nWxzzc77PnpfP20yMMTNsJFoZhSQUns8LY9hxzKSnPYURqf32HTTImmmCbz2RJAyO\nOvPWkmJDkDvalolS6HNnEPE=\n-----END PRIVATE KEY-----\n",
  "client_email": "vertex-ai-service-account@symbolic-bit-398912.iam.gserviceaccount.com",
  "client_id": "114836232517254252283",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vertex-ai-service-account%40symbolic-bit-398912.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
credentials = service_account.Credentials.from_service_account_info(credentials_data)

vertexai.init(
    project="symbolic-bit-398912",
    location="us-central1",
    credentials=credentials
)


# GoCodeo_URL = "http://127.0.0.1:5000/api/v1/explain_api"


GoCodeo_URL = "https://staging-ai-service.gocodeo.com/api/v1/explain_api"

CHAT_API_URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    'Content-Type': 'application/json'
}


def explain_api_request(code):
   
    prompt =f"You are angularjs unit testing expert. Your job is to first understand the given code {code} then explain the code so that every team member should understand the logic and working of the function"
    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.6
    }


    response = requests.post(GoCodeo_URL, json=payload, headers=HEADERS)


    if response.status_code != 200:
        raise Exception(response.text)
  
    choices = response.json()

    if len(choices) == 0:
        raise Exception("Prompt did not return any answer")   
    message = choices[0].get("message", {}).get("content", "")
    # print(message, "message")
 
    return message

def open_api_request(code, type, number, context):
   
    prompt = f"You are angularjs unit testing expert. Your job is to write {number} numbers of {type} type sceanrios for the given code {code} using the explaination of its working here {context}. Your job is to achieve maximum code coverage .Generate scenarios from the given {context} only. It is mandatory that each  numbers of {type} type scenarios genereated by you should be different from each other , means not alike / same type. Try to cover all the possible different corner cases in these scenarios."
    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8
    }

    response = requests.post(GoCodeo_URL, json=payload, headers=HEADERS)
    
    if response.status_code != 200:
        raise Exception(response.text)
  
    choices = response.json()

    if len(choices) == 0:
        raise Exception("Prompt did not return any answer")   
    message = choices[0].get("message", {}).get("content", "")
    # print(message, "message")
 
    return message
def generate_api_request(code, context, type, number,import_lines,src_path,test_path):

   
    prompt = f"""You are angularjs unit testing expert. Your job is to write {number} numbers high quality unit test code  using jasmine and karma framework only, for given angular code: {code} for the given {type} scenarios in the context: {context}.
      Strictly go through the context and generate at least {number} numbers high quality unit test code with description including assertions 
      covering all scenarios in one file. Please mock all the services and data where ever necessary. 
      You have to  make sure to import all the necessary dependencies at the top for execution of tests . For your reference the imports are {import_lines} 
      in the source code file present at {src_path} location. 
      It is mandatory that the imported elements generated by you should be valid,precise & accurate as they will be directly used in production. Try to generate more accurate & executable unit test cases."""
    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8
    }

    response = requests.post(GoCodeo_URL, json=payload, headers=HEADERS)
   
    if response.status_code != 200:
        raise Exception(response.text)
  
    choices = response.json()

    if len(choices) == 0:
        raise Exception("Prompt did not return any answer")   
    message = choices[0].get("message", {}).get("content", "")

 
    return message     




def generate_api_request1(code, response, type, number):
    prompt = f"You are angularjs unit testing expert.Here is the current generated unit test cases:{response}, for input code:{code} . Your task is to improve code of all these current unit test cases on {type} type scenarios. If the  unit test cases you are getting that are  partially implemented ,then you have to fully implement it  accurately using jasmine and karma framework .It is mandatory that every unit test cases should be implemented completely."
    # print(prompt)
    try:
        prompt1 = prompt
        parameters = {
    "max_output_tokens": 8100,
    "temperature": 0.8
}
        model = CodeGenerationModel.from_pretrained("code-bison-32k")
        response = model.predict(
            prefix=prompt1,
            **parameters
        )
        return response.text

    except Exception as e:
        # Handle exceptions and return None
        print(f"Exception: {e}")
        return None
 
def extract_filename(file_path):
    # Convert the file path to raw string format
    file_path = rf"{file_path}"

    # Extract the filename from the file path
    filename = os.path.basename(file_path)

    # Remove the file extension if present
    filename_without_extension = os.path.splitext(filename)[0]

    

    return filename_without_extension    


# Animation function
def animate_training(duration):
    sys.stdout.write("Generating")
    sys.stdout.flush()
    start_time = time.time()
    while time.time() - start_time < duration:
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write("\b" * 3)
        sys.stdout.flush()
        time.sleep(0.5)

def extract_imports_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            typescript_code = file.read()
            
            # Regular expression pattern to match import statements
            import_pattern = r'import\s+{[^}]+}\s+from\s+[\'"].+?[\'"];'

            # Find all import statements using regex
            import_lines = re.findall(import_pattern, typescript_code)

            if not import_lines:
                return ""  # Return empty string if no import lines found

            # Concatenate import lines into a single string with newline characters
            import_string = '\n'.join(import_lines)
            
            return import_string
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error: {e}"
 
def extract_user_defined_imports(typescript_code):
    if not typescript_code.strip():
        return ''  # Return empty string if no imports found

    # Regular expression pattern to match import blocks
    import_pattern = r'(import\s+{[^}]+}\s+from\s+[\'"][^\'"]+[\'"];)+'

    # Find all import blocks using regex
    import_blocks = re.findall(import_pattern, typescript_code)

    user_defined_imports = []

    # Iterate through import blocks
    for import_block in import_blocks:
        # Regular expression pattern to match individual import statements within the block
        import_statement_pattern = r'import\s+{([^}]+)}\s+from\s+[\'"]([^\'"]+)[\'"];'

        # Find all import statements within the block
        import_statements = re.findall(import_statement_pattern, import_block)

        # Iterate through import statements within the block
        for import_statement in import_statements:
            import_symbols, import_path = import_statement

            # Check if the import path is a relative path (starts with './' or '../')
            if import_path.startswith('./'):
                # Replace './' with '../'
                import_path = '../' + import_path[2:]
            elif import_path.startswith('../'):
                # Add an extra '../' to the import path
                import_path = '../' + import_path

            # Construct the new import statement
            new_import_statement = f"import {{ {import_symbols} }} from '{import_path}';"

            # Append the new import statement to the list
            user_defined_imports.append(new_import_statement)

    # Join the user-defined imports into a single string
    user_defined_imports_string = '\n'.join(user_defined_imports)

    return user_defined_imports_string

def replace_string_imports(original_code, updated_imports):
    if not original_code.strip() or not updated_imports.strip():
        return original_code  # Return original code if no imports found

    try:
        # Regular expression pattern to match import statements
        import_pattern = r'import\s+{[^}]+}\s+from\s+[\'"][^\'"]+[\'"];\n*'

        # Find and remove existing imports
        existing_imports = re.findall(import_pattern, original_code)
        original_code = re.sub(import_pattern, '', original_code)

        # Prepend new imports before the remaining code
        updated_code = '\n'.join([import_line.strip() for import_line in updated_imports.split('\n')]) + '\n\n' + original_code.strip()

        return updated_code
    except Exception as e:
        return f"Error: {e}"
def generate_tests_for_directory(directory):
    cwd = os.getcwd()
    print("directory",directory)
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".ts") and not file_name.endswith(".spec.ts"):
                file_path = os.path.join(root, file_name)
                system_name = platform.system()
                print(file_path)
                if system_name == "Windows":
                    file_path = file_path.replace("/", "\\")
                    print("windows",file_path)
                else:
                    file_path = file_path.replace("\\", "/")
                file_path = os.path.relpath(file_path, cwd)
                print("relative path",file_path)

                try:
                    generate_tests(file_path)
                    
                   
                    # Wait for a short while before processing the next file
                    time.sleep(1)
                    print()
                except Exception as e:
                    print(f"An error occurred: {e}")
    # try:
    #     subprocess.run(['npm', 'run', 'test-lib'], check=True, shell=True)
    #     print("npm run test-lib command executed successfully")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error executing npm run test-lib command: {e}")
def start_animation(duration):
    animate_training(duration)
    print()  # Add a newline after animation
    sys.exit()
# Generate tests function
def generate_tests(file_name):
    global db_data
    db_data = None
    global flag
    flag=False
    
    file_path_from_app2 =None

    behaviour_type = ["HappyPath", "EdgeCase", "NegativeCase"]
    cwd = os.getcwd()
    cwd = cwd + "\\"
    system_name = platform.system()
    file_path_from_app = cwd + file_name

    temp = file_path_from_app.replace("/", "\\")

    if system_name == "Windows":
        file_path_from_app = file_path_from_app.replace("/", "\\")
    else:
        file_path_from_app = file_path_from_app.replace("\\", "/")

    # Extract the path from app to .ts using regex
    match = re.search(r'\\.*?lib(.*?\.ts)', temp)

    if match:

        file_path_from_app2 = match.group(1)
        file_path_from_app2 = 'lib' + file_path_from_app2
        
    # else :
    #     pass
    
    # Fetch data from the database   
    for doc in collection.find():
        if file_path_from_app2 in doc:
            db_data = doc
            flag=True
            break

    if flag==True:
        if db_data:
            for scenario_type in behaviour_type:
               
                # Fetch the file content of respective scenario from db
                if isinstance(db_data[file_path_from_app2], dict):
                    file_content = db_data[file_path_from_app2].get(scenario_type, '')
                else:
                    file_content = db_data.get(scenario_type, '')

                print(f"Generating tests on '{scenario_type}' scenarios for file: {file_path_from_app}")
                time.sleep(10)

                filename = rf"{file_path_from_app}"
                filename = os.path.basename(file_path_from_app)

                # Remove the file extension if present
                File_name = os.path.splitext(filename)[0]

                # Write the file content to the test file
                directory_path = os.path.dirname(file_path_from_app)
                test_folder_path = os.path.join(directory_path, 'gocodeo_tests')
                os.makedirs(test_folder_path, exist_ok=True)
                output_file_path = os.path.join(test_folder_path, f'test_{File_name}_{scenario_type}.spec.ts')

                with open(output_file_path, 'w') as output_file:
                    output_file.write(file_content)
                    print(f"Test cases on '{scenario_type}' scenarios written to file: {output_file_path}")
                time.sleep(6)
        else:
            print("Error!")
    else:
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                file_content = file.read()
            explain_response = explain_api_request(file_content)
            
            File_name = extract_filename(file_name)
            import_lines = extract_imports_from_file(file_name)

            behaviour_type = [{"type": "HappyPath", "number": 6}, {"type": "EdgeCase", "number": 12},
                              {"type": "NegativeCase", "number": 8}]
            for obj in behaviour_type:
                type = obj['type']

                print(f"Generating tests on '{type}' scenarios for file : {File_name} ")
                api_response = open_api_request(file_content, obj['type'], obj['number'], explain_response)

                directory_path = os.path.dirname(file_name)
                test_folder_path = os.path.join(directory_path, 'gocodeo_tests')
                output_file_path = os.path.join(test_folder_path, f'test_{File_name}_{type}.spec.ts')

                pattern1 = r'(?:\s*```(?:typescript|javascript|ts)?\n)?(.*?)(?:```|$)'
                pattern2 = r'```(?:typescript|javascript|ts)?\n(.*?)```|\b(?:typescript|javascript|ts)?\n(.*?)(?=$|```)'
                combined_pattern = f"{pattern1}|{pattern2}"

                test_response = generate_api_request(file_content, api_response, obj['type'], obj['number'],
                                                     import_lines, file_name, output_file_path)
                test_response1 = generate_api_request1(file_content, test_response, obj['type'], obj['number'])

                if test_response1:
                    os.makedirs(test_folder_path, exist_ok=True)
                    match = re.search(combined_pattern, test_response1, re.DOTALL)
                    if match:
                        content = match.group(1) or match.group(2) or match.group(3) or match.group(4)
                        content = content.strip()
                    else:
                        content = test_response1
                    new_imports = extract_user_defined_imports(content)
                    updated_code = replace_string_imports(content, new_imports)
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(updated_code)
                        print(f"Test cases on '{type}' scenarios written to file:{output_file_path}")
                else:
                    print(f"Failed to fetch test cases from API for File '{File_name}'.ts")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")

# Main function
def generate_tests_cli():
    # Prompt user for private key
    private_key = input("Enter your private key: ")
    if private_key != "gc_spgrXSnfZqYSVqqhQiVjlYApSQofFXIUtF":
        print("Invalid key.")
        return

    # Start animation for 30 seconds
    animation_thread = threading.Thread(target=start_animation, args=(8,))
    animation_thread.start()

    # Wait for animation thread to finish
    animation_thread.join()

    # Generate tests after animation
    if len(sys.argv) != 3:
        print("Usage: gocodeo-generate generate <file_name>")
        sys.exit(1)

    file_name = sys.argv[2]
    generate_tests(file_name)

def advanced():
    if len(sys.argv) != 3:
        print("Usage: gocodeo-advanced generate <file_name>")
        sys.exit(1)
    private_key = input("Enter your private key: ")
    if private_key != "gc_spgrXSnfZqYSVqqhQiVjlYApSQofFXIUtF":
        print("Invalid key.")
        return
    file_name = sys.argv[2]
    generate_tests_for_directory(file_name)
    

if __name__ == "__main__":
    generate_tests_cli()
    advanced()
    

