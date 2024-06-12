import tf.records as tfr

SCHEMA = tfr.schema(image=tfr.Tensor((256, 64, 1), 'float'), label='string')