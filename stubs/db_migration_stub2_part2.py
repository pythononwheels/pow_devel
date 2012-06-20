    table = None
        
    def up(self):
            #
            # here is where you define your table (Format see example below)
            # the columns below are just examples.
            # Remember that PoW automatically adds an id and a timestamp column (ID,TIMESTAMP)
        self.table = PowTable(self.table_name, self.__metadata__,
            
            Column('example_column', String(50))
            
            #Column('user_id', Integer, ForeignKey('users.id'))
        )
        self.create_table()
        #print CreateTable(self.table)
        
    def down(self):
        self.drop_table()