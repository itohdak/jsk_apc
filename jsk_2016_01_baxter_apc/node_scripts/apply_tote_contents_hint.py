#!/usr/bin/env python

import numpy as np

from jsk_2015_05_baxter_apc.msg import ObjectRecognition
import jsk_apc2016_common
from jsk_recognition_msgs.msg import ClassificationResult
from jsk_topic_tools import ConnectionBasedTransport
from jsk_topic_tools.log_utils import jsk_logwarn
import rospy


class ApplyToteContentsHint(ConnectionBasedTransport):

    """Use tote contents info to improve object recognition"""

    def __init__(self):
        super(self.__class__, self).__init__()
        json_file = rospy.get_param('~json')
        self.tote_contents = jsk_apc2016_common.get_tote_contents(json_file)
        self.pub = self.advertise('~output', ObjectRecognition, queue_size=1)

    def subscribe(self):
        self.sub = rospy.Subscriber('~input', ClassificationResult,
                                    self._apply)

    def unsubscribe(self):
        self.sub.unregister()

    def _apply(self, msg):
        # get candidates probabilities
        candidates = self.tote_contents
        label_to_proba = dict(zip(msg.target_names, msg.probabilities))
        candidates_proba = [label_to_proba[label] for label in candidates]
        candidates_proba = np.array(candidates_proba)
        candidates_proba = candidates_proba / candidates_proba.sum()

        # compose output message
        top_index = np.argmax(candidates_proba)
        out_msg = ObjectRecognition(
            header=msg.header,
            matched=candidates[top_index],
            probability=candidates_proba[top_index],
            candidates=candidates,
            probabilities=candidates_proba,
        )
        self.pub.publish(out_msg)


if __name__ == '__main__':
    rospy.init_node('apply_tote_contents_hint')
    app = ApplyToteContentsHint()
    rospy.spin()
