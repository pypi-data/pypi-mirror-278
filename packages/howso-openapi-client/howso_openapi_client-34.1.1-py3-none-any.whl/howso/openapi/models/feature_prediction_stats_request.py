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


class FeaturePredictionStatsRequest(object):
    """
    Auto-generated OpenAPI type.

    The body of a feature prediction stats request. 
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'action_feature': 'str',
        'robust': 'bool',
        'robust_hyperparameters': 'bool',
        'stats': 'list[str]',
        'weight_feature': 'str',
        'action_condition': 'dict[str, object]',
        'action_condition_precision': 'str',
        'action_num_cases': 'float',
        'context_condition': 'dict[str, object]',
        'context_condition_precision': 'str',
        'context_precision_num_cases': 'float',
        'num_robust_influence_samples_per_case': 'float'
    }

    attribute_map = {
        'action_feature': 'action_feature',
        'robust': 'robust',
        'robust_hyperparameters': 'robust_hyperparameters',
        'stats': 'stats',
        'weight_feature': 'weight_feature',
        'action_condition': 'action_condition',
        'action_condition_precision': 'action_condition_precision',
        'action_num_cases': 'action_num_cases',
        'context_condition': 'context_condition',
        'context_condition_precision': 'context_condition_precision',
        'context_precision_num_cases': 'context_precision_num_cases',
        'num_robust_influence_samples_per_case': 'num_robust_influence_samples_per_case'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, action_feature=None, robust=None, robust_hyperparameters=None, stats=None, weight_feature=None, action_condition=None, action_condition_precision=None, action_num_cases=None, context_condition=None, context_condition_precision=None, context_precision_num_cases=None, num_robust_influence_samples_per_case=None, local_vars_configuration=None):  # noqa: E501
        """FeaturePredictionStatsRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._action_feature = None
        self._robust = None
        self._robust_hyperparameters = None
        self._stats = None
        self._weight_feature = None
        self._action_condition = None
        self._action_condition_precision = None
        self._action_num_cases = None
        self._context_condition = None
        self._context_condition_precision = None
        self._context_precision_num_cases = None
        self._num_robust_influence_samples_per_case = None

        if action_feature is not None:
            self.action_feature = action_feature
        if robust is not None:
            self.robust = robust
        if robust_hyperparameters is not None:
            self.robust_hyperparameters = robust_hyperparameters
        if stats is not None:
            self.stats = stats
        if weight_feature is not None:
            self.weight_feature = weight_feature
        if action_condition is not None:
            self.action_condition = action_condition
        if action_condition_precision is not None:
            self.action_condition_precision = action_condition_precision
        if action_num_cases is not None:
            self.action_num_cases = action_num_cases
        if context_condition is not None:
            self.context_condition = context_condition
        if context_condition_precision is not None:
            self.context_condition_precision = context_condition_precision
        if context_precision_num_cases is not None:
            self.context_precision_num_cases = context_precision_num_cases
        if num_robust_influence_samples_per_case is not None:
            self.num_robust_influence_samples_per_case = num_robust_influence_samples_per_case

    @property
    def action_feature(self):
        """Get the action_feature of this FeaturePredictionStatsRequest.

        When specified, will attempt to return stats that were computed for this specified action_feature. Note 1: \".targetless\" is the action feature used during targetless analysis. Note 2: If get_prediction_stats is being used with time series analysis, the action feature for which the prediction statistics information is desired must be specified. 

        :return: The action_feature of this FeaturePredictionStatsRequest.
        :rtype: str
        """
        return self._action_feature

    @action_feature.setter
    def action_feature(self, action_feature):
        """Set the action_feature of this FeaturePredictionStatsRequest.

        When specified, will attempt to return stats that were computed for this specified action_feature. Note 1: \".targetless\" is the action feature used during targetless analysis. Note 2: If get_prediction_stats is being used with time series analysis, the action feature for which the prediction statistics information is desired must be specified. 

        :param action_feature: The action_feature of this FeaturePredictionStatsRequest.
        :type action_feature: str
        """

        self._action_feature = action_feature

    @property
    def robust(self):
        """Get the robust of this FeaturePredictionStatsRequest.

        When specified, will attempt to return stats that were computed with the specified robust or non-robust type. 

        :return: The robust of this FeaturePredictionStatsRequest.
        :rtype: bool
        """
        return self._robust

    @robust.setter
    def robust(self, robust):
        """Set the robust of this FeaturePredictionStatsRequest.

        When specified, will attempt to return stats that were computed with the specified robust or non-robust type. 

        :param robust: The robust of this FeaturePredictionStatsRequest.
        :type robust: bool
        """

        self._robust = robust

    @property
    def robust_hyperparameters(self):
        """Get the robust_hyperparameters of this FeaturePredictionStatsRequest.

        When specified, will attempt to return stats that were computed using hyperparameters with the specified robust or non-robust type. 

        :return: The robust_hyperparameters of this FeaturePredictionStatsRequest.
        :rtype: bool
        """
        return self._robust_hyperparameters

    @robust_hyperparameters.setter
    def robust_hyperparameters(self, robust_hyperparameters):
        """Set the robust_hyperparameters of this FeaturePredictionStatsRequest.

        When specified, will attempt to return stats that were computed using hyperparameters with the specified robust or non-robust type. 

        :param robust_hyperparameters: The robust_hyperparameters of this FeaturePredictionStatsRequest.
        :type robust_hyperparameters: bool
        """

        self._robust_hyperparameters = robust_hyperparameters

    @property
    def stats(self):
        """Get the stats of this FeaturePredictionStatsRequest.

        Types of stats to output. When unspecified, returns all. 

        :return: The stats of this FeaturePredictionStatsRequest.
        :rtype: list[str]
        """
        return self._stats

    @stats.setter
    def stats(self, stats):
        """Set the stats of this FeaturePredictionStatsRequest.

        Types of stats to output. When unspecified, returns all. 

        :param stats: The stats of this FeaturePredictionStatsRequest.
        :type stats: list[str]
        """
        allowed_values = ["accuracy", "confusion_matrix", "contribution", "mae", "mda", "mda_permutation", "missing_value_accuracy", "precision", "r2", "recall", "rmse", "spearman_coeff", "mcc"]  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                not set(stats).issubset(set(allowed_values))):  # noqa: E501
            raise ValueError(
                "Invalid values for `stats` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(stats) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._stats = stats

    @property
    def weight_feature(self):
        """Get the weight_feature of this FeaturePredictionStatsRequest.

        When specified, will attempt to return stats that were computed using this weight_feature. 

        :return: The weight_feature of this FeaturePredictionStatsRequest.
        :rtype: str
        """
        return self._weight_feature

    @weight_feature.setter
    def weight_feature(self, weight_feature):
        """Set the weight_feature of this FeaturePredictionStatsRequest.

        When specified, will attempt to return stats that were computed using this weight_feature. 

        :param weight_feature: The weight_feature of this FeaturePredictionStatsRequest.
        :type weight_feature: str
        """

        self._weight_feature = weight_feature

    @property
    def action_condition(self):
        """Get the action_condition of this FeaturePredictionStatsRequest.

        A condition map to select the action set, which is the dataset for which the prediction stats are for. If both action_condition and context_condition are provided, then all of the action cases selected by the action_condition will be excluded from the context set, which is the set being queried to make predictions on the action set, effectively holding them out. If only action_condition is specified, then only the single predicted case will be left out.  The dictionary keys are the feature name and values are one of: - None - A value, must match exactly. - An array of two numeric values, specifying an inclusive range. Only applicable to continuous and numeric ordinal features. - An array of string values, must match any of these values exactly. Only applicable to nominal and string ordinal features. 

        :return: The action_condition of this FeaturePredictionStatsRequest.
        :rtype: dict[str, object]
        """
        return self._action_condition

    @action_condition.setter
    def action_condition(self, action_condition):
        """Set the action_condition of this FeaturePredictionStatsRequest.

        A condition map to select the action set, which is the dataset for which the prediction stats are for. If both action_condition and context_condition are provided, then all of the action cases selected by the action_condition will be excluded from the context set, which is the set being queried to make predictions on the action set, effectively holding them out. If only action_condition is specified, then only the single predicted case will be left out.  The dictionary keys are the feature name and values are one of: - None - A value, must match exactly. - An array of two numeric values, specifying an inclusive range. Only applicable to continuous and numeric ordinal features. - An array of string values, must match any of these values exactly. Only applicable to nominal and string ordinal features. 

        :param action_condition: The action_condition of this FeaturePredictionStatsRequest.
        :type action_condition: dict[str, object]
        """

        self._action_condition = action_condition

    @property
    def action_condition_precision(self):
        """Get the action_condition_precision of this FeaturePredictionStatsRequest.

        Exact matching or fuzzy matching. Only used if action_condition is not not null.

        :return: The action_condition_precision of this FeaturePredictionStatsRequest.
        :rtype: str
        """
        return self._action_condition_precision

    @action_condition_precision.setter
    def action_condition_precision(self, action_condition_precision):
        """Set the action_condition_precision of this FeaturePredictionStatsRequest.

        Exact matching or fuzzy matching. Only used if action_condition is not not null.

        :param action_condition_precision: The action_condition_precision of this FeaturePredictionStatsRequest.
        :type action_condition_precision: str
        """
        allowed_values = ["exact", "similar"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and action_condition_precision not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `action_condition_precision` ({0}), must be one of {1}"  # noqa: E501
                .format(action_condition_precision, allowed_values)
            )

        self._action_condition_precision = action_condition_precision

    @property
    def action_num_cases(self):
        """Get the action_num_cases of this FeaturePredictionStatsRequest.

        The maximum amount of cases to use to calculate prediction stats. If not specified, the limit will be k cases if precision is \"similar\", or 1000 cases if precision is \"exact\". Works with or without action_condition. If action_condition is set: - If None, will be set to k if precision is \"similar\" or no limit if precision is \"exact\". If action_condition is not set: - If None, will be set to the Howso default limit of 2000. 

        :return: The action_num_cases of this FeaturePredictionStatsRequest.
        :rtype: float
        """
        return self._action_num_cases

    @action_num_cases.setter
    def action_num_cases(self, action_num_cases):
        """Set the action_num_cases of this FeaturePredictionStatsRequest.

        The maximum amount of cases to use to calculate prediction stats. If not specified, the limit will be k cases if precision is \"similar\", or 1000 cases if precision is \"exact\". Works with or without action_condition. If action_condition is set: - If None, will be set to k if precision is \"similar\" or no limit if precision is \"exact\". If action_condition is not set: - If None, will be set to the Howso default limit of 2000. 

        :param action_num_cases: The action_num_cases of this FeaturePredictionStatsRequest.
        :type action_num_cases: float
        """

        self._action_num_cases = action_num_cases

    @property
    def context_condition(self):
        """Get the context_condition of this FeaturePredictionStatsRequest.

        A condition map to select the context set, which is the set being queried to make  predictions on the action set. If both action_condition and context_condition are provided, then all of the cases from the action set, which is the dataset for which the prediction stats are for, will be excluded from the context set, effectively holding them out. If only action_condition is specified, then only the single predicted case will be left out.  The dictionary keys are the feature name and values are one of: - None - A value, must match exactly. - An array of two numeric values, specifying an inclusive range. Only applicable to continuous and numeric ordinal features. - An array of string values, must match any of these values exactly. Only applicable to nominal and string ordinal features. 

        :return: The context_condition of this FeaturePredictionStatsRequest.
        :rtype: dict[str, object]
        """
        return self._context_condition

    @context_condition.setter
    def context_condition(self, context_condition):
        """Set the context_condition of this FeaturePredictionStatsRequest.

        A condition map to select the context set, which is the set being queried to make  predictions on the action set. If both action_condition and context_condition are provided, then all of the cases from the action set, which is the dataset for which the prediction stats are for, will be excluded from the context set, effectively holding them out. If only action_condition is specified, then only the single predicted case will be left out.  The dictionary keys are the feature name and values are one of: - None - A value, must match exactly. - An array of two numeric values, specifying an inclusive range. Only applicable to continuous and numeric ordinal features. - An array of string values, must match any of these values exactly. Only applicable to nominal and string ordinal features. 

        :param context_condition: The context_condition of this FeaturePredictionStatsRequest.
        :type context_condition: dict[str, object]
        """

        self._context_condition = context_condition

    @property
    def context_condition_precision(self):
        """Get the context_condition_precision of this FeaturePredictionStatsRequest.

        Exact matching or fuzzy matching. Only used if context_condition is not not null.

        :return: The context_condition_precision of this FeaturePredictionStatsRequest.
        :rtype: str
        """
        return self._context_condition_precision

    @context_condition_precision.setter
    def context_condition_precision(self, context_condition_precision):
        """Set the context_condition_precision of this FeaturePredictionStatsRequest.

        Exact matching or fuzzy matching. Only used if context_condition is not not null.

        :param context_condition_precision: The context_condition_precision of this FeaturePredictionStatsRequest.
        :type context_condition_precision: str
        """
        allowed_values = ["exact", "similar"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and context_condition_precision not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `context_condition_precision` ({0}), must be one of {1}"  # noqa: E501
                .format(context_condition_precision, allowed_values)
            )

        self._context_condition_precision = context_condition_precision

    @property
    def context_precision_num_cases(self):
        """Get the context_precision_num_cases of this FeaturePredictionStatsRequest.

        Limit on the number of context cases when context_condition_precision is set to \"similar\". If None, will be set to k. 

        :return: The context_precision_num_cases of this FeaturePredictionStatsRequest.
        :rtype: float
        """
        return self._context_precision_num_cases

    @context_precision_num_cases.setter
    def context_precision_num_cases(self, context_precision_num_cases):
        """Set the context_precision_num_cases of this FeaturePredictionStatsRequest.

        Limit on the number of context cases when context_condition_precision is set to \"similar\". If None, will be set to k. 

        :param context_precision_num_cases: The context_precision_num_cases of this FeaturePredictionStatsRequest.
        :type context_precision_num_cases: float
        """

        self._context_precision_num_cases = context_precision_num_cases

    @property
    def num_robust_influence_samples_per_case(self):
        """Get the num_robust_influence_samples_per_case of this FeaturePredictionStatsRequest.

        Specifies the number of robust samples to use for each case for robust contribution computations. Defaults to 300 + 2 * (number of features). 

        :return: The num_robust_influence_samples_per_case of this FeaturePredictionStatsRequest.
        :rtype: float
        """
        return self._num_robust_influence_samples_per_case

    @num_robust_influence_samples_per_case.setter
    def num_robust_influence_samples_per_case(self, num_robust_influence_samples_per_case):
        """Set the num_robust_influence_samples_per_case of this FeaturePredictionStatsRequest.

        Specifies the number of robust samples to use for each case for robust contribution computations. Defaults to 300 + 2 * (number of features). 

        :param num_robust_influence_samples_per_case: The num_robust_influence_samples_per_case of this FeaturePredictionStatsRequest.
        :type num_robust_influence_samples_per_case: float
        """

        self._num_robust_influence_samples_per_case = num_robust_influence_samples_per_case

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
        if not isinstance(other, FeaturePredictionStatsRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FeaturePredictionStatsRequest):
            return True

        return self.to_dict() != other.to_dict()
