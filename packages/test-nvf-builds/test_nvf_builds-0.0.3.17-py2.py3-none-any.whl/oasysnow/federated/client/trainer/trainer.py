import os
import os
import pickle
import secrets

from gennet.utils.Dataloader import *
from gennet.utils.Utility_functions import *
import numpy as np
from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants

from oasysnow.federated.common.model.global_model import GlobalModel
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]=""




class Trainer(Executor):
    def __init__(self, epochs_per_round):
        super().__init__()
        self.epochs_per_round = epochs_per_round
        self.train_images, self.train_labels = None, None
        self.test_images, self.test_labels = None, None
        self.model = None
        self.datapath = os.getcwd() + "/"


    def handle_event(self, event_type: str, fl_ctx: FLContext):
        if event_type == EventType.START_RUN:
            self.setup(fl_ctx)
        if event_type == EventType.BEFORE_PULL_TASK :
            nonce = secrets.token_urlsafe(64)
            fl_ctx.set_prop("nonce", nonce, False, False)

    def setup(self, fl_ctx: FLContext):
        client_name = fl_ctx.get_identity_name()

        scope_properties = fl_ctx.get_prop(FLContextKey.SCOPE_PROPERTIES)
        print(">>>>>>>>>SCOPE", client_name, scope_properties)
        if scope_properties is None:
            raise Exception("Scope Properties not found.")

        try:
            self.xtrain = np.load(scope_properties['xtrain'])
            self.ytrain = np.load(scope_properties['ytrain'])
            self.xval = np.load(scope_properties['xval'])
            self.yval = np.load(scope_properties['yval'])
        except Exception as e:
            raise e

        self.model = GlobalModel().get_model()
        print(self.model.summary())
        # self.var_list = [str(index) for index in range(len(self.model.get_weights()))]

    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        """
        This function is an extended function from the super class.
        As a supervised learning based trainer, the train function will run
        evaluate and train engines based on model weights from `shareable`.
        After finishing training, a new `Shareable` object will be submitted
        to server for aggregation.

        Args:
            task_name: dispatched task
            shareable: the `Shareable` object acheived from server.
            fl_ctx: the `FLContext` object achieved from server.
            abort_signal: if triggered, the training will be aborted.

        Returns:
            a new `Shareable` object to be submitted to server for aggregation.
        """

        # retrieve model weights download from server's shareable
        if abort_signal.triggered:
            return make_reply(ReturnCode.TASK_ABORTED)

        if task_name != "train":
            return make_reply(ReturnCode.TASK_UNKNOWN)

        dxo = from_shareable(shareable)
        model_weights = dxo.data

        values = list(model_weights.values())
        self.model.set_weights(values)

        # adjust LR or other training time info as needed
        # such as callback in the fit function
        self.model.fit(x=self.xtrain, y=self.ytrain, batch_size=64, epochs=self.epochs_per_round, verbose=1,
                  validation_data=(self.xval, self.yval), shuffle=True)

        client_name = fl_ctx.get_identity_name()
        current_round = shareable.get_cookie(AppConstants.CONTRIBUTION_ROUND)
        eval_result = self.model.evaluate(self.xval, self.yval)
        dict_result = dict(zip(self.model.metrics_names, eval_result))
        print(">>>>>>>> Analysis over the test set. Client: ", client_name, "; Round:", current_round, "Results:", dict_result)

        # report updated weights in shareable
        weights = {str(key): value for key, value in enumerate(self.model.get_weights())}
        run_number = fl_ctx.get_job_id()

        self.model.save_weights(self.datapath + "run_" + str(run_number) + '.weights.h5')
        with open(self.datapath + "run_" + str(run_number) + '.weights.pickle', "wb") as f:
            pickle.dump(weights, f)

        dxo = DXO(data_kind=DataKind.WEIGHTS, data=weights)

        self.log_info(fl_ctx, "Local epochs finished. Returning shareable")
        new_shareable = dxo.to_shareable()
        return new_shareable

