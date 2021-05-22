def is_number(value):
    if type(value) is int or type(value) is float:
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_labels(sample, dataset):
    all_label_ids = set(map(lambda x: x["label_id"], dataset.labels))
    for label_id, value in sample.labels.items():
        if label_id not in all_label_ids:
            return False, "标签(%s)未定义" % label_id

        label = dataset.get_label(label_id)
        label_type = label["type"]

        if label_type == "enum":
            if type(value) is not str:
                return False, "标签(%s)应当是枚举(字符串)类型" % label_id
            if value not in label["values"]:
                return False, "标签(%s)的值应当属于[%s],传入的值为%s" % (
                    label_id,
                    ", ".join(label["values"]),
                    "`%s`" % value,
                )

        elif label_type == "number":
            if not is_number(value):
                return False, "标签(%s)应当是数值类型" % label_id

            value = float(value)
            sample.labels[label_id] = value

            if "min_num" in label and value < label["min_num"]:
                return False, "标签(%s)的值不能小于%f" % (label_id, label["min_num"])

            if "max_num" in label and value > label["max_num"]:
                return False, "标签(%s)的值不能大于%f" % (label_id, label["max_num"])

        all_label_ids.remove(label_id)
    if len(all_label_ids) > 0:
        return False, "标签(%s)的描述缺失" % ", ".join(all_label_ids)
    return True, None
