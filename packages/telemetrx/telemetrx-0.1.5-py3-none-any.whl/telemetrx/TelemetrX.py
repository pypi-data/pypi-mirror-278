import asyncio
from typing import Literal
import aiohttp
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)


async def send_telemetrx_async(telemetrx_env: Literal["dev", "stage", "prod"] = "stage",
                               telemetrx_data: dict = None, app_token: str = None,
                               telemetrx_base_url: str = None):
    """Sends telemetry data asynchronously to the appropriate URL.

    Args:
        telemetrx_env: Environment (dev, stage, or prod).
        telemetrx_data: Dictionary of telemetry data.

    URL will be generated using BASE_URL_ENVIRONMENT eg: BASE_URL_DEV, BASE_URL_STAGE, BASE_URL_PROD
    :param telemetrx_base_url:
    :param telemetrx_data:
    :param telemetrx_env:
    :param app_token:
    """
    url = telemetrx_base_url+"/telemetrx/send"
    logger.debug(f"Sending telemetry data to {url}, data: {telemetrx_data}")
    if not url:
        raise ValueError(f"Invalid environment: {telemetrx_env}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {app_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=telemetrx_data, headers=headers) as response:
            # Optional: Basic error handling
            if response.status != 200:
                logger.error(f"Telemetry send failed for {telemetrx_env}: {response.status}")
            else:
                logger.debug(f"Telemetry send success for {telemetrx_env}: {response.status}")


# Example usage
async def send_to_correct_env(environment,
                              telemetry_data,
                              app_token,
                              telemetrx_base_url):
    await send_telemetrx_async(environment,
                               telemetry_data,
                               app_token,
                               telemetrx_base_url)


def send_telemetrx(user: str,
                   app_name: str,
                   telemetry_data=None,
                   telemetrx_env: str = "stage",
                   telemetry_type: Literal["Adoption", "Enablement", "Other"] = "Adoption",
                   technology_stripe: str = "Not specified",
                   anonymize: bool = False,
                   get_orgstats: bool = True,
                   telemetrx_base_url: str = None,
                   app_token: str = None,
                   proxy_app: dict = None,
                   ):
    """
    Helps to send Telemetrx data asynchronously to the appropriate URL.

    :param proxy_app: In case service App is sending data for proxy app, this will be used to send data
    :param telemetrx_base_url: Telemetrx Base URL provided or based on environment variable BASE_URL_{telemetrx_env}
    :param app_token: App Token provided or based on environment variable TELEMETRX_API_KEY
    :param get_orgstats: When set to true, the TelemetrX backend will generate some more details about the user, e.g their workgroup, id ...
    :param anonymize: When set to true, the user details will be encoded in the TelemetrX
    backend. It is set to False by default.
    :param technology_stripe: Defines the Technology stripe where the application belongs. E.g Collaboration, Service Provider, Enterprise... It is set to "Not specified" by default.
    :param telemetry_type: Defines the type of Telemetry data sent. Acceptable values are Adoption, Enablement and Other. It is set to Adoption by default.
    :param telemetry_data: Dictionary of telemetry data Will be added in Telemetry data as telemetry__{app_name.replace(' ', '-')}__{key}
    :param user: User CEC or identifier, this would be anonymized in TelemetrX if anonymize is set to True
    :param app_name: Name of the app, It will be used with token to validate if App is allowed to send data
    :param telemetrx_env: Environment will be used for TelemetrX (dev, stage, or prod)
    :return: None
    """
    if telemetry_data is None:
        telemetry_data = {}
    if not app_name:
        raise ValueError("App Name is required for sending telemetry data")
    if not telemetrx_env:
        raise ValueError("TelemetrX Environment is required for sending telemetry data")
    if telemetrx_env not in ["dev", "stage", "prod"]:
        raise ValueError(
            f"Invalid TelemetrX Environment, expected either of dev, stage and prod, received {telemetrx_env}")
    if technology_stripe == "Not specified":
        raise ValueError("Please specify a technology stripe before sending your data. This ensures that your app "
                         "metrics are included in the Technology stripe dashboards.")

    if not proxy_app:
        telemetrx_data = {
            "data":
                {
                    "app_name": app_name,
                    "cec": user,
                    "telemetrx_type": telemetry_type,
                    "technology_stripe": technology_stripe,
                    "custom": {
                        **telemetry_data
                    },
                    "anonymize": anonymize,
                    "include_orgstats": get_orgstats
                }
        }
    else:
        telemetrx_data = {
            "data":
                {
                    "app_name": app_name,
                    "cec": user,
                    "telemetrx_type": telemetry_type,
                    "technology_stripe": technology_stripe,
                    "proxy_app": proxy_app,
                    "custom": {
                        **telemetry_data
                    },
                    "anonymize": anonymize,
                    "include_orgstats": get_orgstats
                }
        }
    telemetrx_base_url = f"{telemetrx_base_url or os.getenv(f'BASE_URL_{telemetrx_env}'.capitalize())}"
    app_token = app_token or os.getenv('TELEMETRX_API_KEY')
    if not app_token:
        raise ValueError("App Token is required for sending telemetry data, please provide TELEMETRX_API_KEY in env or app_token in function call")
    if not telemetrx_base_url:
        raise ValueError("TelemetrX Base URL is required for sending telemetry data, please provide BASE_URL_{telemetrx_env} in env or telemetrx_base_url in function call")
    logger.debug(f"TelemetrX data will be sent to "
                 f"{telemetrx_base_url} for {telemetrx_env} with data: {telemetrx_data}")

    asyncio.run(send_to_correct_env(telemetrx_env,
                                    telemetrx_data,
                                    app_token,
                                    telemetrx_base_url,
                                    ))
