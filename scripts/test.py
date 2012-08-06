import generate_migration
import sys,os

inl = "firstname String(50), lastname String(50), email String(100)"
inf = open(os.path.normpath("./stubs/partials/db_migration_stub2_part2.py"))
instr = inf.read()
print generate_migration.transform_col_defs(instr, inl)