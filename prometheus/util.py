def rep_str(dict):
    context = '\n'
    for key,value in dict.items():
        if key == "runbook_url":
            continue
        context += "%s:%s\n" %(key,value)
    return context


