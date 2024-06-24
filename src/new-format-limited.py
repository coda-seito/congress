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
                for node in json_data['childNodes']:
                    if 'nodeValue' in node:
                        value = node['nodeValue']
                        text = value['pdffile']
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

listr = ["https://www.govinfo.gov/wssearch/rb//cdoc/115/hdoc/[0-99]?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/115/hdoc/[100-199]?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/115/sdoc/all?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/115/tdoc/all?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/116/hdoc/[0-99]?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/116/hdoc/[100-199]?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/116/sdoc/all?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/116/tdoc/all?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/117/hdoc/[0-99]?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/117/hdoc/[100-199]?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/117/sdoc/all?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/117/tdoc/all?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/118/hdoc/[0-99]?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/118/hdoc/[100-199]?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/118/sdoc/all?fetchChildrenOnly=1",
"https://www.govinfo.gov/wssearch/rb//cdoc/118/tdoc/all?fetchChildrenOnly=1"]
for url1 in listr:
    print("|", end='')
    fetch_data(url=url1, file_name='absolute.txt')
