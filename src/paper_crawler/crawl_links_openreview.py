import openreview
from dotenv import load_dotenv
import os
from tqdm import tqdm
from multiprocessing import Pool
import json

from .crawl_links_soup import process_link

def get_openreview_submissions(venueid: str) -> list[str]:
    # API V2
    print(os.environ["OPENREVIEW_USERNAME"])
    client = openreview.api.OpenReviewClient(
        baseurl='https://api2.openreview.net',
        username=os.environ["OPENREVIEW_USERNAME"],
        password=os.environ["OPENREVIEW_PASSWORD"]
    )

    submissions = client.get_all_notes(content={'venueid': venueid} )

    print(f"{venueid} has : {len(submissions)} submissions.")

    # assemble links
    links = ["https://openreview.net" + submission.content['pdf']['value'] for submission in submissions]

    return links   



if __name__ == '__main__':
    load_dotenv()

    venueid = 'ICLR.cc/2024/Conference'

    links = get_openreview_submissions(venueid)


    # loop through paper links find pdfs
    with Pool(2) as p:
        res = list(tqdm(p.imap(process_link, links), total=len(links)))

    with open(f"./storage/{"_".join(venueid.split("/"))}.json", 'w') as f:
        f.write(json.dumps(res, indent=1))
