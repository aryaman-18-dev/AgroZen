import requests
import os

BASE_URL = "http://localhost:5000/api/v1/files"

def test_file_upload():
    print("🚀 Testing File Upload Service...")
    
    # 1. Create a dummy file
    test_file_path = "test_image.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test file for AgroZen upload service.")
    
    try:
        # 2. Upload the file
        print("Step 1: Uploading file...")
        with open(test_file_path, "rb") as f:
            files = {'file': (test_file_path, f, 'text/plain')}
            data = {'user_id': 1}
            response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
        
        if response.status_code == 201:
            res_data = response.json()
            file_id = res_data['file']['id']
            download_url = res_data['download_url']
            print(f"✅ File uploaded successfully! ID: {file_id}")
            print(f"🔗 Download URL: {download_url}")
            
            # 3. Fetch file info
            print(f"Step 2: Fetching info for file {file_id}...")
            response = requests.get(f"{BASE_URL}/{file_id}")
            if response.status_code == 200:
                print(f"✅ File info retrieved: {response.json()['file']['original_name']}")
            
            # 4. List user files
            print("Step 3: Listing files for user 1...")
            response = requests.get(f"{BASE_URL}/user/1")
            if response.status_code == 200:
                print(f"✅ Found {len(response.json()['files'])} files for user 1")
                
        else:
            print(f"❌ Upload failed: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == "__main__":
    test_file_upload()
