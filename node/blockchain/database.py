import sqlite3

class Collection_stub:
    """
    Collection class for storing documents(blocks in this case)
    """
    def __init__(self):
        self.collection = []

    def find(self, query):
        for document in self.collection:
            yield document

    def count_documents(self, query):
        return len(self.collection)

    def insert_one(self, document):
        self.collection.append(document)

    def delete_one(self):
        raise NotImplementedError

    def delete_many(self, query):
        for document in self.collection:
            if (self.run_query(query, document)):
                self.collection.remove(document)

    def remove(self):
        raise NotImplementedError

    def find_one(self, query):
        for document in self.collection:
            if (self.run_query(query, document)):
                return document
    
    def run_query(self, query, document):
        # returns if the document matches the query
        for attribute, condition in query.items():
            try:
                if (type(condition)!="dict"):
                    return document[attribute] == query[attribute]
                if (condition.get("$gt",None)):
                    condition_val = condition.get("$gt",None)
                    return document[attribute] > condition_val
            except:
                print("Error running query")

    