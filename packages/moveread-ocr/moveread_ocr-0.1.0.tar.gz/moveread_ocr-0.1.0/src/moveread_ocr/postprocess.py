from jaxtyping import Int, Shaped
import tensorflow as tf
import keras
StringLookup = keras.layers.StringLookup

def remove_blanks(path: tf.Tensor, blank: int = 0) -> tf.RaggedTensor:
  """Remove zeros from `path` across the last dimension"""
  mask = tf.not_equal(path, blank)
  return tf.ragged.boolean_mask(path, mask)

def decode_labels(labels: Int[tf.SparseTensor, "batch maxlen"], num2char: StringLookup) -> Shaped[tf.Tensor, "batch"]:
  """Converts an encoded label/prediction back into a string tensor"""
  dense = tf.sparse.to_dense(labels)
  chars = num2char(remove_blanks(dense))
  return tf.strings.reduce_join(chars, axis=-1)