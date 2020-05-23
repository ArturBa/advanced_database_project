def get_or_create(session, model, **kwargs):
    """
    Get or create item in a db
    session: database session
    model: model of a item
    **kwargs: filter data
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
