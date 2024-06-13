import os
import dotenv
import argparse

class Config:
    def __init__(self, 
                api_url: str = None,
                token: str = None,
                number_threads: int = 5,
                retry_delay_seconds: int = 5) -> None:

        # eviroment config
        self.api_url = api_url
        self.version = 1 # default 
        self.token = token
        self.number_threads = number_threads
        self.retry_delay_seconds = retry_delay_seconds
    
