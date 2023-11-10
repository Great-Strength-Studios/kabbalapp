from ..models import *

class DomainRepository():
    ''' The Domain Repository is responsible for managing the domain models, repositories, and modules for an app.
    '''

    # TODO: Incorporate real domain model later.
    def get_domain_model(self, id: str) -> AppDomainModel:
        pass

    def get_domain_models(self, type: str = None) -> List[AppDomainModel]:
        pass

    def save_domain_model(self, domain_model: AppDomainModel) -> None:
        pass

    def get_repository(self, id: str) -> AppRepository:
        '''Returns the repository with the input id.

        :param id: The id of the repository to retrieve.
        :type id: str
        '''
        pass

    def save_repository(self, repository: AppRepository):
        '''Saves the input repository.

        :param repository: The repository to save.
        :type repository: class: `domain.models.AppRepository`
        '''
        pass