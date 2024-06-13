# Manual Select

> Pipeline interface for manual grid selection

## TL; DR

- Input (`Qin`): an image and the scoresheet model
- Output (`Qout`):
  - `Selected`: the grid corners
  - `Recorrect`: the image is too distorted to select the grid

## Usage

```python
import moveread.pipelines.manual_select as sel

Qin = Queue[tuple[sel.Task, State]] = ...
Qout = Queue[tuple[sel.Result, State]] = ...

api = SelectAPI(Qin, Qout)
await api.items().sync()
await api.select('id', Rectangle(tl=[0, 0], size=[1, 1]))
await api.recorrect('id')
```

- Run [demo.ipynb](demo.ipynb) for a full example