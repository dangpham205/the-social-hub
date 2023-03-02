from enums.db import table_name_enum
from cores.elasticsearch.es_helper import ElasticSearch


def total_enrollment_informations_by_school_id(school_id):
    query = {
        "size": 0,
        "query": {
            "match": {
                "school_id": school_id
            }
        }
    }
    if ElasticSearch().check_index_is_exists(table_name_enum.USER):
        rs = ElasticSearch().client.search(
            index=table_name_enum.USER, body=query)
        total_majors = rs['hits']['total']['value']
        return total_majors
    return 0


def address_default_province_name_by_school_id(school_id):
    query = {
        "size": 1,
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "school_id": school_id
                        }
                    },
                    {
                        "match": {
                            "is_default": True
                        }
                    }
                ]
            }
        }
    }
    if ElasticSearch().check_index_is_exists(table_name_enum.USER):
        rs = ElasticSearch().client.search(index=table_name_enum.USER, body=query)
        try:
            return rs['hits']['hits'][0]['_source']['province_name']
        except:
            return None
    return None


def paginate_schools_by_province_id(province_id):
    query = {
        "query": {
            "match": {
                "province_id": province_id
            }
        }
    }
    rs = ElasticSearch().client.search(index=table_name_enum.USER, body=query)
    addresses = rs['hits']['hits']
    school_ids = set()
    for address in addresses:
        school_id = address['_source']['school_id']
        school_ids.add(school_id)
    query = {
        "bool": {
            "must": [
                {
                    "terms": {
                        "id": list(school_ids)
                    }
                }
            ]
        }
    }
    return query


def school_info_by_school_id(school_id):
    query = {
        "size": 1,
        "query": {
            "match": {
                "id": school_id
            }
        }
    }
    rs = ElasticSearch().client.search(index=table_name_enum.USER, body=query)
    try:
        school = rs['hits']['hits'][0]['_source']
        return school['name'], school['code']
    except:
        return None, None


def paginate_school(province_id, name, code):
    query = None
    if province_id:
        query = paginate_schools_by_province_id(province_id)
    if name:
        if query:  # TH tìm theo tỉnh thành sau đó còn search theo tên, code...
            query['bool']['should'] = [
                {
                    "match_phrase": {
                        "name": name.lower(),
                    }
                },
                # {
                #     "wildcard": {
                #         "name": {
                #             "value": f"*{name.lower()}*",
                #         }
                #     }
                # }
            ]
        else:
            query = {
                "bool": {
                    "must": [
                        {
                            "match_phrase": {
                                "name": name.lower(),
                            }
                        },
                        # {
                        #     "wildcard": {
                        #         "name": {
                        #             "value": f"*{name.lower()}*",
                        #         }
                        #     }
                        # }
                    ]
                }
            }
    if code:
        if query:  # TH tìm theo tỉnh thành sau đó còn search theo tên, code...
            query['bool']['must'].append(
                {
                    "wildcard": {
                        "code": f"*{code.lower()}*"
                    }
                }
            )
        else:
            query = {
                "bool": {
                    "must": [
                        {
                            "wildcard": {
                                "code": f"*{code.lower()}*"
                            }
                        }
                    ]
                }
            }
    print(query)
    return query
