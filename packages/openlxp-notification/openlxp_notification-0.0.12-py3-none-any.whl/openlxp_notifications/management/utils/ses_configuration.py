import logging
import os

logger = logging.getLogger('dict_config_logger')

headers = {'Content-Type': 'application/json'}


"""
    Functions set up to extract environment values for
    AWS Simple Email Service (SES)

"""


def check_aws_access_key():
    """Extracts P1PS base endpoint"""
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')

    if aws_access_key:
        logger.info("AWS Access key is present and set")
    else:
        raise ValueError("Team Token value is absent and not set")

    return aws_access_key


def check_aws_secret():
    """Extracts P1PS base endpoint"""
    aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if aws_secret:
        logger.info("AWS Secret access Key  is present and set")
    else:
        raise ValueError("Team Token value is absent and not set")

    return aws_secret


def check_aws_region():
    """Extracts P1PS base endpoint"""
    aws_region = os.environ.get('AWS_DEFAULT_REGION')

    if aws_region:
        logger.info("AWS Default region is present and set")
    else:
        raise ValueError("Team Token value is absent and not set")

    return aws_region


def overall_health():
    """Check the variable required for SES are set"""
    check_aws_access_key()
    check_aws_secret()
    check_aws_region()
