class RevRouter:

    def db_for_read(self, model, **hints):
        # print(model._meta.db_table)
        if model._meta.db_table == "polls_restaurant_reviews":
            # print("Reading from review database")
            return "reviews"
        # print("Reading from default database")
        return None

    def db_for_write(self, model, **hints):
        # print(model._meta.db_table)
        if model._meta.db_table == "polls_restaurant_reviews":
            # print("Saving to review database")
            return "reviews"
        # print("Saving to default database")
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # print(obj1._meta.db_table)
        if (
            obj1._meta.db_table == "polls_restaurant_reviews" or
            obj2._meta.db_table == "polls_restaurant_reviews"
        ):
            return True
        return None

    def allow_migrate(self, db, db_table, model_name=None, **hints):
        if db_table == "polls_restaurant_reviews":
            return True
        return None
