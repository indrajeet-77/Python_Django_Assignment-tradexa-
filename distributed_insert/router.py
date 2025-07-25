class DistributedRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'distributed_insert':
            if model.__name__ == 'User':
                return 'users'
            elif model.__name__ == 'Product':
                return 'products'
            elif model.__name__ == 'Order':
                return 'orders'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label != 'distributed_insert':
            return None
        if db == 'users':
            return model_name == 'user'
        elif db == 'products':
            return model_name == 'product'
        elif db == 'orders':
            return model_name == 'order'
        return None
