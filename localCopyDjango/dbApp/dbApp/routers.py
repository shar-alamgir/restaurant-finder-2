class RevRouter:
    route_table = "Review"

    def db_for_read(self, model, **hints):
        if model._meta.db_table == "Review":
            return "reviews"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table == "Review":
            return "reviews"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.db_table == "Review" or
            obj2._meta.db_table == "Review"
        ):
            return True
        return None

    def allow_migrate(self, db, db_table, model_name=None, **hints):
        if db_table == "Review":
            return True
        return None
