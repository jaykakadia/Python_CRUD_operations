import requests
import concurrent.futures
import time
import random

BASE_URL = "http://127.0.0.1:5001"
TOTAL_REQUESTS = 2000
CONCURRENCY = 50

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NjE2ODg2OSwianRpIjoiYTkxMzJkNWItNmI2MC00MTk2LWFmN2UtZDA0MzNhZjkxMDRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwicm9sZVwiOiBcImFkbWluXCJ9IiwibmJmIjoxNzc2MTY4ODY5LCJjc3JmIjoiMWZkMGE0NDEtODA5Ni00Njc4LWIzMWQtODQ0NzI3NGNhM2M3IiwiZXhwIjoxNzc2MTc2MDY5fQ.bd6jRyZHHNZq4nfLB0H9BUpAgeKPs5YRisdacsrmX_Q"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# -------- PUT (full update) --------
def put_request():
    try:
        note_id = random.randint(1, 100)  # avoid same row lock

        r = requests.put(
            f"{BASE_URL}/notes/{note_id}",
            json={
                "title": f"Updated Title {note_id}",
                "content": "Updated Content"
            },
            headers=headers
        )
        return r.status_code == 200
    except:
        return False


# -------- PATCH (partial update) --------
def patch_request():
    try:
        note_id = random.randint(1, 100)

        r = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={
                "title": f"Patched {note_id}"
            },
            headers=headers
        )
        return r.status_code == 200
    except:
        return False


def run_test(mode="PUT"):
    success = 0
    fail = 0

    start = time.time()

    func = put_request if mode == "PUT" else patch_request

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(func) for _ in range(TOTAL_REQUESTS)]

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            if future.result():
                success += 1
            else:
                fail += 1

            if (i + 1) % 500 == 0:
                print(f"Completed {i+1}/{TOTAL_REQUESTS}")

    end = time.time()

    print("\n===== RESULT =====")
    print("Mode:", mode)
    print("Time:", round(end - start, 2), "s")
    print("Success:", success)
    print("Fail:", fail)
    print("Speed:", round(TOTAL_REQUESTS / (end - start), 2), "req/sec")


if __name__ == "__main__":
    # change mode to "PATCH" if needed
    run_test(mode="PUT")