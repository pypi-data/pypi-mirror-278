# coding: utf-8

"""
Howso API

OpenAPI implementation for interacting with the Howso API. 
"""

try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from howso.openapi.configuration import Configuration


class ReduceDataParams(object):
    """
    Auto-generated OpenAPI type.

    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'features': 'list[str]',
        'distribute_weight_feature': 'str',
        'influence_weight_entropy_threshold': 'float'
    }

    attribute_map = {
        'features': 'features',
        'distribute_weight_feature': 'distribute_weight_feature',
        'influence_weight_entropy_threshold': 'influence_weight_entropy_threshold'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, features=None, distribute_weight_feature='.case_weight', influence_weight_entropy_threshold=0.6, local_vars_configuration=None):  # noqa: E501
        """ReduceDataParams - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._features = None
        self._distribute_weight_feature = None
        self._influence_weight_entropy_threshold = None

        if features is not None:
            self.features = features
        if distribute_weight_feature is not None:
            self.distribute_weight_feature = distribute_weight_feature
        if influence_weight_entropy_threshold is not None:
            self.influence_weight_entropy_threshold = influence_weight_entropy_threshold

    @property
    def features(self):
        """Get the features of this ReduceDataParams.

        A list of context features to use when determining which cases to remove.

        :return: The features of this ReduceDataParams.
        :rtype: list[str]
        """
        return self._features

    @features.setter
    def features(self, features):
        """Set the features of this ReduceDataParams.

        A list of context features to use when determining which cases to remove.

        :param features: The features of this ReduceDataParams.
        :type features: list[str]
        """

        self._features = features

    @property
    def distribute_weight_feature(self):
        """Get the distribute_weight_feature of this ReduceDataParams.

        The name of the weight feature used when performing data reduction.

        :return: The distribute_weight_feature of this ReduceDataParams.
        :rtype: str
        """
        return self._distribute_weight_feature

    @distribute_weight_feature.setter
    def distribute_weight_feature(self, distribute_weight_feature):
        """Set the distribute_weight_feature of this ReduceDataParams.

        The name of the weight feature used when performing data reduction.

        :param distribute_weight_feature: The distribute_weight_feature of this ReduceDataParams.
        :type distribute_weight_feature: str
        """

        self._distribute_weight_feature = distribute_weight_feature

    @property
    def influence_weight_entropy_threshold(self):
        """Get the influence_weight_entropy_threshold of this ReduceDataParams.

        The quantile to use when deciding which cases to remove. Cases above this quantile will be removed.

        :return: The influence_weight_entropy_threshold of this ReduceDataParams.
        :rtype: float
        """
        return self._influence_weight_entropy_threshold

    @influence_weight_entropy_threshold.setter
    def influence_weight_entropy_threshold(self, influence_weight_entropy_threshold):
        """Set the influence_weight_entropy_threshold of this ReduceDataParams.

        The quantile to use when deciding which cases to remove. Cases above this quantile will be removed.

        :param influence_weight_entropy_threshold: The influence_weight_entropy_threshold of this ReduceDataParams.
        :type influence_weight_entropy_threshold: float
        """

        self._influence_weight_entropy_threshold = influence_weight_entropy_threshold

    def to_dict(self, serialize=False, exclude_null=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                elif 'exclude_null' in args:
                    return x.to_dict(serialize, exclude_null)
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            elif value is None and (exclude_null or attr not in self.nullable_attributes):
                continue
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ReduceDataParams):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReduceDataParams):
            return True

        return self.to_dict() != other.to_dict()
