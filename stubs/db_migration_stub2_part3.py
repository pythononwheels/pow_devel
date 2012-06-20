            Column('acolumn', String(50)),
            Column('another_id', Integer, ForeignKey('another.id'))
        )
        self.table.create()
        
    def down(self):
        self.table = Table(self.table_name, PowObject.__metadata__, autoload = True )
        self.table.drop()
