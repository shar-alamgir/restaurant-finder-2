class RevRouter:

    def db_for_read(self, model, **hints):
        # print(model._meta.db_table)
        if model._meta.db_table == "polls_reviews":
            return "reviews"
        return None

    def db_for_write(self, model, **hints):
        # print(model._meta.db_table)
        if model._meta.db_table == "polls_reviews":
            print("Saving to review database")
            return "reviews"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # print(obj1._meta.db_table)
        if (
            obj1._meta.db_table == "polls_reviews" or
            obj2._meta.db_table == "polls_reviews"
        ):
            return True
        return None

    def allow_migrate(self, db, db_table, model_name=None, **hints):
        if db_table == "polls_reviews":
            return True
        return None
