import cmd
from database import Database

class dtree_interactive(cmd.Cmd):
    
    # database object for getting the information
    oDatabase = None
    strCurrentTable = None
    strCurrentTarget = None
        
    
    
    def __print_values(self, p_lValues):
        for i, entry in enumerate(p_lValues):
            strPre = "[{i}] ".format(i=i) 
            print strPre + entry
            
    def __select(self, p_lValues, p_strDest, p_strMessage):
        dtree_interactive.__print_values(p_lValues)
        index = input("{msg}: ".format(msg=p_strMessage))
        return p_lValues[index]
        
    def __show(self, p_lValues, p_strSelected): 
        for entry in p_lValues:
            strPre = "[X] " if (entry == p_strSelected) else "[ ] "
            print strPre + entry
        
    def do_show_tables(self, arg):
        """show_tables
        set the correct table"""
        dtree_interactive.__show(self,dtree_interactive.oDatabase.get_tables(), dtree_interactive.strCurrentTable)

    
    def do_select_table(self, arg):
        """select_tables
        select the table for the current session"""
        lTables = dtree_interactive.oDatabase.get_tables()
        index = dtree_interactive.__select(self, lTables, dtree_interactive.strCurrentTable, "Selected Table: ")
        dtree_interactive.strCurrentTable = lTables[index]
        print "Select Table is now: " + lTables[index]



    def do_show_target(self, arg):
        """show_target
        set the target column"""
        if dtree_interactive.strCurrentTable is None:
            print "Please select a Table first"
        else:
            dtree_interactive.__show(dtree_interactive.oDatabase.get_columns(), dtree_interactive.strCurrentTarget)
    

    
    def do_EOF(self, line):
        return True



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        strDB = sys.argv[1]
        dtree_interactive.oDatabase = Database(strDB)
        dtree_interactive().cmdloop()
    else:
        print "Please select a Database to operate on!"
        print "command: python dtree.py path/to/db"
        