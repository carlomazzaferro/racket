from functools import reduce


def unfold(result, keep_keys=None, filter_keys=None):
    if keep_keys:
        return [{k: v for k, v in d.as_dict().items() if k in keep_keys} for d in result]
    if filter_keys:
        return [{k: v for k, v in d.as_dict().items() if k not in filter_keys} for d in result]
    return [d.as_dict() for d in result]


def merge_result_sequences(lists):
    return list(map(lambda p: reduce(lambda x, y: {**x, **y}, p), zip(*lists)))


def merge_and_unfold(result, keep_keys=None, filter_keys=None):
    r = len(result[0])
    unfolded = [unfold([d[i] for d in result], keep_keys=keep_keys, filter_keys=filter_keys)
                for i in range(r)]
    return merge_result_sequences(unfolded)
