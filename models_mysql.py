# Admin masters

class CampusLocation(Model):
    name = CharField(max_length=128, primary_key=True)
    # prevent_borrowing = BooleanField(default=False)

class UserGroup(Model):
    name = CharField(max_length=24, primary_key=True)
    position = IntegerField(verbose_name='Ordering position', default=0)
    # visible = BooleanField(default=True)

class UserRole(Model):    
    name = CharField(max_length=16, primary_key=True)    
    permissions = CharField(max_length=256)  # List of permissions supplied by this role

class Currency(Model):
    name = CharField(max_length=32, primary_key=True)
    symbol = CharField(max_length=4)

# Librarian Masters

class User(Model, UserMixin):
    # username = CharField(max_length=32, unique=True)
    password = CharField(max_length=512, null=True)
    # refnum = CharField()
    name = CharField(max_length=24)
    group = ForeignKey(UserGroup)
    email = EmailField(null=True)
    # phone = CharField(max_length=16)
    # birthday = DateField()
    active = BooleanField(default=True)

class UserRoles(Model):
    user = ForeignKey(User)
    role = ForeignKey(Role)

class Publisher(Model):
    name = CharField(max_length=128, primary_key=True)

class PublishPlace(Model):
    name = CharField(max_length=128, primary_key=True)

class Creator(Model):
    name = CharField(max_length=256, unique=True) # Or comma-separated list of names
    creator_type = models.CharField(max_length=1, choices=(
        ('A', 'Author'),
        ('E', 'Editor'),
        ('I', 'Illustrator')))

# We didn't plan this field but will need to soon
class PeriodicalSubscription(Model):
    periodical_name = CharField(max_length=64)
    # More fields can be added here...

class Item(Model):
    accession = CharField() # String since old values have prefix
    status = CharField(choices=(
        ('a','Available'),
        ('b', 'Borrowed'),
        ('l', 'Lost'),
        ('d', 'Discarded'),
        ('q', 'Quarantined')))
        
    title = CharField(max_length=128)
    subtitle = CharField(max_length=128, null=True)
    # keywords = CharField(max_length=256)
    comments = CharField(max_length=,128, null=True)

    campus_location = ForeignKey(CampusLocation, required=True)
    promo_location = ForeignKey(CampusLocation,
        help_text='Prominent place where item is placed temporarily to attract readers',
        null=True)

    # Source
    price = DecimalField(precision=2)
    price_currency = ForeignKey(Currency)
    receipt_date = DateField()
    source = CharField(max_length=64) # Where it came from

    borrowed_by_user_id = ForeignKey(User)
    borrowed_by_user_name = CharField(max_length=24)
    last_borrowed_date = DateTimeField()

    #display_title = CharField(max_length=256)

    call_no = ListField(CharField(max_length=8))
    publisher = ForeignKey(Publisher)
    publish_place = ForeignKey(PublishPlace)
    publish_year = CharField(max_length=4)
    isbn = CharField(max_length=17) # TODO: Add validation

    author = ForeignKey(Creator, related_name='authored_items')
    editor = ForeignKey(Creator, related_name='edited_items')
    illustrator = ForeignKey(Creator, related_name='illustrated_items')

    periodical_name = ForeignKey(PeriodicalSubscription)

    vol_no = IntegerField(verbose_name='Volume')
    vol_issue = IntegerField(verbose_name='Vol. issue')
    
    issue_no = IntegerField(verbose_name='Issue no')
    issue_date = DateField(verbose_name='Issue Date')
    date_hide_day = BooleanField('Hide issue date',
        help_text='eg. "May 2015" instead of "22 May 2015"',
        default=False)

    # TODO: Inserts?

# Transactions

# I didn't understand how to implement meeting structure with app code
# so I've put this model for now but you may want to change it.
class BorrowCurrent(Model):
    user = ForeignKey(User, required=True)
    user_group = ForeignKey(UserGroup)
    borrow_date = DateTimeField(required=True)
    due_date = DateTimeField()
    # is_longterm = BooleanField(default=False)

class BorrowPast(Model):
    item = ForeignKey(Item)
    user = CharField(max_length=24) # not FK since User may be deleted
    user_group = CharField(max_length=24) # ditto

    borrow_date = DateTimeField()
    return_date = DateTimeField()
