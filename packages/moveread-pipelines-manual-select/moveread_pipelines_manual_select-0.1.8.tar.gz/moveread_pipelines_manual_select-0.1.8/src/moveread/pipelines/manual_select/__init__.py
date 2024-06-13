"""
### Manual Select
> Pipeline interface for manual grid selection

```
import moveread.pipelines.manual_select as sel

Qin = Queue[tuple[sel.Task, State]] = ...
Qout = Queue[tuple[sel.Result, State]] = ...

api = SelectAPI(Qin, Qout)
await api.items().sync()
await api.select('id', Rectangle(tl=[0, 0], size=[1, 1]))
await api.recorrect('id')
```
"""
import lazy_loader as lazy
__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)