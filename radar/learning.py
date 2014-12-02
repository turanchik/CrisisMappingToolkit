# -----------------------------------------------------------------------------
# Copyright * 2014, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration. All
# rights reserved.
#
# The Crisis Mapping Toolkit (CMT) v1 platform is licensed under the Apache
# License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
# -----------------------------------------------------------------------------

import ee
from util.mapclient_qt import centerMap, addToMap

import domains
from histogram import RadarHistogram

def __learning_threshold(domain, algorithm):
    training_domain = domains.get_radar_image(domains.TRAINING_DATA[domain.id])
    classifier = ee.apply('TrainClassifier', {'image': training_domain.image,
                            'subsampling' : 0.07,
                            'training_image' : domains.get_ground_truth(training_domain),
                            'training_band': 'b1',
                            'training_region' : training_domain.bounds,
                            'max_classification': 2,
                            'classifier_name': algorithm})
    classified = ee.call('ClassifyImage', domain.image, classifier).select(['classification'], ['b1']);
    return classified;

def decision_tree(domain):
    return __learning_threshold(domain, 'Cart')
def random_forests(domain):
    return __learning_threshold(domain, 'RifleSerialClassifier')
def svm(domain):
    return __learning_threshold(domain, 'Pegasos')


