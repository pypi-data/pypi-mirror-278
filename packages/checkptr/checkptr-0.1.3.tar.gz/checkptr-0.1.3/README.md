# Checkptr

> Simple, framework-agnostic standard for model checkpointing

```bash
pip install checkptr
```

```python
from checkptr import Checkpointer

chkptr = Checkpointer.pytorch('path/to/checkpoints')
# or Checkpointer('path', save_fn=torch.save, load_fn=torch.load)

chkptr.checkpoint(model, f'model_{epoch}.pth')
model = checkptr.load(f'model_{epoch}.pth')


print('Checkpoints:', chkptr.checkpoints()) # ['model_0.pth', 'model_1.pth', ...]
```

Creates:

```
checkpoints/
  model_0.pth
  model_1.pth
  ...
```


And that's it! Simple.