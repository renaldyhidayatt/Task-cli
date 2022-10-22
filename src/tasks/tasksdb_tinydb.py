import tinydb

"""
Database wrapper for tinydb for tasks project
"""


class TasksDB_TinyDB:
    """Wrapper class for TinyDB.

    The methods in this class need to match
    all database interaction classes.

    So far, this is:
    TasksDB_MongoDB found in tasksdb_pymongo.py.
    TasksDB_TinyDB found in tasksdb_tinydb.py.
    """

    def __init__(self, db_path) -> None:
        self._db = tinydb.TinyDB(db_path + "tasks_db.json")

    def add(self, task):
        """
        Adding a task dict to db
        """
        task_id = self._db.insert(task)
        task["id"] = task_id
        self._db.update(task, doc_ids=[task_id])

        return task_id

    def get(self, task_id):
        return self._db.get(doc_id=task_id)

    def list_tasks(self, owner=None):
        if owner is None:
            return self._db.all()
        else:
            return self._db.search(tinydb.Query().owner == owner)

    def count(self):
        """
        Return number of tasks in db
        """

        return len(self._db)

    def update(self, task_id, task):
        """
        Modify task in db with given task_id
        """
        self._db.update(task, doc_ids=[task_id])

    def delete(self, task_id):  # type (int) -> ()
        """Remove a task from db with given task_id."""
        self._db.remove(doc_ids=[task_id])

    def delete_all(self):
        """Remove all tasks from db."""
        self._db.purge()

    def unique_id(self):  # type () -> int
        """Return an integer that does not exist in the db."""
        i = 1
        while self._db.contains(doc_ids=[i]):
            i += 1
        return i

    def stop_tasks_db(self):
        """Disconnect from DB."""
        self._db.close()


def start_tasks_db(db_path):
    """Connect to db"""
    return TasksDB_TinyDB(db_path)
