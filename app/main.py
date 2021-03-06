import os
from pwd import getpwnam  


import cherrypy
from cherrypy.process.plugins import DropPrivileges, PIDFile, Daemonizer

from .server import FilePusher
from .operations import ServerOperations
from .database.tools import Setup

class Main():
    def __init__(self):
        path = os.path.abspath(os.path.dirname(__file__))
        self.database = path+"/../data/filepusher.db"
        self.files = path+"/../data/files"
        self.config = path+"/../server.conf"
        self.pid = path+"/../server.pid"
        # OS specific
        self.uid = getpwnam('filepusher').pw_uid
        self.gid = getpwnam('filepusher').pw_gid

    def run(self):
        if os.path.isfile(self.database):
            print("Importing server configuration")
            srvOp = ServerOperations(self.database,self.files)
            cherrypy.config.update(self.config)
            print("Starting server instance")
            Daemonizer(cherrypy.engine).subscribe()
            DropPrivileges(cherrypy.engine, uid=self.uid, gid=self.gid).subscribe()
            PIDFile(cherrypy.engine, self.pid).subscribe()
            cherrypy.quickstart(FilePusher(srvOp),'/',self.config)
        else:
            print("Can't run! Missing database file.")
            print("Try 'python3 run.py setup'")

    def setup(self):
        # Create database if it does not exists
        if not os.path.isfile(self.database):
            print("Creating database; provide ROOT user:")
            username = str(input("username: "))
            password = str(input("password: "))
            Setup(self.database).createRoot(username,password)
            print("Database created ("+self.database+")")
        else:
            print("Database EXIST! Do you want to OVERWRITE!")
            correctInput = False
            while not correctInput:
                valid = ["y","n"]
                answer = str(input("(y/n): "))
                if answer in valid:
                    correctInput = True
                    if answer == "y":
                        print("Too bad! It's not implemented yet")
                    
                    
