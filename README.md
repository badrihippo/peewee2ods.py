# peewee2ods.py

This script takes in a [peewee](http://docs.peeewe-orm.com)
model definition file and output an ods file containing details about the
data tables.

Test data is in `test_models.py`; main script is (you guessed it)
`peewee2ods.py`. Run like this:

    python peewee2ods.py path/to/inputfile

Output will be in `peewee_models.py`

The current version is very fussy about the format of lines, and does not
yet support multiline field definitions. This will not work:

    status = CharField(choices=(
        ('a','Available'),
        ('b', 'Borrowed'),
        ('l', 'Lost'),
        ('d', 'Discarded'),
        ('q', 'Quarantined')))

...and meanwhile, this will end up in the file, even though it probably
shouldn't:

    # Following field is yet to be implemented
    # keywords = CharField(max_length=256)

I'll try working to update this, but contributions are always welcome ;-)

Speaking of which, see the TODO.md file if you want to help out!
