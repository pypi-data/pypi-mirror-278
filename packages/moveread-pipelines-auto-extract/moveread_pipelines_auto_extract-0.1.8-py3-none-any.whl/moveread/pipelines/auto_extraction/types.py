from pydantic import BaseModel
from haskellian import Either
import robust_extraction as re
from robust_extraction import ModelID
from moveread.annotations import Corners, Contours

class Task(BaseModel):
  model: ModelID
  img: bytes
  already_corrected: bool = False

class Ok(BaseModel):
  contours: Contours
  perspective_corners: Corners | None
  corrected: bytes
  contoured: bytes

class Err(BaseModel):
  error: re.Error

Result = Either[Err, Ok]