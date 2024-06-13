# Auto Extraction

> Pipeline interface for an auto-extraction daemon

```
import moveread.pipelines.auto_extract as extr

Qin: tuple[extr.Task, State] = ...
Qerr: tuple[extr.Err, State] = ...
Qok: tuple[extr.ok, State] = ...

await extr.run(Qin, Qerr, Qok)
```

- Run [demo.ipynb](demo.ipynb) for a full example