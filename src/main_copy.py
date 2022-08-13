"""TODO: sepearate code into python files and MVC model
"""

import os
import sqlite3
from flask import (Flask, render_template, request, jsonify, redirect, url_for)
from dataclasses import dataclass
from typing import Optional


APP = Flask("__main__")


@dataclass
class SchemaData:
    month: str
    day: str
    time: str
    server: str
    auth_type: str
    user: str
    ip_address: str
    port: int
    pubkey: Optional[str] = "NULL" 

    def add_to_database(self) -> tuple:     
        return (self.month, self.day, self.time, self.server, self.auth_type, self.user, self.ip_address, self.port, self.pubkey)
    
    def date_object(self) -> tuple:
        return (self.month, self.day)


@dataclass
class SchemaDataSearch:
	month: Optional[str] = "month NOT NULL" 
	day: Optional[str] = "day NOT NULL" 
	time: Optional[str] = "time NOT NULL" 
	server: Optional[str] = "server NOT NULL" 
	auth_type: Optional[str] = "auth_type NOT NULL" 
	user: Optional[str] = "user NOT NULL" 
	ip_address: Optional[str] = "ip_address NOT NULL" 
	port: Optional[int]  = "port NOT NULL"
	pubkey: Optional[str] = "pubkey NOT NULL" 

	def _month(self):
		if self.month != "month NOT NULL":
			return f"month='{self.month}'"
		else:
			return self.month

	def _day(self):
		if self.day != "day NOT NULL":
			return f"day='{self.day}'"
		else:
			return self.day

	def _time(self):
		if self.time != "time NOT NULL":
			return f"time='{self.time}'"
		else:
			return self.time

	def _server(self):
		if self.server != "server NOT NULL":
			return f"server='{self.server}'"
		else:
			return self.server

	def _auth_type(self):
		if self.auth_type != "auth_type NOT NULL":
			return f"auth_type='{self.auth_type}'"
		else:
			return self.auth_type

	def _user(self):
		if self.user != "user NOT NULL":
			return f"user='{self.user}'"
		else:
			return self.user

	def _ip_address(self):
		if self.ip_address != "ip_address NOT NULL":
			return f"ip_address='{self.ip_address}'"
		else:
			return self.ip_address

	def _port(self):
		if self.port != "port NOT NULL":
			return f"port='{self.port}'"
		else:
			return self.port
	
	def _pubkey(self):
		if self.pubkey != "pubkey NOT NULL":
			return f"pubkey='{self.pubkey}'"
		else:
			return self.pubkey
	
	def sql_search(self, table):
		return f"SELECT * from {table} WHERE {self._month()} AND {self._day()} AND {self._time()} AND {self._server()} AND {self._auth_type()} AND {self._user()} AND {self._ip_address()} AND {self._port()} AND {self._pubkey()}"


