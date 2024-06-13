import requests
from bs4 import BeautifulSoup

class LipsumAPI:
    def __init__(self) -> None:
        pass
    
    def generate(self, count: int, content_type: str, default_start: bool = True) -> str:
        # Validate type input
        if content_type not in ['words', 'paragraphs', 'bytes', 'lists']:
            raise ValueError("content_type must be 'words', 'paragraphs', 'bytes', or 'lists'")
        
        url = "https://www.lipsum.com/feed/html"
        if content_type == "paragraphs":
            wtype = 'paras'
        else:
            wtype = content_type
        
        data = {
            'amount': count,
            'what': wtype,
        }
        if default_start:

            data["start"] = "yes"
        try:
            # Send the request
            response = requests.post(url, data=data)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            
            soup = BeautifulSoup(response.text, 'lxml')

            # Extract text from <p> or <ul> tags
            if content_type == 'lists':
                text_list = [ul.get_text() for ul in soup.find_all('ul')]
            else:
                text_list = [p.get_text() for p in soup.find_all('p')]
            
            # Concatenate the text into a single string
            lorem_text = '\n'.join(text_list)
            
            # Remove extra whitespace and newlines if content_type is 'lists'

            lorem_text = lorem_text.replace("\n", "")
            
            return lorem_text
        
        except requests.RequestException as e:
            raise Exception(f"Error fetching data from Lipsum.com: {e}")


