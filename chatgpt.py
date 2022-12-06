from typing import Dict
import requests
import json
from uuid import uuid4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ChatGPT:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.urls = {
            'login': 'https://chat.openai.com/auth/login',
            'session': 'https://chat.openai.com/api/auth/session',
            'conversation': 'https://chat.openai.com/backend-api/conversation',
        }
        self.session = requests.session()
        self.access_token = None
        self.conversation_id = str(uuid4())
        self.parent_message_id = str(uuid4())
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'

    def login(self) -> Dict[str, str]:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent={}'.format(self.user_agent))
        driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        driver.get(self.urls['login'])
        element = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Log in')]"))
        )
        element.click()
        element = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
        )
        element.send_keys(self.username)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        element = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        element.send_keys(self.password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
        driver.close()
        return cookies

    def get_access_token(self) -> str:
        cookies = self.login()
        headers = {
            'User-Agent': self.user_agent,
        }
        response = self.session.get(self.urls['session'], cookies=cookies, headers=headers)
        data = json.loads(response.text)
        return data['accessToken']

    def get_response(self, request: str, attempts: int = 1) -> str:
        if self.access_token is None:
            self.access_token = self.get_access_token()
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'User-Agent': self.user_agent,
        }
        message_id = str(uuid4())
        data = {
            'action': 'next',
            'messages': [
                {
                    'id': message_id,
                    'role': 'user',
                    'content': {
                        'content_type': 'text',
                        'parts': [
                            str(request),
                        ],
                    },
                },
            ],
            'parent_message_id': self.parent_message_id,
            'model': 'text-davinci-002-render',
        }
        response = self.session.post(self.urls['conversation'], headers=headers, json=data)
        if response.ok:
            self.parent_message_id = message_id
            data = [chunk for chunk in response.text.split('\n') if chunk.strip()]
            data = data[-2].lstrip('data: ')
            data = json.loads(data)
            return data['message']['content']['parts'][0]
        elif attempts > 0:
            self.access_token = None
            return self.get_response(request, attempts - 1)
        return "Unknown error."
