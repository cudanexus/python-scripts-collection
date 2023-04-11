import requests
import json
import time
import telegram
from datetime import datetime

#add your telegram token starting with ":" 5990****:AADDSSAD
token=''

# Add Chat Id below starting with "-"

bot = telegram.Bot(token=token)




# bot.send_message(chat_id='-806401409', text=code, parse_mode=telegram.ParseMode.HTML)


url = "https://replit.com/graphql"
headers = {
    "Host": "replit.com",
    "Connection": "close",
    "Content-Length": "1024",
    "accept": "*/*",
    "x-requested-with": "XMLHttpRequest",
    "x-client-version": "00ea8a5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "content-type": "application/json",
    "Origin": "https://replit.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://replit.com/bounties?order=creationDateDescending",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
import pytz

payload = "[{\"operationName\":\"BountiesPageSearch\",\"variables\":{\"input\":{\"count\":4,\"searchQuery\":\"\",\"statuses\":[\"open\",\"inProgress\",\"completed\",\"canceled\"],\"order\":\"creationDateDescending\",\"listingState\":\"listed\"}},\"query\":\"query BountiesPageSearch($input: BountySearchInput!) {\\n  bountySearch(input: $input) {\\n    __typename\\n    ... on BountySearchConnection {\\n      items {\\n        ...BountyCard\\n        __typename\\n      }\\n      pageInfo {\\n        hasNextPage\\n        nextCursor\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on UserError {\\n      message\\n      __typename\\n    }\\n    ... on UnauthorizedError {\\n      message\\n      __typename\\n    }\\n  }\\n}\\n\\nfragment BountyCard on Bounty {\\n  id\\n  title\\n  descriptionPreview\\n  cycles\\n  deadline\\n  status\\n  slug\\n  solverPayout\\n  timeCreated\\n  applicationCount\\n  isUnlisted\\n  solver {\\n    id\\n    username\\n    image\\n    url\\n    __typename\\n  }\\n  user {\\n    id\\n    username\\n    image\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\n\"}]"

response_old = None

while True:
    response = requests.post(url, headers=headers, data=payload, verify=False)
    response_dict = json.loads(response.text)
    # Load old response from file
    with open('response.json', 'r') as f:
        old_response_dict = json.load(f)

    code = '''

'''

    # Check if old and new responses are different
    if response_dict != old_response_dict:
        # Print the differences
        print('New items found:')
        for item in response_dict[0]['data']['bountySearch']['items']:
            if item not in old_response_dict[0]['data']['bountySearch']['items']:
                # print(item)
                bounty_price = item['solverPayout']/100
                print(bounty_price)
                bounty_price=str(bounty_price)+"$"
                print(type(bounty_price))
                #convert bounty_deadline to current date - bounty_deadline
                bounty_deadline = item['deadline']
                from datetime import datetime, timezone

                # Convert the deadline string to a datetime object
                deadline_str = str(bounty_deadline)
                deadline_dt_naive = datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M:%S.%fZ")

                # Add timezone information to deadline_dt
                deadline_dt = deadline_dt_naive.replace(tzinfo=timezone.utc)

                # Get the current date and time in UTC
                current_dt = datetime.now(timezone.utc)

                # Calculate the difference between the current date and the deadline
                time_diff = str(deadline_dt - current_dt)

                # Print the time difference
                print(f"Time remaining until the deadline: {time_diff}")



                code="**New Bounty Found: **"+item['title']+"\n\n"+"Bounty Description: "+item['descriptionPreview']+"\n\n"+"Bounty Slug: "+item['slug']+"\n\n"+"Bounty Status: "+item['status']+"\n\n"+"Bounty Deadline: "+time_diff+"\n\n"+"Bounty Solver Payout: "+bounty_price+"\n\n\n"
                print(code)
                bot.send_message(chat_id='', text=code, parse_mode=telegram.ParseMode.HTML)
                print('\n')

        # Save current response as old response
        with open('response.json', 'w') as f:
            json.dump(response_dict, f, indent=4)

    

        


# bounty_items = response_dict[0]['data']['bountySearch']['items']
    time.sleep(6)  # Wait for 60 seconds before making the next API call
    print('API call made waiting for 60 seconds before making the next API call\n\n')
