import keyring
from loguru import logger


def valid_credentials(cred_name: str) -> bool:
    creds = keyring.get_credential(cred_name, None)
    if creds is None:
        logger.error(f'Could not find credentials among the generic credentials in Windows Credentials Manager. Credentials name: {cred_name}')
        return False
    return True