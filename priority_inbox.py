import requests
import heapq
from datetime import datetime

CATEGORY_SCORES = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

def load_notifications(endpoint_url, token=None):
    req_headers = {}
    if token:
        req_headers['Authorization'] = f'Bearer {token}'
        
    try:
        res = requests.get(endpoint_url, headers=req_headers, timeout=15)
        res.raise_for_status()
        payload = res.json()
        return payload.get("notifications", [])
    except requests.exceptions.RequestException as error:
        print(f"Failed to fetch data from API: {error}")
        return []

def extract_highest_priority(notifs_list, limit=10):
    p_queue = []

    for item in notifs_list:
        category = item.get("Type", "")
        score = CATEGORY_SCORES.get(category, 0)
        
        time_str = item.get("Timestamp", "")
        try:
            time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            time_obj = datetime.min
            
        entry = (score, time_obj, item.get("ID", ""), item)

        if len(p_queue) < limit:
            heapq.heappush(p_queue, entry)
        else:
            heapq.heappushpop(p_queue, entry)

    p_queue.sort(reverse=True)
    return [node[3] for node in p_queue]

if __name__ == "__main__":
    TARGET_URL = "http://4.224.186.213/evaluation-service/notifications"
    MY_TOKEN = "YOUR_AUTH_TOKEN_HERE" 
    
    print("Connecting to API...")
    fetched_data = load_notifications(TARGET_URL, MY_TOKEN)
    
    if not fetched_data:
        print("No new notifications to display.")
    else:
        print(f"Retrieved {len(fetched_data)} items. Filtering top 10...\n")
        
        top_notifications = extract_highest_priority(fetched_data, limit=10)
        
        print("=" * 60)
        print(" YOUR PRIORITY INBOX ")
        print("=" * 60)
        
        for index, msg in enumerate(top_notifications, start=1):
            msg_type = msg.get('Type', 'Unknown').upper()
            print(f"{index:2d}. [{msg_type}] {msg.get('Message', '')}")
            print(f"    Added: {msg.get('Timestamp', '')} | Ref: {msg.get('ID', '')}\n")
