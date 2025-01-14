import math


def do_naive_bayes_prediction(
    x, observed_class_distribution: dict, attribute_observers: dict
):
    """Perform Naive Bayes prediction

    Parameters
    ----------
    x
        The feature values.

    observed_class_distribution
        Observed class distribution

    attribute_observers
        Attribute (features) observer

    Returns
    -------
    votes
        dict

    Notes
    -----
    This method is not intended to be used as a stand-alone method.
    """
    total_weight = sum(observed_class_distribution.values())
    if not observed_class_distribution or total_weight == 0:
        # No observed class distributions, all classes equal
        return None

    votes = {}
    for class_index, class_weight in observed_class_distribution.items():
        # Prior
        if class_weight > 0:
            votes[class_index] = math.log(class_weight / total_weight)
        else:
            votes[class_index] = 0.0
            continue

        if attribute_observers:
            for att_idx in attribute_observers:
                if att_idx not in x:
                    continue
                obs = attribute_observers[att_idx]
                # Prior plus the log likelihood
                tmp = obs.probability_of_attribute_value_given_class(
                    x[att_idx], class_index
                )
                votes[class_index] += math.log(tmp) if tmp > 0 else 0.0

    # Max log-likelihood
    max_ll = max(votes.values())
    # Apply the log-sum-exp trick (https://stats.stackexchange.com/a/253319)
    lse = max_ll + math.log(
        sum(math.exp(log_proba - max_ll) for log_proba in votes.values())
    )

    for class_index in votes:
        votes[class_index] = math.exp(votes[class_index] - lse)

    return votes
