from rest_framework import status, viewsets

from common.utils import api_success


class EnvelopedModelViewSet(viewsets.ModelViewSet):
    success_messages = {
        "list": "Records fetched successfully.",
        "retrieve": "Record fetched successfully.",
        "create": "Record created successfully.",
        "update": "Record updated successfully.",
        "partial_update": "Record updated successfully.",
        "destroy": "Record deleted successfully.",
    }

    def _response(self, action, data=None, status_code=status.HTTP_200_OK):
        return api_success(data, self.success_messages.get(action, "Request completed successfully."), status_code)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return self._response("list", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return self._response("retrieve", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self._response("create", serializer.data, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        action = "partial_update" if partial else "update"
        return self._response(action, serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self._response("destroy", {})
