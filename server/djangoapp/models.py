from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Car Make Model
class CarMake(models.Model):
    name = models.CharField(max_length=100)  # Name of the car make
    description = models.TextField()  # Description of the car make
    # You can add any other fields you'd like for the car make

    def __str__(self):
        return self.name  # Return the name as the string representation

# Car Model Model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship with CarMake
    name = models.CharField(max_length=100)  # Name of the car model
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # You can add more choices for car types as needed
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')  # Type of the car model
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),  # Max value of 2023
            MinValueValidator(2015)   # Min value of 2015
        ]
    )
    # You can add other fields for the car model if needed, such as price, color, etc.

    def __str__(self):
        return f"{self.car_make.name} {self.name}"  # Return a string representation combining car make and model name
