from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import logging
import constants

security = HTTPBasic()
logger = logging.getLogger("file_api")

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if not (
        secrets.compare_digest(credentials.username, constants.username) and
        secrets.compare_digest(credentials.password, constants.password)
    ):
        logger.warning("Unauthorized access")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return credentials.username