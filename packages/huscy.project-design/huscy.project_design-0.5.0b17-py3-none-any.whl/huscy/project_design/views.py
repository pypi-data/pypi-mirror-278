from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from huscy.project_design import models, serializer, services
from huscy.projects.models import Project


class ExperimentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return services.get_experiments(self.project)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializer.CreateExperimentSerializer
        else:
            return serializer.ExperimentSerializer

    def perform_create(self, serializer):
        serializer.save(project=self.project)


class SessionViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = models.Session.objects.all()
    permission_classes = (IsAuthenticated, )

    def initial(self, request, *args, **kwargs):
        self.experiment = get_object_or_404(
            models.Experiment,
            pk=self.kwargs['experiment_pk'],
            project=self.kwargs['project_pk']
        )
        super().initial(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializer.CreateSessionSerializer
        else:
            return serializer.SessionSerializer

    def perform_create(self, serializer):
        serializer.save(experiment=self.experiment)


class DataAcquisitionMethodViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                                   mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.DataAcquisitionMethod.objects.all()
    serializer_class = serializer.DataAcquisitionMethodSerializer
    permission_classes = (IsAuthenticated, )

    def initial(self, request, *args, **kwargs):
        self.session = get_object_or_404(
            models.Session,
            experiment=self.kwargs['experiment_pk'],
            pk=self.kwargs['session_pk'],
            experiment__project=self.kwargs['project_pk']
        )
        super().initial(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(session=self.session)
