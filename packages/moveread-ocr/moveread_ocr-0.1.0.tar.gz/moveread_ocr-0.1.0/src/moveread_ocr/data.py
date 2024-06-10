from typing import Mapping, Sequence
import string
from haskellian import iter as I
import tensorflow as tf

VOCABULARY = list(string.ascii_letters + '12345678' + '-=')
char2num = { c: i for i, c in enumerate(VOCABULARY) }

def parse_img(mat, width: int = 256, height: int = 64):
  gray = tf.image.rgb_to_grayscale(mat)
  neg = 255 - gray # type: ignore
  resized = tf.image.resize_with_pad(neg, height, width) # always pads to 0. I want pad = 255 (white). So, I negate the image before and after!
  unneg = 255 - resized
  transposed = tf.transpose(unneg, perm=[1, 0, 2])
  flipped = tf.image.flip_left_right(transposed)
  normalized = tf.cast(flipped, tf.float32) / 255. # type: ignore
  return normalized

def parse_sample(sample: tuple[bytes, str], char2num: Mapping[str, int] = char2num):
  import pure_cv as vc
  img, label = sample
  x = parse_img(vc.decode(img)) # type: ignore
  y = [char2num[c] for c in label.strip()]
  return x, y

def collate_batch(batch: tuple[tuple[tf.Tensor, Sequence[int]], ...]):
  imgs, labs = I.unzip(batch)
  return tf.stack(imgs), tf.ragged.stack(labs).to_sparse() # type: ignore