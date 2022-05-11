from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from sklearn.tree import DecisionTreeClassifier
import joblib

#create a tuple
GENDER = (
    (0,'Female'),
    (1,'Male'),
)

class Data(models.Model):
    name = models.CharField(max_length=50, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(13), MaxValueValidator(19)] ,null=True)
    height = models.PositiveIntegerField(null=True)
    sex = models.PositiveIntegerField(choices=GENDER, null=True)
    predictions = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add= True)
    
    class Meta:
        ordering = ['-date']
        
        
    def __str__(self):
        return self.name    
    
    def save(self, *args, **kwargs):
        sport_model = joblib.load('sport_model.joblib')
        self.predictions = sport_model.predict([[self.age, self.height, self.sex]])
        return super().save(*args, **kwargs) #The super() function returns an object that represents the parent class.
    
    '''
     we do not know what arguments save is expecting so this is basically saying 
     "any arguments passed into our new save(...) method, just hand them off to the old overridden save(...) 
     method, positional arguments first followed by any keyword arguments"
    '''
    