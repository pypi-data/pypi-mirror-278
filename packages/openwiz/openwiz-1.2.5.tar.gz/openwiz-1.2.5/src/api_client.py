import openai
from src.logger import Logger

class APIClient:
    def __init__(self, api_key, logger: Logger):
        self.api_key = api_key
        self.logger = logger
        openai.api_key = self.api_key

    def generate_code(self, prompt):
        try:
            # message = openai.chat.completions.create(
            #     messages=[
            #         {
            #             "role": "user",
            #             "content": "Generate code for the following prompt and only return the code:\n\n" + prompt,
            #         }
            #     ],
            #     model="gpt-3.5-turbo",
            # )
            message = {
                "id": "cmpl-5hR1xyzxyzxyz",
                "object": "text_completion",
                "created": 1616620981,
                "model": "text-davinci-003",
                "choices": [
                    {
                        "text": 'import requests\nfrom bs4 import BeautifulSoup\n\ndef get_stock_info(stock_symbol):\n\turl = f"https://www.google.com/finance/quote/{stock_symbol}"\n\tresponse = requests.get(url)\n\tif response.status_code == 200:\n\t\tsoup = BeautifulSoup(response.content, \'html.parser\')\n\t\tprice = soup.find(class_="YMlKec fxKbKc").get_text()\n\t\tchange = soup.find(class_="YMlKec fxKbKc").next_sibling.get_text()\n\t\treturn f"Price: {price}, Change: {change}"\n\telse:\n\t\treturn "Failed to fetch data"\n\n# Example usage\nprint(get_stock_info("AAPL"))',
                        "index": 0,
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": 5,
                    "completion_tokens": 7,
                    "total_tokens": 12
                }
            }
            return message['choices'][0]['text']
        except Exception as e:
            print(f"\nERROR MESSAGE: {e}")
            return None