"""
### Manual Correct
> Pipeline interface for a Manual Correction API

```
api = CorrectAPI(Qin, Qcorr, Qrot)

await api.items().sync()
await api.correct('id', Corners(tl=[0, 0], tr=[0, 1], br=[1, 1], bl=[1, 0]))
await api.rotate('id', 90)
```
"""
import lazy_loader as lazy
__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)