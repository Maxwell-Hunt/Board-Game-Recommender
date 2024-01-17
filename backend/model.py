import tensorflow as tf
import numpy as np

@tf.keras.saving.register_keras_serializable()
class Recommender(tf.keras.Model):
    def __init__(self, num_users, num_items, **kwargs):
        super().__init__(**kwargs)
        self.num_latent_features = 30
        self.W = tf.Variable(tf.random.normal(shape=(num_users, self.num_latent_features)))
        self.X = tf.Variable(tf.random.normal(shape=(num_items, self.num_latent_features)))
        
    def call(self, x):
        user_indices = tf.cast(x[:, 0], np.int32)
        item_indices = tf.cast(x[:, 1], np.int32)
        return tf.reduce_sum(tf.multiply(tf.gather(self.X, item_indices), tf.gather(self.W, user_indices)), axis=1)
    
@tf.keras.saving.register_keras_serializable()
def mse_with_l2(predictions, observations):
    mse = tf.keras.losses.mean_squared_error(predictions, observations)
    regularizer = tf.reduce_sum([tf.nn.l2_loss(model.W), tf.nn.l2_loss(model.X)])
    lambda_l2 = 0.0001
    return mse + lambda_l2 * regularizer