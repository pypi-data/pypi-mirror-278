import tensorflow as tf
import keras

def parse_labels(labels, char2num: keras.layers.StringLookup):
  clean = tf.strings.regex_replace(labels, '[\+#]', '')
  split = tf.strings.unicode_split(clean, 'UTF-8')
  y: tf.RaggedTensor = char2num(split)
  return y.to_sparse()