class TestingDatabase:

    def __init__(self) -> None:
        self.database_file = "testing.db"
        self.table_name = "testing"
        self.path =  os.getcwd()+"/"+self.database_file
        self.database_connection = sqlite3.connect(self.path)
        self.database_cursor = self.database_connection.cursor()
        self.database_init()
        return None

    def database_init(self) -> None:
        self.database_connection.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table_name}
                (month TEXT, day TEXT, time TEXT, server TEXT, auth_type TEXT, user TEXT, ip_address TEXT, port TEXT, pubkey TEXT)""")
        self.database_connection.commit()
        return None

    def adding_to_database(self, parameters) -> None:
        if parameters not in self.database_cursor.execute(f"SELECT * FROM {self.table_name}").fetchall():
            self.database_cursor.execute( f"INSERT OR IGNORE INTO {self.table_name} VALUES (?,?,?,?,?,?,?,?,?)", parameters)
            self.database_connection.commit()
        return None

    def return_individual(self, parameters) -> list[tuple]:
        return parameters in self.database_cursor.execute(f"SELECT * FROM {self.table_name}").fetchall()

    def return_database(self) -> list[tuple]:
         return self.database_cursor.execute(f"SELECT * FROM {self.table_name}").fetchall()

    def return_by_date(self, month, day) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE month='{month}' AND day='{day}'").fetchall()

    def return_by_server(self, server) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE server='{server}'").fetchall()

    def return_by_auth_type(self, auth_type) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE auth_type='{auth_type}'").fetchall()

    def return_by_user(self, user) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE user='{user}'").fetchall()

    def return_by_ip_address(self, ip_address) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE ip_address='{ip_address}'").fetchall()

    def return_by_port(self, port) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE port={port}").fetchall()

    def return_by_pubkey(self, pubkey) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE pubkey='{pubkey}'").fetchall()
    
    def return_by_accepted(self) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE auth_type ='Accepted publickey' OR auth_type ='Accepted password'").fetchall()
    
    def return_by_failed(self) -> list[tuple]:
        return self.database_cursor.execute(f"SELECT * FROM {self.table_name} WHERE auth_type ='Failed password'").fetchall()


class LogHandlerTesting:
    
    def __init__(self) -> None:
        self.log_path = "/var/log/auth.log"
        return None

    def index_check(self, log:list) -> list:
        if log[1] != '':
            log.insert(1, '')
            return log
        elif log[1] == '':
            return log

    def normal_log(self, log) -> tuple:
        log = log.split(" ")
        log = self.index_check(log)
        add_to_data_sort = SchemaData(
                        month=log[0],day=log[2], time=log[3], server=log[4], auth_type=" ".join(log[6:8]), 
                        user=log[9], ip_address=log[11], port=log[13])
        return add_to_data_sort.add_to_database()
    
    def invalid_user(self, log) -> tuple:
        log = log.split(" ")
        log = self.index_check(log)
        add_to_data_sort = SchemaData(
                    month=log[0], day=log[2],time=log[3], server=log[4], auth_type=" ".join(log[6:8]),
                    user=log[11], ip_address=log[13], port=log[15])
        return add_to_data_sort.add_to_database()

    def pubkey_log(self, log) -> tuple:
        log = log.split(" ")
        log = self.index_check(log)
        add_to_data_sort = SchemaData(
                    month=log[0], day=log[2],time=log[3], server=log[4], auth_type=" ".join(log[6:8]),
                    user=log[9], ip_address=log[11], port=log[13], pubkey=" ".join(log[15:18]))
        return add_to_data_sort.add_to_database()

    def _testing_logs(self, log:str) -> tuple: 
        """Reads the log file and and saves the ssh logs based on content of the log"""
        if "Accepted password" in log or "Accepted publickey" in log:
            if "Accepted publickey" in log:
                return self.pubkey_log(log)
            else:
                return self.normal_log(log)

        elif "Failed password" in log or "Failed publickey" in log:
            if "invalid user" in log:
                return self.invalid_user(log)
            else:
                return self.normal_log(log)


class LogHandler:

    def __init__(self) -> None:
        self.log_path = "/var/log/auth.log"
        return None

    def index_check(self, log:list) -> list:
        if log[1] != '':
            log.insert(1, '')
            return log
        elif log[1] == '':
            return log

    def normal_log(self, log) -> tuple:
        log = log.split(" ")
        log = self.index_check(log)
        add_to_data_sort = SchemaData(
                        month=log[0],day=log[2], time=log[3], server=log[4], auth_type=" ".join(log[6:8]), 
                        user=log[9], ip_address=log[11], port=log[13])
        return add_to_data_sort.add_to_database()
    
    def invalid_user(self, log) -> tuple:
        log = log.split(" ")
        log = self.index_check(log)
        add_to_data_sort = SchemaData(
                    month=log[0], day=log[2],time=log[3], server=log[4], auth_type=" ".join(log[6:8]),
                    user=log[11], ip_address=log[13], port=log[15])
        return add_to_data_sort.add_to_database()

    def pubkey_log(self, log) -> tuple:
        log = log.split(" ")
        log = self.index_check(log)
        add_to_data_sort = SchemaData(
                    month=log[0], day=log[2],time=log[3], server=log[4], auth_type=" ".join(log[6:8]),
                    user=log[9], ip_address=log[11], port=log[13], pubkey=" ".join(log[15:18]))
        return add_to_data_sort.add_to_database()


    def main(self) -> None: 
        """Reads the log file and and saves the ssh logs based on content of the log
        """
        with open(self.log_path, "r") as file:
            lines = file.readlines()
        
        for log in lines:
            if "Accepted password" in log or "Accepted publickey" in log:
                if "Accepted publickey" in log:
                    TestingDatabase().adding_to_database(self.pubkey_log(log))
                else:
                    TestingDatabase().adding_to_database(self.normal_log(log))

            elif "Failed password" in log or "Failed publickey" in log:
                if "invalid user" in log:
                    TestingDatabase().adding_to_database(self.invalid_user(log))
                else:
                    TestingDatabase().adding_to_database(self.normal_log(log))
        return None


class Display:


    @APP.route("/", methods=['GET', "POST"])
    def index():
        """Connects to the next available port.
        """
        page = render_template("index.html", 
                    ssh_log_accepted = TestingDatabase().return_by_accepted()[::-1],
                    ssh_log_failed = TestingDatabase().return_by_failed()[::-1],
                    title = "home pages")
        if request.method == "POST":
            LogHandler().main()
            return redirect(url_for('index'))
        else:
            return page

    @APP.route("/docs", methods=['GET', "POST"])
    def docs_page():
        page = render_template("docs.html", 
                    ssh_log_accepted = TestingDatabase().return_by_accepted()[::-1],
                    ssh_log_failed = TestingDatabase().return_by_failed()[::-1],
                    title = "docs")
        if request.method == "POST":
            LogHandler().main()
            return redirect(url_for('docs_page'))
        else:
            return page

    @APP.route("/accepted", methods=['GET', "POST"])
    def accepted_page():

        page = render_template("accepted.html", 
                    ssh_log_accepted = TestingDatabase().return_by_accepted()[::-1],
                    ssh_log_failed = TestingDatabase().return_by_failed()[::-1],
                    title = "accepted logins")
        if request.method == "POST":
            LogHandler().main()
            return redirect(url_for('accepted_page'))
        else:
            return page

    @APP.route("/failed", methods=['GET', "POST"])
    def failed_page():
        page = render_template("failed.html", 
                    ssh_log_accepted = TestingDatabase().return_by_accepted()[::-1],
                    ssh_log_failed = TestingDatabase().return_by_failed()[::-1],
                    title = "failed logins")
        if request.method == "POST":
            LogHandler().main()
            return redirect(url_for('accepted_page'))
        else:
            return page

    @APP.route("/api", methods=['GET', "POST"])
    def api_page():
        page = render_template("api.html", 
                    ssh_log_accepted = TestingDatabase().return_by_accepted()[::-1],
                    ssh_log_failed = TestingDatabase().return_by_failed()[::-1],
                    title = "api")
        if request.method == "POST":
            LogHandler().main()
            return redirect(url_for('accepted_page'))
        else:
            return page


class API:

    @APP.route("/api/v2/get/all_accepted",  methods=['GET'])
    def get_all_accepted():
        data = TestingDatabase().return_by_accepted()[::-1]
        return jsonify(data)
    
    @APP.route("/api/v2/get/last_accepted",  methods=['GET'])
    def get_last_accepted():
        data = TestingDatabase().return_by_accepted()[-1][::-1]
        return jsonify(data)
    
    @APP.route("/api/v2/get/all_failed",  methods=['GET'])
    def get_all_failed():
        data = TestingDatabase().return_by_failed()[::-1]
        return jsonify(data)
    
    @APP.route("/api/v2/get/last_failed",  methods=['GET'])
    def get_last_failed():
        data = TestingDatabase().return_by_failed()[-1][::-1]
        return jsonify(data)
    
    @APP.route("/api/v2/get/help",  methods=['GET'])
    def get_help():
        data = ["/api/v2/get/last_failed", "/api/v2/get/all_failed", 
                "/api/v2/get/last_accepted", "/api/v2/get/all_accepted"]
        return jsonify(data)


if __name__ == "__main__":
    LogHandler().main()
    APP.run(debug=True, host='0.0.0.0', port=5000)
