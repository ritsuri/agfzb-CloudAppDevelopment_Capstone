from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

# User model

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='please input your name')
    description = models.CharField(null=False, max_length=30, default='information of car model')
    

    # Create a toString method for object string representation
    def __str__(self):
        return self.name + " " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

model_choices = (
    ('Sedan', 'Sedan'),
    ('SUV', 'SUV'),
    ('Wagon', 'Wagon')
)

# User model
class CarModel(models.Model):
    dealer_id = models.IntegerField(null=False, max_length=30, default='xx')
    #modelname = models.CharField(null=False, max_length=30, default='please input name of car model')
    car_type = models.CharField(null=False, max_length=30, choices=model_choices)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    year = models.DateField(null=True)
    
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.car_type + " " + self.year



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
