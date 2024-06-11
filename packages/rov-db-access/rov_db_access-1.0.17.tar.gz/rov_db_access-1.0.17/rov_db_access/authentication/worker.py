from sqlalchemy import select

from rov_db_access.config.db_utils import init_db_engine
from rov_db_access.config.settings import Settings
from sqlalchemy.orm import Session
from rov_db_access.authentication.models import User

settings = Settings()


class AuthenticationWorker:

    def __init__(self) -> None:

        self.engine = init_db_engine(
            settings.db_rov_gis_user,
            settings.db_rov_gis_password,
            settings.db_rov_gis_host,
            settings.db_rov_gis_port,
            settings.db_rov_gis_database
        )

    def get_user_by_username(self, username: str):
        with Session(self.engine) as session:
            user_query = (
                select(User)
                .where(User.username == username)
                .limit(1)
            )
            user = session.scalar(user_query)
            roles = user.roles
            return {"user": user, "user_roles": roles}

    def create_user(self, username: str, password: str):
        with Session(self.engine) as session:
            new_user = User(username=username, password=password)
            session.add(new_user)
            session.commit()
            return new_user

    def load_user(self, id: str):
        with Session(self.engine) as session:
            user = session.get(User, id)
            if user is None:
                print(f'No user with id {id} found!')
                return False
            return {
                "id": user.id,
                "username": user.username,
                "logged_at": user.logged_at,
                "organization_id": user.organization_id
            }

    def load_users_by_org(self, organization_id: str):
        with Session(self.engine) as session:
            query_users = (
                select(User)
                .where(User.organization_id == organization_id)
                .order_by(User.id)
            )
            users = session.scalars(query_users).all()
            if users is None or len(users) == 0:
                return []
            else:
                print(f'Users found!: {len(users)} results')
                results = []
                for user in users:
                    results.append({
                        "id": user.id,
                        "username": user.username,
                        "logged_at": user.logged_at,
                        "organization_id": user.organization_id
                    })
                return results
