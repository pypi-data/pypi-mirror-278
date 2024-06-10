import pathlib

from gennet.utils.Utility_functions import sensitivity, specificity
import tensorflow as tf

from oasysnow.federated.common.model.gennet_model import GenNet

class GlobalModel():
    def __init__(self):

        self.weight_positive_class = 2
        self.weight_negative_class = 1
        self.inputsize = 100

        path_to_file = pathlib.Path(__file__).parent.resolve()
        self.genemask_path = path_to_file / 'data/SNP_gene_mask.npz'
        self.model = GenNet(genemask_path=self.genemask_path)
        optimizer = tf.keras.optimizers.Adam(lr=0.0006)
        self.model.compile(loss=self.weighted_binary_crossentropy, optimizer=optimizer,
                      metrics=["accuracy", sensitivity, specificity, tf.keras.metrics.AUC()])

        _ = self.model(tf.keras.Input(shape=(self.inputsize,)))

    def get_model(self):
        return self.model


    def weighted_binary_crossentropy(self, y_true, y_pred):
        y_true = tf.keras.backend.clip(y_true, 0.0001, 1)
        y_pred = tf.keras.backend.clip(y_pred, 0.0001, 1)

        return tf.keras.backend.mean(
            -y_true * tf.keras.backend.log(y_pred + 0.0001) * self.weight_positive_class - (1 - y_true) * tf.keras.backend.log(
                1 - y_pred + 0.0001) * self.weight_negative_class)
