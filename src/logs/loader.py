import pathlib

class Config:
    log_path = "/var/log/auth.log"

class Handler:

    def check_file() -> bool:
        if pathlib.Path(Config.log_path).exists(): return True
        else: return False

    def load_logs():
        if Handler.check_file():
            with open(Config.log_path, "r") as file:
                lines = file.readlines()
                return lines
        else: return None

    def process_log_line(log_line: str) -> list[str]:
        log = log_line.split(" ")
        if log[1] != "":
            log.insert(1, "") 
            return log
        return log

    # def index_check(self, log:list) -> list:
    #     if log[1] != '':
    #         log.insert(1, '')
    #         return log
    #     elif log[1] == '':
    #         return log

    # def normal_log(self, log) -> tuple:
    #     log = log.split(" ")
    #     log = self.index_check(log)
    #     add_to_data_sort = SchemaData(
    #                     month=log[0],day=log[2], time=log[3], server=log[4], auth_type=" ".join(log[6:8]), 
    #                     user=log[9], ip_address=log[11], port=log[13])
    #     return add_to_data_sort.add_to_database()
    
    # def invalid_user(self, log) -> tuple:
    #     log = log.split(" ")
    #     log = self.index_check(log)
    #     add_to_data_sort = SchemaData(
    #                 month=log[0], day=log[2],time=log[3], server=log[4], auth_type=" ".join(log[6:8]),
    #                 user=log[11], ip_address=log[13], port=log[15])
    #     return add_to_data_sort.add_to_database()

    # def pubkey_log(self, log) -> tuple:
    #     log = log.split(" ")
    #     log = self.index_check(log)
    #     add_to_data_sort = SchemaData(
    #                 month=log[0], day=log[2],time=log[3], server=log[4], auth_type=" ".join(log[6:8]),
    #                 user=log[9], ip_address=log[11], port=log[13], pubkey=" ".join(log[15:18]))
    #     return add_to_data_sort.add_to_database()


    # def main(self) -> None: 
    #     """Reads the log file and and saves the ssh logs based on content of the log
    #     """
    #     with open(self.log_path, "r") as file:
    #         lines = file.readlines()
        
    #     for log in lines:
    #         if "Accepted password" in log or "Accepted publickey" in log:
    #             if "Accepted publickey" in log:
    #                 TestingDatabase().adding_to_database(self.pubkey_log(log))
    #             else:
    #                 TestingDatabase().adding_to_database(self.normal_log(log))

    #         elif "Failed password" in log or "Failed publickey" in log:
    #             if "invalid user" in log:
    #                 TestingDatabase().adding_to_database(self.invalid_user(log))
    #             else:
    #                 TestingDatabase().adding_to_database(self.normal_log(log))
    #     return None

if __name__ == "__main__":
    Handler.check_file()