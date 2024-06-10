from typing import Callable, TypeVar, Generic, Protocol
from dataclasses import dataclass
import os

Model = TypeVar('Model')

class LoadFn(Protocol, Generic[Model]):
  def __call__(self, path: str, model: Model | None = None) -> Model:
    ...

@dataclass
class Checkpointer(Generic[Model]):

  base_path: str
  save_fn: Callable[[Model, str], None]
  load_fn: LoadFn[Model]

  @classmethod
  def pytorch(cls, base_path: str, *, weights_only: bool = True):
    import torch
    if weights_only:
      def save(model, path):
        torch.save(model.state_dict(), path)

      def load(path: str, model = None): # type: ignore
        if model is None:
          raise ValueError('Model must be provided when loading weights only')
        model.load_state_dict(torch.load(path))
        return model
      
    else:
      def save(model, path):
        torch.save(model, path)

      def load(path, model = None):
        return torch.load(path)
      
    return Checkpointer[torch.nn.Module](base_path, save, load)
  
  @classmethod
  def keras(cls, base_path: str, *, weights_only: bool = True):
    import keras
    if weights_only:
      def save(model: keras.Model, path): # type: ignore
        model.save_weights(path)
      def load(path, model=None): # type: ignore
        if model is None:
          raise ValueError('Model must be provided when loading weights only')
        model.load_weights(path)
        return model
    else:
      def save(model, path):
        model.save(path)
      def load(path, model = None):
        return keras.models.load_model(path)
    
    return Checkpointer[keras.Model](base_path, save, load)

  def path(self, name: str) -> str:
    return os.path.join(self.base_path, name)

  def checkpoint(self, model: Model, name: str):
    os.makedirs(self.base_path, exist_ok=True)
    self.save_fn(model, self.path(name))

  def load(self, name: str) -> Model:
    return self.load_fn(self.path(name))
  
  def checkpoints(self):
    return os.listdir(self.base_path)