from googleapiclient.discovery import build
from credentials import cse_api_key, cse_id


def kword_search(query, startnum):
    service = build("customsearch", "v1", developerKey=cse_api_key)
    res = service.cse().list(q=query, cx=cse_id, start=startnum).execute()
    return res


if __name__ == "__main__":
    query = "charlotte rookie lamello ball OR youngest player OR nba history OR record"
    kword_search(query, 1)
