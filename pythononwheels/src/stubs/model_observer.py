#
# Observer class for {{model_class_name}} model
# See Oberver Pattern Rails: https://api.rubyonrails.org/v3.1/classes/ActiveRecord/Observer.html
# 

class {{model_class_name}}Observer:
    """
        You can add callbacks for the following events:
        before & after:  upsert, validation, delete.
        Method Names:
            before_upsert
            after_upsert
            before_validation
            ... and so on
    """    
    #
    # example observer method:
    #
    def before_upsert(self, model):
        """
            Do something with your {{model_class_name}} Model here
        """
        # you could e.g. send an email if a new Post or User was created 
        # this is the right place to do it. Not in the model itself.
        # To separate business logic and Model behaviour.
        print(" OBSERVER: upserted  {{model_class_name}} ;(")
        print(model)
    
    #def after_upsert(self, model):
    #    """
    #        Do something with your {{model_class_name}} Model here
    #    """
    #    # you could e.g. send an email if a new Post or User was created 
    #    # this is the right place to do it. Not in the model itself.
    #    # To separate business logic and Model behaviour.
    #    print(" OBSERVER: upserted  {{model_class_name}} ;(")
    #    print(model)

    #
    # uncomment observers below. But be aware that obervers are called for every 
    # model event .... can be oberhead .. 
    #
    #def before_delete(self, model):
    #    """
    #        Do something with your {{model_class_name}} Model here
    #    """
    #    print(" You killed this nice model {{model_class_name}} ;(")
    #    print(model)

    #def after_delete(self, model):
    #    """
    #        Do something with your {{model_class_name}} Model here
    #    """
    #    print(" You killed this nice model {{model_class_name}} ;(")
    #    print(model)
    
    #def before_validate(self, validator):
    #    """
    #        Do something with your {{model_class_name}} Model and cerberus validator
    #    """
    #    # 
    #    pass
    
    #def after_validate(self, validation_result):
    #    """
    #        Do something with your {{model_class_name}} Model and cerberus validation result
    #    """
    #    # you could e.g. send an email if a new Post or User was created 
    #    pass