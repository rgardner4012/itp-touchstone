from simple_term_menu import TerminalMenu

# Class Prompt for menu, one def for normal menu and one for using a dict as the options
class Prompt:
    def menu(options):
        main_menu = TerminalMenu(options)
        menu_entry_index = main_menu.show()
        selection = options[menu_entry_index]
        return selection
    
    def dict_menu(dict_options):
        selection = Prompt.menu(list(dict_options.keys()))
        selected_func = dict_options.get(selection)
        selected_func()
        return selection
