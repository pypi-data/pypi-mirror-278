import tensorflow as tf
import keras

def valid_labels(labels, vocab: str, maxlen: int = 10, minlen: int = 2):
  or_ = '|'.join(vocab)
  vocab_regex = f'^({or_})+$'
  vocab_ok = tf.strings.regex_full_match(labels, vocab_regex)
  short_enough = tf.strings.length(labels) <= maxlen
  long_enough = tf.strings.length(labels) >= minlen
  return vocab_ok and short_enough and long_enough

def parse_labels(labels, char2num: keras.layers.StringLookup, vocab: str):
  oov_regex = f'[^{vocab}]'
  clean = tf.strings.regex_replace(labels, oov_regex, '')
  split = tf.strings.unicode_split(clean, 'UTF-8')
  tf.assert_greater(tf.size(split), 0)
  y: tf.RaggedTensor = char2num(split)
  return y.to_sparse()