from . import models
from huscy.project_design.models import DataAcquisitionMethod, Experiment, Session


def create_experiment(project, description='', sessions=[], title=''):
    order = project.experiments.count()

    experiment = Experiment.objects.create(
        description=description,
        order=order,
        project=project,
        title=title or f'Experiment {order + 1}',
    )

    for session in sessions:
        create_session(experiment, **session)

    return experiment


def create_session(experiment, data_acquisition_methods=[], title=''):
    order = experiment.sessions.count()

    session = Session.objects.create(
        experiment=experiment,
        order=order,
        title=title or f'Session {order + 1}',
    )

    for data_acquisition_method in data_acquisition_methods:
        create_data_acquisition_method(session, **data_acquisition_method)

    return session


def create_data_acquisition_method(session, type, duration, location='', setup_time=None,
                                   teardown_time=None, stimulus=None):
    order = session.data_acquisition_methods.count()

    if isinstance(type, models.DataAcquisitionMethodType):
        pass
    elif isinstance(type, str):
        type = models.DataAcquisitionMethodType.objects.get(pk=type)
    else:
        raise ValueError('Unknown data type for `type` attribute')

    return DataAcquisitionMethod.objects.create(
        duration=duration,
        location=location,
        order=order,
        session=session,
        stimulus=stimulus,
        type=type,
    )


def get_experiments(project):
    return project.experiments.order_by('order')


def get_sessions(experiment):
    return experiment.sessions.order_by('order')


def get_data_acquisition_methods(session):
    return session.data_acquisition_methods.order_by('order')


def get_data_acquisition_method_type(short_name):
    return models.DataAcquisitionMethodType.objects.get(short_name=short_name)


def update_experiment(experiment, **kwargs):
    updatable_fields = (
        'description',
        'order',
        'title',
    )
    return update(experiment, updatable_fields, **kwargs)


def update_session(session, **kwargs):
    updatable_fields = (
        'title',
    )
    return update(session, updatable_fields, **kwargs)


def update_data_acquisition_method(data_acquisition_method, **kwargs):
    updatable_fields = (
        'duration',
        'location',
        'setup_time',
        'stimulus',
        'teardown_time',
    )
    return update(data_acquisition_method, updatable_fields, **kwargs)


def update(instance, updatable_fields, **kwargs):
    update_fields = []

    for field_name, value in kwargs.items():
        if field_name not in updatable_fields:
            raise ValueError(f'Cannot update field "{field_name}".')
        setattr(instance, field_name, value)
        update_fields.append(field_name)

    if update_fields:
        instance.save(update_fields=update_fields)

    return instance
