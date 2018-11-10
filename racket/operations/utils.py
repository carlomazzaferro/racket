def unfold(result, keep_keys=None):
    if keep_keys:
        return [{k: v for k, v in d.as_dict().items() if k in keep_keys} for d in result]
    return [d.as_dict() for d in result]
