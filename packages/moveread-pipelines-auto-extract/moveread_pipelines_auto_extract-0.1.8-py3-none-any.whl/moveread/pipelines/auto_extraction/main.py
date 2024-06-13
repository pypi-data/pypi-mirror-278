from typing import Protocol, TypeVar, NamedTuple, Generic
import asyncio
from haskellian import funcs as F, Left, Right, either as E
from q.api import ReadQueue, WriteQueue, ReadError
import pure_cv as vc
import robust_extraction as re
import robust_extraction.templates as ts
from dslog import Logger
from .types import Ok, Err, Task, Result

class ExtrFn(Protocol):
  def __call__(self, img, model: ts.SheetModel, *, autocorrect: bool) -> re.Result:
    ...

def extract(task: Task, extr: ExtrFn = re.descaled_extract) -> Result: 
  mat = vc.decode(task.img)
  match extr(mat, ts.models[task.model], autocorrect=not task.already_corrected):
    case Right(ok):
      corr = vc.encode(ok.corr_img, '.jpg') # type: ignore
      cont = F.pipe(
        vc.draw.contours(ok.corr_img, ok.contours, color=(0, 0, 255)), # type: ignore
        vc.descale_h(target_height=768), # type: ignore
        vc.encode(format='.jpg'), # type: ignore
      )
      return Right(Ok(contours=ok.contours, corrected=corr, contoured=cont, perspective_corners=ok.perspective_corners))
    case Left(err):
      return Left(Err(error=err))
    

State = TypeVar('State')

class Queues(NamedTuple, Generic[State]):
  Qin: ReadQueue[tuple[Task, State]]
  Qout: WriteQueue[tuple[Result, State]]
    

async def run(
  Qin: ReadQueue[tuple[Task, State]],
  Qout: WriteQueue[tuple[Result, State]],
  *, logger: Logger = Logger.of(print).prefix('[AUTO-EXTRACT]')
):
  """Extract all tasks from `Qin`; push results to `Qerr` or `Qok`, passing along the associated state"""

  @E.do[ReadError]()
  async def run_one():
    id, (task, state) = (await Qin.read()).unsafe()
    logger(f'Extracting "{id}"')
    res = extract(task)
    (await Qout.push(id, (res, state))).unsafe()
    logger(f'Extracted "{id}": {"OK" if res.tag == "right" else f"ERR: {res.value}"}')
    (await Qin.pop(id)).unsafe()

  while True:
    e = await run_one()
    if e.tag == 'left':
      logger('Queue error', e.value, level='ERROR')
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(0) # release the loop