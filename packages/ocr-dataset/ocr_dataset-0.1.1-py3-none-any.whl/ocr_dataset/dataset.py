from typing_extensions import Iterable, Protocol, TypeVar, Generic
from dataclasses import dataclass
from haskellian import iter as I

T = TypeVar('T', covariant=True)

class DatasetProto(Protocol, Generic[T]):
  def iterate(self, key: str) -> Iterable[T]:
    ...
  def len(self, key: str, /) -> int | None:
    ...

@dataclass
class Dataset:

  images: DatasetProto[bytes]
  labels: DatasetProto[str]

  @classmethod
  def read(cls, base: str) -> 'Dataset':
    import lines_dataset as lds
    import files_dataset as fds
    return Dataset(
      labels=lds.Dataset.read(base),
      images=fds.Dataset.read(base),
    )
  
  @I.lift
  def iterate(self, images_key: str = 'images', labels_key: str = 'labels') -> Iterable[tuple[bytes, str]]:
    return zip(self.images.iterate(images_key), self.labels.iterate(labels_key))
  
  def __iter__(self):
    return self.iterate()
  
  def len(self, images_key: str = 'images', labels_key: str = 'labels') -> int | None:
    images_len = self.images.len(images_key)
    labels_len = self.labels.len(labels_key)
    if images_len is not None and labels_len is not None:
      return min(images_len, labels_len)