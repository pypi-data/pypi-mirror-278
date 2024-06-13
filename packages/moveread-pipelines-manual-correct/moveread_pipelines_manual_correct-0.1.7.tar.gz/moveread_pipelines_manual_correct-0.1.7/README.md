# Manual Correct

> Pipeline interface for a Manual Correction API

## TL; DR

- Input (`Qin`): basically an image URL
- Output (`Qout`):
  - `Corrected`: perspective corners, or
  - `Rotated`: angle of rotation (in 90º increments)

## Usage

```python
import moveread.pipelines.manual_correct as corr

Qin = Queue[tuple[corr.Task, State]] = ...
Qout = Queue[tuple[corr.Result, State]] = ...


api = corr.CorrectAPI(Qin, Qout)

await api.items().sync()
await api.correct('id', Corners(tl=[0, 0], tr=[0, 1], br=[1, 1], bl=[1, 0]))
await api.rotate('id', 90)
```

- Run [demo.ipynb](demo.ipynb) for a full example