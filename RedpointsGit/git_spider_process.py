"""This is the entry point for the git crawler, main function gets executed to start the process"""
__license__ = "None"
__author__ = "Tugberk Arkose"
__docformat__ = 'reStructuredText'

from scrapy.crawler import Crawler, CrawlerProcess
from spiders.git_spider import GitSpider
from scrapy.utils.project import get_project_settings
from scrapy import signals
import argparse
import json
import random
import logging


def get_args():
    """ returns: input_json_data, output_json_file_path
        rtype: tuple

        ...note: output_json_file_path is not required input, default value None"""
    parser = argparse.ArgumentParser(
        description="Git Crawler")
    parser.add_argument('-i',
                        required=True,
                        help="Input Json file path")
    parser.add_argument('-o',
                        required=False,
                        help="Output Json file path")
    args = parser.parse_args()

    input_json_file_path = args.i
    input_json_file = open(input_json_file_path)
    input_json_str = input_json_file.read()
    input_json_data = json.loads(input_json_str)
    input_json_file.close()

    output_json_file_path = args.o
    return input_json_data, output_json_file_path


def parse_input_params(input_json_data):
    """ returns: keywords, proxies, search_type
        rtype: tuple

        :param input_json_data: json string"""
    keywords = input_json_data['keywords']
    proxies = input_json_data['proxies']
    search_type = input_json_data['type']
    return keywords, proxies, search_type


def write_result_to_json(result, output_json_file="result.json"):
    """
    :param result: json string output of the crawler
    :param output_json_file: optional output file path
    """
    with open(output_json_file, 'w') as f:
        json.dump(result, f, indent=4)


def run_crawler(keywords, proxies, search_type):
    """
    :param keywords: a list of keywords to be used as search terms (unicode characters supported)
    :param proxies: one of them selected and used randomly to perform all the HTTP requests
        (you can get a free list of proxies to work with at https://free-proxy-list.net/)
    :param search_type:  the type of object we are searching for (Repositories, Issues and Wikis supported)
    """
    result = []

    def collect_items(item, response, spider):
        result.append(item)

    crawler = Crawler(GitSpider)
    crawler.signals.connect(collect_items, signals.item_scraped)

    process = CrawlerProcess(get_project_settings())

    process.crawl(crawler,
                  query=' '.join(keywords),
                  proxy=random.choice(proxies),
                  search_type=search_type)
    process.start()
    return result


def verify_search_type(search_type):
    search_type = str.lower(search_type)
    if search_type != "repositories" and search_type != "issues" and search_type != "wikis":
        raise Exception("Unsupported search type: {}".format(search_type))


def main():
    """
    Entry point for the program
    """
    print("Git scrapper running...")
    input_json_data, output_json_file_path = get_args()
    keywords, proxies, search_type = parse_input_params(input_json_data)

    verify_search_type(search_type)
    result = run_crawler(keywords, proxies, search_type)

    write_result_to_json(result, output_json_file_path)
    print("Scrapping finished!")


if __name__ == '__main__':
    main()

