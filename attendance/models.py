from django.utils import timezone

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    room = models.ForeignKey('Room')
    entry_datetime = models.DateTimeField(auto_now=True)
    entry_time = models.TimeField(auto_now=True)
    exit_datetime = models.DateTimeField(null=True, default=None)
    exit_time = models.TimeField(null=True, default=None)
    student_number = models.CharField(max_length=255)

    @staticmethod
    def students_in_library(room_id=None):
        """
        :return: a list of students currently in the library
        """
        if room_id:
            room = Room.objects.get(pk=room_id)
            return Attendance.objects.filter(exit_datetime=None, room=room)
        return Attendance.objects.filter(exit_datetime=None)

    @staticmethod
    def student_in_library(student_number):
        """
        :param student_number: student_number to be checked
        :return: True or False depending wether the student is currently in the
        library or not
        """
        students = Attendance.students_in_library()
        for s in students:
            if s.student_number == student_number:
                return True
        return False

    @staticmethod
    def entry(student_number, room):
        """

        :param student_number: student_number to be entered
        :param room: id of the room in which entry has to be made
        :return: Nothing, just does the entry for the given student number
        """
        room = Room.objects.get(id=room)
        obj = Attendance(
            student_number=student_number,
            room=room
        )
        obj.save()

    @staticmethod
    def exit(student_number):
        """
        :param student_number: student_number to be exited
        :return: Nothing, just exits the student
        """
        Attendance.objects.filter(
            student_number=student_number,
            exit_datetime=None
        ).update(
            exit_datetime=timezone.now(),
            exit_time=timezone.now().time()
        )

    def __str__(self):
        return self.student_number

    class Meta:
        verbose_name_plural = 'Attendance'
        ordering = ['entry_datetime', 'exit_datetime']
