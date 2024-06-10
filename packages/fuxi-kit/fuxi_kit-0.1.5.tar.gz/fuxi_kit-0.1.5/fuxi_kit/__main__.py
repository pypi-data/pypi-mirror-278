# -*- coding: utf-8 -*
import asyncio
import logging
import os
import sys

import yaml
from aiohttp import ClientSession
from yarl import URL


class FuxiKit(object):
    def __init__(self, config_file=None):
        self.config_file = config_file if config_file is not None else "config.yaml"
        self.config = self.load_config()
        self.session = None
        self.loop = asyncio.get_event_loop()
        self.logger = self.setup_logger()

        try:
            self.username = os.environ["username"]
            self.password = os.environ["password"]
        except KeyError:
            self.logger.error(
                "Environment variables `username` and `password` must be set"
            )
            sys.exit(1)

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel((self.config["log"]["level"]).upper())
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - FUXI::AUTH - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_config(self):
        try:
            with open(self.config_file) as file:
                self.config = yaml.safe_load(file)
            return self.config
        except IOError:
            print("Could not open config file: {}".format(self.config_file))
            sys.exit(1)
        except yaml.scanner.ScannerError as err:
            print("Config file({}) failed to load: {}".format(self.config_file, err))
            sys.exit(1)

    async def pass_verify(self):
        if not self.session:
            self.session = ClientSession()
        params = {"api-key": self.config["fuxi_web"]["auth_api_key"]}
        url = URL(
            "{}{}".format(
                self.config["fuxi_web"]["endpoint"], self.config["fuxi_web"]["auth_api"]
            )
        ).with_query(params)
        json_data = {"username": self.username, "password": self.password}
        headers = {"Content-Type": "application/json", "User-Agent": '"FuxiKit/v1"'}
        async with self.session.post(url, json=json_data, headers=headers) as response:
            self.logger.info(f"POST {url} - Status: {response.status}")
            if response.status == 200:
                self.logger.error(f"Authentication passed - {response.status}")
                sys.exit(0)
            else:
                self.logger.error(f"Authentication failed - {response.status}")
                sys.exit(1)

    def async_run(self):
        self.loop.run_until_complete(self.pass_verify())
        self.loop.close()


if __name__ == "__main__":
    FuxiKit().async_run()
