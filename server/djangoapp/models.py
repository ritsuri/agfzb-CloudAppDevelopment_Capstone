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
    name = models.CharField(null=False, max_length=30, default='please input car brand name')
    description = models.CharField(null=False, max_length=30, default='information of car model')
    

    # Create a toString method for object string representation
    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

model_choices = (
    ('SEDAN', 'Sedan'),
    ('SUV', 'SUV'),
    ('WAGON', 'WAGON'),
    ('COUPE', 'Coupe'),
    ('SPORT', 'Sport'),
    ('HATCHBACK', 'Hatchback'),
    ('CONVERTIBLE', 'Convertible'),
    ('MINIVAN', 'Mini Van'),
)

# User model
class CarModel(models.Model):
    dealer_id = models.IntegerField(null=False, max_length=50, default=0)
    modelname = models.CharField(null=False, max_length=30, default='please input name of car model')
    car_type = models.CharField(null=False, max_length=30, choices=model_choices)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    year = models.IntegerField(blank=True)
    
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.car_type + " " + self.modelname



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, id, dealership, name, car_make, car_model, car_year, purchase, purchase_date, review, sentiment=None):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment
        self.time = now()
        
    def __str__(self):
        return self.name