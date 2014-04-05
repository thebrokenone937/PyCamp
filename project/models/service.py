from project.models.engine import *
#from project.models.core.drawings import Drawings

class Service(object):
    
    def getByColumn(self, **kwargs):
        
        result = session.query(self.Model).filter_by(**kwargs).first() 
        
        return result
    
    def save(self, model):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        
        session.add(model)
        session.commit()
        return model

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return session.query(self.Model).all()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return session.query(self.Model).get(id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        return session.query(self.Model).filter(self.Model.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return session.query(self.Model).filter_by(**kwargs)

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return session.query(self.Model).get_or_404(id)

    def update(self, model, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param **kwargs: update parameters
        """
        
        for k, v in kwargs.items():
            setattr(model, k, v)
        self.save(model)
        return model
    
    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.Model(**kwargs)

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.save(self.new(**kwargs))

    def delete(self, model):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        session.delete(model)
        session.commit()
