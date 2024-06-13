from loguru import logger


def valid_surveyids(surveyids) -> bool:
    if surveyids is None:
        return True
    if isinstance(surveyids, int):
        return True
    if isinstance(surveyids, list):
        if all(isinstance(id, int) for id in surveyids):
            return True
    logger.error(f'Survey_ids should be either an int of a list of ints or None\nSurveyIds: {surveyids}')
    return False 