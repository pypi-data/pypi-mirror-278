from nomad_media_pip.src.admin.asset_upload.upload_thread import _upload_thread

import time, threading

def _multi_thread_upload(self, AUTH_TOKEN, URL, FILE, RESPONSE, DEBUG):
    PARTS = RESPONSE["parts"]
    TOTAL_PARTS = len(PARTS)
    MAX_ACTIVE_WORKERS = 8
    MAX_WORKERS = min(TOTAL_PARTS, MAX_ACTIVE_WORKERS)
    MAX_RETRIES = 5

    idx = 0
    worker_count = { "value": 0 }
    threads = []
    while idx < TOTAL_PARTS:
        # Loop while available workers
        while (worker_count["value"] < MAX_WORKERS) and (idx < TOTAL_PARTS):
            for tries in range(MAX_RETRIES):
                try:
                    thread = threading.Thread(target=_upload_thread, args=(self, AUTH_TOKEN, URL, FILE, PARTS[idx], 
                                                                          worker_count, DEBUG))
                    threads.append(thread)
                    thread.start()

                    idx += 1
                    worker_count["value"] += 1

                    if idx >= TOTAL_PARTS:
                        break
                except Exception as e:
                    print(f"Error: {e}. Retrying...")
                else:
                    break

        while (worker_count["value"] == MAX_WORKERS):
            time.sleep(20)

    for thread in threads:
        thread.join()

    while True:
        if worker_count["value"] == 0:
            break
        time.sleep(20)
    