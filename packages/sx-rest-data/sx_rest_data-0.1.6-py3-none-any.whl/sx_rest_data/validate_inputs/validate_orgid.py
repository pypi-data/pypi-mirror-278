from loguru import logger


def valid_orgid(orgid: int) -> bool:
    if orgid is None:
        return True
    if isinstance(orgid, int):
        return True
    logger.error(f'If supplied Org_id should be an int. Orgid: {orgid}')
    return False 