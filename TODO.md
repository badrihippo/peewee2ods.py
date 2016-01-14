# Next steps for peewee2ods.py

Here is the list of tasks I can think of that we need to work on for
this script. Feel free to add (or remove!) to the list.

  * Add ability to scan multiline field definitions
  * Add ability to process only actual model and field definitions
    (right now it treats *any* class definition as a "model" and *any*
    class attribute definition as a "field".
  * Use argparse to better process input arguments (maybe add option to
    process multiple model files at once)
  * Add ability to specify output file (support is there in write_data
    function, but not in argument-parsing script - mainly because there
    currently *is* no argument-parsing script
