import c45
from database import Database
from diff import compare
from table import create_from_csv


db = Database()
db.add_table("system", create_from_csv("/home/julesy/Workspace/qfin_system.csv", p_strDelimiter=";"))
db.add_table("systemb", create_from_csv("/home/julesy/Workspace/qfin_system.csv", p_strDelimiter=";"))
db.add_table("trade", create_from_csv("/home/julesy/Workspace/qfin_trade.csv", p_strDelimiter=";"))
db.add_table("instrument", create_from_csv("/home/julesy/Workspace/qfin_instrument.csv", p_strDelimiter=";"))
db.add_table("joined", db.join("system", "systemb", [('Trade Nr', 'Trade Nr')], p_strType="inner"))
db.add_table("joined_trade", db.join("joined", "trade", [('Trade Nr', 'TradeNr')], p_strType="left"))


#db.add_table("joined_all", db.join("joined_trade", "instrument", [('Intrument', 'insaddr')], p_strType="left"))

tbl = db.get_table("joined_trade")
tbl.add_column("cls_Nominal", compare(tbl, "Nominal", "Nominal_"))
c45.start(tbl, "cls_Nominal")

#print len(db.get_table("joined_all").get_columns()), "columns"
#print db.get_table("joined_all").get_columns()

#db.get_table("joined_trade").pretty_print()