import logging
from argparse import ArgumentParser

from castor_extractor.warehouse import salesforce  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main():
    parser = ArgumentParser()

    parser.add_argument("-u", "--username", help="Salesforce username")
    parser.add_argument("-p", "--password", help="Salesforce password")
    parser.add_argument("-c", "--client-id", help="Salesforce client id")
    parser.add_argument(
        "-s", "--client-secret", help="Salesforce client secret"
    )
    parser.add_argument(
        "-t", "--security-token", help="Salesforce security token"
    )
    parser.add_argument("-b", "--base-url", help="Salesforce instance URL")
    parser.add_argument("-o", "--output", help="Directory to write to")

    parser.add_argument(
        "--skip-existing",
        dest="skip_existing",
        action="store_true",
        help="Skips files already extracted instead of replacing them",
    )
    parser.set_defaults(skip_existing=False)

    args = parser.parse_args()

    salesforce.extract_all(
        username=args.username,
        password=args.password,
        client_id=args.client_id,
        client_secret=args.client_secret,
        security_token=args.security_token,
        base_url=args.base_url,
        output_directory=args.output,
        skip_existing=args.skip_existing,
    )
