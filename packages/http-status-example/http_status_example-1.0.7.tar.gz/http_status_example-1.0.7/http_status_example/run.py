import requests
import sys
URL = r"https://choosealicense.com/"

def get_request(url:str=URL):
    """Prints HTTP status code of the URL provided or the default URL"""
    print(f"checking status for {url} ...")
    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    else:
        print(response.status_code)


def main(url:str):
    """Main entry point for the script"""    
    get_request(url)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        url = URL
    else:
        url = sys.argv[1]
    main(url)