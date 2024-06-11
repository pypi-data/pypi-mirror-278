def get_fields() -> list:
    """
    Получение полей с типами из коллекции
    """
    return [
        {
            "$project": {
                "fields": {
                    "$objectToArray": "$$ROOT"
                }
            }
        },
        {
            "$unwind": "$fields"
        },
        {
            "$group": {
                "_id": "$fields.k",
                "field": {"$first": "$fields.k"},
                "type": {
                    "$first":
                        {
                            "$cond": [
                                {"$eq": [{"$type": "$fields.v"}, "boolean"]},
                                {"$type": "$fields.v"},
                                "$fields.v"
                            ]
                        }
                }
            }
        },
        {"$match": {"type": {"$ne": None}}}
    ]
