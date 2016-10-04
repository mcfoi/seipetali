from django.test import TestCase
from django.db import models
from .models import get_duplicate


class TestModel(models.Model):
    name = models.CharField(max_length=10, unique=True)
    int_number = models.IntegerField(null=True)
    text = models.CharField(max_length=10)

    class Meta:
        unique_together = ('int_number', 'text')


class GetDuplicateTestCase(TestCase):

    def setUp(self):
        self.obj0 = TestModel.objects.create(name='0', int_number=1, text='10.0')
        self.obj1 = TestModel.objects.create(name='1', int_number=2, text='10.0')
        self.obj2 = TestModel.objects.create(name='2', int_number=3, text='20.0')

    def test_no_duplicate(self):
        obj = TestModel()
        obj.name = '3'
        obj.int_number = 4
        obj.text = '30.0'
        self.assertRaises(TestModel.DoesNotExist, get_duplicate, obj=obj)

    def test_unique(self):
        dup = TestModel()
        dup.name = '0'
        self.assertEqual(get_duplicate(dup), self.obj0)

    def test_unique_together(self):
        dup = TestModel()
        dup.name = '3'
        dup.int_number = 2
        dup.text = '10.0'
        self.assertEqual(get_duplicate(dup), self.obj1)
