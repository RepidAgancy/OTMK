from datetime import datetime

from django.utils import timezone

from rest_framework import views, generics, status
from rest_framework.response import Response

from account import permissions, models
from account.developer.problems import serializers


class ProblemListApiView(generics.ListAPIView):
    serializer_class = serializers.ProblemsSerializer
    queryset = models.Problem.objects.filter(programmer_id__isnull=True)
    permission_classes = (permissions.IsProgrammer, )


class SolveProblemApiView(views.APIView):
    permission_classes = (permissions.IsProgrammer, )

    def post(self, request, problem_id):
        programmer = request.user
        if programmer.status == models.BUSY:
            return Response({"message": "You are busy"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            problem = models.Problem.objects.get(id=problem_id, is_solved=False, programmer=None)
        except models.Problem.DoesNotExist:
            return Response({"message": f"Problem ({problem_id}) not fount"})
        problem.programmer = programmer
        problem.start_time = timezone.now().time()
        problem.status = models.IN_PROCESS
        programmer.status = models.BUSY
        problem.save()
        programmer.save()
        return Response({"message": "successfully accepted"})


class ProblemIsSolvedApiView(views.APIView):
    permission_classes = (permissions.IsProgrammer,)

    def post(self, request, problem_id):
        programmer = request.user
        if programmer.status == models.NOT_BUSY:
            return Response({"message": "you are not busy"})
        try:
            problem = models.Problem.objects.get(id=problem_id, programmer=programmer, programmer_is_solve=False)
        except models.Problem.DoesNotExist:
            return Response({"message": f"Problem ({problem_id}) not fount"})

        problem.programmer_is_solve = True
        problem.end_time = timezone.now().time()

        problem.solve_date = datetime.now().date()
        problem.solve_time = datetime.now().time()
        problem_solve_time = timezone.make_aware(datetime.now()) - problem.created_at
        problem.problem_solve_time = str(problem_solve_time)
        problem.status = models.DONE
        problem.save()
        programmer.status = models.NOT_BUSY
        programmer.save()
        return Response({'message': 'Problem successfully solved'})


class KeepBusyApiView(views.APIView):
    permission_classes = (permissions.IsProgrammer, )

    def post(self, request):
        programmer = request.user
        if programmer.status == models.BUSY:
            return Response({"message": "You are busy"})
        keep_busy = models.KeepBusy.objects.create(
            programmer=programmer,
        )
        programmer.status = models.BUSY
        programmer.save()
        return Response({"message": "user successfully be busy"})


class UserKeepNotBusyApiView(generics.GenericAPIView):
    permission_classes = (permissions.IsProgrammer,)
    serializer_class = serializers.KeepBusySerializer

    def get(self, request):
        if request.user.status == models.NOT_BUSY:
            return Response({"message": "You are not busy"}, status=status.HTTP_400_BAD_REQUEST)
        keep_busy = models.KeepBusy.objects.filter(programmer=request.user).last()
        if not keep_busy:
            return Response({"message": "you are not busy"})
        return Response({"data": f"{keep_busy.created_at.date()}, {keep_busy.start_time.strftime("%H:%M")}, {datetime.now().time().strftime("%H:%M")}"}, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.status == models.NOT_BUSY:
            return Response({"message": "You are not busy"})
        serializer = serializers.KeepBusySerializer(data=request.data)
        serializer.is_valid()
        keep_busy = models.KeepBusy.objects.filter(programmer__id=request.user.id).last()
        keep_busy.comment = serializer.validated_data['comment']
        keep_busy.end_time = datetime.now().time()
        keep_busy.save()
        request.user.status = models.NOT_BUSY
        request.user.save()
        return Response({"message": "successfully confirmed"}, status=status.HTTP_200_OK)


