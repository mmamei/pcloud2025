def new_data(request):
    from google.cloud import firestore
    db = firestore.Client(database='test1')
    sensor = request.values['sensor']
    data = request.values['date']
    val = float(request.values['val'])
    entity = db.collection('sensors').document(sensor).get()
    if entity.exists:
        d = entity.to_dict()
        d['readings'].append({'data':data, 'val':val})
        db.collection('sensors').document(sensor).set(d)
    else:
        db.collection('sensors').document(sensor).set({'readings':[{'data':data, 'val':val}]})
    return 'ok', 200