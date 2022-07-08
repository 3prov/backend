# from rest_framework import generics
# from api.models import FormURL
#
#
# class EvaluationFormURLCreate(generics.CreateAPIView):
#     queryset = FormURL.objects.all()
#     serializer_class = FormURLCreateSerializer
#     permission_classes = [permissions.AllowAny, IsWorkAcceptingStage, IsWorkDoesNotAlreadyExistsFromFormURL]
#
#     def create(self, request, *args, **kwargs):
#         form_url = FormURL.get_from_url(url=kwargs['encoded_part'])
#         if not form_url:
#             raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})
#         added_essay = Essay.objects.create(
#             task=Text.get_current(),
#             body=request.data['body'],
#             author=form_url.user
#         )
#         return Response(EssayFormURLCreateSerializer(added_essay).data, status=status.HTTP_201_CREATED)  # TODO: change EssayFormURLCreateSerializer
