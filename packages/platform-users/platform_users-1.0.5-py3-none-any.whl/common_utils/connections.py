#Python Imports
import threading

#Django Imports
from django.db import connections

#Third-Party Imports

#Project-Specific Imports
from common_utils.logger import get_logger

#Relative Import



class ConnectionManager:
    """Database connection manager"""
    logger = get_logger('ConnectionManager')
    def connect_default_db(self):
        """Connect thread to default database"""
        try:
            self._set_db_for_thread('default')
            self.logger.info("Thread connected to default database")
        except Exception as e:
            self.logger.error("Error connecting to default database: %s", e)
            raise e
            
    def connect_tenant_db(self, db_alias):
        """Connect thread to tenant database"""
        try:
            self._set_db_for_thread(db_alias)
            self.logger.info("Thread connected to tenant %s database", db_alias)  
        except Exception as e:
            self.logger.error("Error connecting to tenant %s database: %s", db_alias, e)
            raise e
        
    def _set_db_for_thread(self, db_alias):
        setattr(threading.current_thread(), 'db_alias', db_alias)
        
    def close_connections(self):
        connections.close_all()
        