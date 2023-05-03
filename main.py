import datetime, time
import notion, emails

# Daily subject names
SUBJECTS = {
    "Monday": ["English", "Biology", "Sociology"],
    "Tuesday": ["Maths", "Chemistry", "Geography"],
    "Wednesday": ["Computer Science", "Physics", "Economics"],
    "Thursday": ["English", "Chemistry", "Geography"],
    "Friday": ["Maths", "Biology", "Sociology"],
    "Saturday": ["Computer Science", "Economics", "Physics"],
    "Sunday": ["English", "Maths", "Computer Science"],
}

# Daily subject database IDs
IDS = {
    "Monday": ["0df34a7e440c49f4b528e2c7c18ce905", "ecff5913a1a0451fb56bafa858de5b6b", "d2baccbac08f44159af1eed9829d51f1"],
    "Tuesday": ["42ad9899d2df47a2a49b82a85fc95efe", "0944dc54b2674405801288d0f87ca7d1", "b06a12c5f7a74df3932b7678e9970572"],
    "Wednesday": ["2519a8f5a3fd4b12bbeee24aca4119ad", "5d8736625e4a40c1997e9c7df4967d82", "9b31b98e4c0f409fb7d55e5bbc87cdd5"],
    "Thursday": ["0df34a7e440c49f4b528e2c7c18ce905", "0944dc54b2674405801288d0f87ca7d1", "b06a12c5f7a74df3932b7678e9970572"],
    "Friday": ["42ad9899d2df47a2a49b82a85fc95efe", "ecff5913a1a0451fb56bafa858de5b6b", "d2baccbac08f44159af1eed9829d51f1"],
    "Saturday": ["2519a8f5a3fd4b12bbeee24aca4119ad", "9b31b98e4c0f409fb7d55e5bbc87cdd5", "5d8736625e4a40c1997e9c7df4967d82"],
    "Sunday": ["0df34a7e440c49f4b528e2c7c18ce905", "42ad9899d2df47a2a49b82a85fc95efe", "2519a8f5a3fd4b12bbeee24aca4119ad"],
}

# Time to trigger code at
HOUR = 16
MINUTE = 0

def start():
    while True:
        # Get current time
        now = datetime.datetime.now()

        # Check if time matches TIME constant
        if now.hour == HOUR and now.minute == MINUTE:
            names, ids = daily_subjects()
            
            page_infos = []

            for id in ids:

                # Call function to get list of subject pages
                results = notion.get_subject_results(id)

                # Count amount of pages
                page_count = notion.count_pages(results)

                # Get a random page
                sublist_index, sublist_item_index = notion.random_page(page_count, results)

                # Retrieve the actual page
                sublist = results[sublist_index]
                i = 0
                for page in sublist["results"]:
                    if i == sublist_item_index:

                        # Get information about page and put in dictionary
                        page_info = {}
                        page_info["title"] = page["properties"]["Name"]["title"][0]["plain_text"]
                        page_info["url"] = page["url"]
                        page_info["created"] = notion.format_date(page["created_time"])
                        page_info["topic"] = page ["properties"]["Topic"]["select"]["name"]
                        page_info["term"] = page ["properties"]["Term"]["select"]["name"]

                        page_infos.append(page_info)

                        break

                    i += 1
                    

            hw_tests = notion.homework_and_tests()
            msg = emails.construct_email(page_infos, names, hw_tests)
            emails.send_email(msg)

        # Wait a minute to avoid constant checks      
        time.sleep(60)

def daily_subjects():
    # Get current day of the week
    today = datetime.datetime.today().strftime('%A')

    # Make lists of daily subjects and IDs
    subject_names = SUBJECTS[today]
    subject_ids = IDS[today]

    return subject_names, subject_ids

start()
