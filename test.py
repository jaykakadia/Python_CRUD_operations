import requests
import concurrent.futures
import time
import string
import random

BASE_URL = "http://127.0.0.1:5001"
TOTAL_REQUESTS = 10000
CONCURRENCY = 100 # Set back to 100 to prevent OS thread crashing!

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run_load_test():
    username = generate_random_string()
    password = "password123"

    print(f"[*] Registering temporary test user: {username}")
    try:
        res = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password, "role": "user"})
        if res.status_code != 201:
            print("Failed to register. Is the app running?")
            print(res.json())
            return
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server. Is it running on port 5001?")
        return

    print("[*] Logging in to get token...")
    res = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    token = res.json().get("access_token")
    
    if not token:
        print("Failed to get token!")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("[*] Creating a dummy note so the database isn't empty...")
    dummy_note = {
        "title": "Speed Test Note",
        "content": "This is a note created during the load test!"
    }
    requests.post(f"{BASE_URL}/notes", json=dummy_note, headers=headers)

    success_count = 0
    fail_count = 0

    print(f"\n[*] Starting {TOTAL_REQUESTS} requests...")
    print(f"[*] Firing {CONCURRENCY} concurrent threads to hit GET /allNotes")
    print("[*] Please wait...\n")

    print("[*] Sample Response from server (1 request):")
    try:
        sample_r = requests.get(f"{BASE_URL}/allNotes", headers=headers)
        import json
        print(json.dumps(sample_r.json(), indent=2))
        print("-" * 40 + "\n")
    except Exception as e:
        print("Failed to get sample response:", e)

    def make_request():
        try:
            # We are sending a GET request here. 
            r = requests.get(f"{BASE_URL}/allNotes", headers=headers)
            if r.status_code == 200:
                print(r.json()) # Printing every single request!
                return True
            else:
                return False
        except Exception:
            return False

    start_time = time.time()

    # Using ThreadPoolExecutor to send requests in parallel so it doesn't take forever!
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(make_request) for _ in range(TOTAL_REQUESTS)]
        
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success_count += 1
            else:
                fail_count += 1

            # Print an update every 1000 requests
            total_done = success_count + fail_count
            if total_done % 1000 == 0:
                print(f" -> Completed {total_done} / {TOTAL_REQUESTS} requests...")

    duration = time.time() - start_time
    
    print("\n" + "="*30)
    print("      TEST COMPLETE")
    print("="*30)
    print(f"Total Requests  : {TOTAL_REQUESTS}")
    print(f"Successful      : {success_count} \u2705")
    print(f"Failed          : {fail_count} \u274c")
    print(f"Time Taken      : {duration:.2f} seconds")
    print(f"Speed           : {(TOTAL_REQUESTS/duration):.2f} req/sec")

def put_function_test():
    BASE_URL = "http://127.0.0.1:5001"
    TOTAL_REQUESTS = 2
    CONCURRENCY = 1 # Set back to 100 to prevent OS thread crashing!
    success_count = 0 
    Fail_count = 0

    def make_request():
        try:
            r = requests.put(f"{BASE_URL}/notes/1", json={"title": "Updated Note", "content": "Updated Content"}, headers=headers)
            if r.status_code == 200:
                print(r.json()) # Printing every single request!
                return True
            else:
                return False
        except Exception:
            return False

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(make_request) for _ in range(TOTAL_REQUESTS)]
        
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success_count += 1
            else:
                Fail_count += 1

            total_done = success_count + Fail_count
            if total_done % 1000 == 0:
                print(f" -> Completed {total_done} / {TOTAL_REQUESTS} requests...")

    duration = time.time() - start_time
    
    print("\n" + "="*30)
    print("      TEST COMPLETE")
    print("="*30)
    print(f"Total Requests  : {TOTAL_REQUESTS}")
    print(f"Successful      : {success_count} \u2705")
    print(f"Failed          : {Fail_count} \u274c")
    print(f"Time Taken      : {duration:.2f} seconds")
    print(f"Speed           : {(TOTAL_REQUESTS/duration):.2f} req/sec")
    
    


if __name__ == "__main__":
    run_load_test()
    # put_function_test()
