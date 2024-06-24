import requests
import os
import time

def get_section(url):
    if 'hdoc' in url:
        return "house"
    elif 'sdoc' in url or 'tdoc' in url:
        return "senate"
    else :
        return ""
def fetch_data(url, file_name):
    try:
        time.sleep(0.5)
        path = f'./txt/{file_name}'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            if 'childNodes' in json_data:
                print(url)
                for node in json_data['childNodes']:
                    if 'nodeValue' in node:
                        value = node['nodeValue']
                        if 'text' in value:
                            text = value['text']
                            publishdate = value['publishdate']
                            section = get_section(url)
                            with open(path, 'a') as file:
                                file.write("\n" + publishdate + "," + section + "," +text)
                        if 'browsePathAlias' in value:
                            new_url = f"https://www.govinfo.gov/wssearch/rb//cdoc/{value['browsePathAlias']}?fetchChildrenOnly=1"
                            fetch_data(new_url, file_name)
        else:
            print("Error:", response.status_code)
    except Exception as e:
        print(e)

for year in range(115, 119):
    print("|", end='')
    url1 = f"https://www.govinfo.gov/wssearch/rb//cdoc/{year}?fetchChildrenOnly=1"
    fetch_data(url=url1, file_name='absolute.txt')
