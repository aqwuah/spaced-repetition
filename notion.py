import requests, datetime, time, random

NOTION_TOKEN = ""
RESULT_SIZE = 10
NOTION_VERSION = "2022-06-28"

def send_request(ID, start_cursor=None, type="notes"):
    # Send API request
    url = f"https://api.notion.com/v1/databases/{ID}/query"
    payload = {"page_size": RESULT_SIZE}
    if start_cursor:
        payload["start_cursor"] = start_cursor
    if type == "notes":
        payload["sorts"] = [{"property": "Created", "direction": "ascending"}]
    elif type == "hw/tests":
        payload["filter"] = {"property": "Completed", "checkbox": {"equals": False}}
    r = requests.post(url, json=payload, headers={"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": NOTION_VERSION})
    
    # Raise exception if bad HTTP response
    r.raise_for_status()
    response = r.json()

    return response

def get_subject_results(ID):
    # Initiate list, send API request and append to list
    results = []
    response = send_request(ID,)
    results.append(response)

    # Repeat API call if there are more results
    while response["has_more"]:
        time.sleep(1)
        response = send_request(ID, start_cursor=response["next_cursor"])
        results.append(response)

    return results

def count_pages(results):
    page_count = 0

    # Iterate through pages and increment variable
    for j in range(len(results)):
        for page in results[j]["results"]:
            page_count += 1

    return page_count

def random_page(page_count, results):
    # Random page
    item_index = random.randint(0, page_count - 1)

    # Calculate which sublist the item is found in, and what index it is in that list
    sublist_index = (item_index) // RESULT_SIZE
    sublist_item_index = (item_index) % RESULT_SIZE

    return sublist_index, sublist_item_index

def format_date(old_date):
    # Convert input string to datetime object
    dt_obj = datetime.datetime.fromisoformat(old_date[:-1])

    # Convert datetime object to nicer string
    new_date = dt_obj.strftime("%d %B %Y")

    return new_date

def homework_and_tests():

    amounts = []

    for i in range(2):
        if i == 0:
            id = "4d46e7cb9b904adaa236ffd1412cfcec" 
        else:
            id = "647d8cb30d6440fe9465d9494170b2be"
    
        # Get homework / test database
        response = send_request(id, type="hw/tests")

        # Count items in database
        i = 0
        for x in response["results"]:
            i += 1
        
        amounts.append(i)

    return amounts
    
