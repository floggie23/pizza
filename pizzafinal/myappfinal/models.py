from django.db import models
import re
import datetime
import datetime
import bcrypt

PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
class UserManager(models.Manager):  
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    def register(self, form):
        pw = bcrypt.hashpw(form['pass2'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['name'],
            last_name = form['lastname'],
            email = form['email'],
            city = form['city'],
            state = form['state'],
            adress = form['adress'],
            password = pw,
        )
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 2:
            errors["fname"] = " First Name should be at least 2 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "Last name should be at least 2 characters"
        # if not EMAIL_REGEX.match(postData['email']):
        #     errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=postData['email'])
        if 'state' not in postData:
            errors['state'] = 'Add a state'
        if email_check:
            errors['email'] = "Email already in use"
        if len(postData['adress']) < 2:
            errors["adress"] = "Add a valid address"
        if len(postData['city']) < 2:
            errors["city"] = "Add a valid city!"
        if len(postData['pass2']) < 8:
            errors['pass2'] = 'Password must be at least 8 characters'
        if postData['pass2'] != postData['re_pass']:
            errors['pass2'] = 'Passwords do not match'    
        return errors
    def updateuser_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name2']) < 2:
            errors["name2"] = " First Name should be at least 2 characters"
        if len(postData['lastname2']) < 2:
            errors["lastname2"] = "Last name should be at least 2 characters"
        # if not EMAIL_REGEX.match(postData['email2']):
        #     errors['email2'] = 'Invalid Email Address'
        email_check = self.filter(email=postData['email2'])
        if 'state2' not in postData:
            errors['state2'] = 'Add a state'
        if email_check:
            errors['email2'] = "Email already in use"
        if len(postData['adress2']) < 2:
            errors["adress2"] = "Add a valid address"
        if len(postData['city2']) < 2:
            errors["city2"] = "Add a valid city!"
        return errors
    def pizza_validator(self, postData):
        errors = {}
        if 'method' not in postData:
            errors['method'] = 'Add a method'
        if 'size' not in postData:
            errors['size'] = 'Add a pizza size'
        if 'crust' not in postData:
            errors['crust'] = 'Add crust type'
        if 'qty' not in postData:
            errors['qty'] = 'Add a quantity'
        if 'item' not in postData:
            errors['item'] = 'Add toppings'
        return errors
        
    
class User(models.Model):
    first_name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 100 , unique=True)
    last_name = models.CharField(max_length = 60)
    city = models.CharField(max_length = 60)
    adress = models.CharField(max_length = 60)
    state = models.CharField(max_length = 60)
    password = models.CharField(max_length = 150)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Order(models.Model):
    # Constants in Model class
    CARRYOUT = "Carryout"
    DELIVERY = "Delivery"
    method_choices = [
        (CARRYOUT,"carryout"),
        (DELIVERY,"delivery")
    ]
    method = models.CharField(max_length=25,choices=method_choices,default=DELIVERY)
    qty=models.IntegerField(default=1)
    price=models.DecimalField(default=0,decimal_places=0,max_digits=6)
    user = models.ForeignKey(User, related_name="orders", on_delete = models.CASCADE)
    favorite = models.ForeignKey(User, related_name="favorites", on_delete = models.CASCADE,null=True)
    # # user = models.ManyToManyField(User, related_name="")
    delivery_fee=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # def is_upperclass(self):
    #     return self.method in {self.CARRYOUT, self.DELIVERY}


class Pizza(models.Model):
    VEGGIE = "VEGETERIAN"
    PEPPERONI= "PEPPERONI"
    MARGHERITA = "MARGHERITA"
    BBQ="BARBEQUE"
    HAWAIIAN="HAWAIIAN"
    BUFFALO="BUFFALO"
    SUPREME="SUPREME"
    type_choices = [
        (VEGGIE,"veggie"),
        (PEPPERONI,"pepperoni"),
        (MARGHERITA,"margherita"),
        (BBQ,"bbq"),
        (HAWAIIAN,"hawaiian"),
        (BUFFALO,"buffalo"),
        (SUPREME,"supreme"),
    ]
    types = models.CharField(max_length=25,choices=type_choices,default=VEGGIE)
    LARGE = "LARGE"
    MEDIUM= "MEDIUM"
    SMALL = "SMALL"
    size_choices= [
        (LARGE,"large"),
        (MEDIUM,"medium"),
        (SMALL,"small"),
    ]
    size=models.CharField(max_length=25,choices=size_choices,default=MEDIUM)
    THIN_CRUST = "THIN CRUST"
    THICK_CRUST = "THICK CRUST"
    crust_choices=[
        (THIN_CRUST , "thin_crust"),
        (THICK_CRUST , "thick_crust"),
    ]
    crust=models.CharField(max_length=32,choices=crust_choices,default= THIN_CRUST)
    order=models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="pizza",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    