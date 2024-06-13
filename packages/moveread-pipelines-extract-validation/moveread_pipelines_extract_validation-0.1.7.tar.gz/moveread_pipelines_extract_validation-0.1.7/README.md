# Extract Validation

> Pipeline interface for the auto-extract validation API

## TL; DR

- Input (`Qin`): a contoured image + whether it's already perspective-corrected
- Output (`Qout`): `'correct' | 'perspective-correct' | 'incorrect'`
  - But, `'perspective-correct'` is only acceptable whe the image isn't already perspective-corrected

## Usage

```python
import moveread.pipelines.extract_validation as val

Qin = Queue[tuple[val.Task, State]] = ...
Qout = Queue[tuple[val.Annotation, State]] = .....

api = val.ValidateAPI(Qin, Qout)

await api.items().sync()
await api.annotate('taskId', 'correct')
```