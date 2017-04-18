"""
Usage:
    add_person <first_name> <last_name> (fellow|staff) [(y|n)]
    create_room (office|living_space) <room_name>...
    reallocate_person <first_name> <"last_name"> <new_room>
    load_people <filename>
    print_allocations [--o=filename]
    print_unallocated [--o=filename]
    print_room <room_name>
    save_state [--db=sqlite_database]
    load_state [--db=sqlite_database]
    quit
Options:
    -h, --help  Show this screen and exit
    -i --interactive  Interactive Mode
    wants_accommodation=<N> [default: N]
"""

import cmd
import os
from termcolor import cprint, colored
from pyfiglet import figlet_format
from docopt import docopt, DocoptExit
from modules.amity import Amity
from db.amity_db import *

amity_object = Amity()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

border = colored("*" * 60, 'yellow').center(140)


def introduction():

    print(border)
    print('WELCOME TO AMITY ALLOCATION '.center(140))
    print("1. create_room (Office|Living Space) <room_name>".center(35) + " \t \t \t \t"+
          "5. print_allocations [--o=filename.txt]".center(60))
    print("2. add_person < first_name> <last_name> (Fellow|Staff) [<wants_space>]".center(35)
     + ""+ "6. print_unallocated [--o=filename.txt]".center(47))
    print("3. reallocate_person <employee_id> <new_room_name>".center(35) + " \t \t \t"+
          "7. print_room <room_name>".center(53))
    print("4. load_people <filename>".center(25) + " \t\t \t \t \t \t"+
          "8. save_state [--db=sqlite_database]".center(88))
    print("9.load_state <sqlite_database>".center(178))
    print(border)
    print("\n")
    print("OPTIONAL COMMANDS:".center(140))
    print("\n")

    print("1. help".center(140))
    print("2. quit".center(140))

    print(__doc__)
    print(border)


def save_state_on_interrupt():
    print("saving state.")
    Amity.save_state()


class AmityApplication(cmd.Cmd):
    cprint(figlet_format('AMITY', font='poison'), color='yellow', attrs=['bold'])

    prompt = "Amity -->"

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room  (office|living_space) <room_name>..."""
        print(arg)
        if arg["office"]:
            room_type = "office"
        if arg["living_space"]:
            room_type = "living_space"

        room_name = arg["<room_name>"]
        amity_object.create_room(room_type, room_name)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> (fellow|staff) [(y|n)] """

        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        if arg["fellow"]:
            role = "FELLOW"
        if arg["staff"]:
            role = "STAFF"
        if arg["y"]:
            wants_accommodation = "Y"
        elif arg["n"]:
            wants_accommodation = "N"
        else:
            wants_accommodation ="N"
        amity_object.add_person(first_name, last_name, role.upper(), wants_accommodation=wants_accommodation)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <filename>"""
        filename = arg["<filename>"]
        if os.path.exists(filename):
            amity_object.load_people(filename)
        else:
            print("File not found")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <first_name> <last_name> <new_room>"""
        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        full_name = first_name + " " + last_name
        new_room = arg["<new_room>"]

        if new_room.title() in amity_object.office:
            amity_object.reallocate_person(full_name.title(), new_room)
        elif new_room.title() in amity_object.living_space:
            amity_object.reallocate_person(full_name.title(), new_room.title())
        else:
            print('{0}is not a room in Amity' .format(new_room))

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room_name = arg["<room_name>"]
        amity_object.print_rooms(room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        filename = arg["--o"]

        amity_object.print_allocations(filename)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        filename = arg["--o"]

        amity_object.print_unallocated(filename)

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        db_name = arg["--db"]
        amity_object.save_state(db_name)

    @docopt_cmd
    def do_load_state(self, arg):
        '''Usage: load_state [--db=sqlite_database]'''
        db_name = arg["--db"]
        amity_object.load_state(db_name)

    @docopt_cmd
    def do_quit(self, arg):
        '''Usage: quit '''
        print("GOODBYE!!!")
        exit()


if __name__ == '__main__':
    introduction()
    try:
        AmityApplication().cmdloop()
    except KeyboardInterrupt:
        save_state_on_interrupt()



