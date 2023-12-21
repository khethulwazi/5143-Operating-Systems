# Filesystem Starter Class
from sqliteCrud import SqliteCrud
from prettytable import PrettyTable
import os
# rich.progress import track
import math

def convert_size(size_bytes): 
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

class FileSystem:
    # db_name =   "testfilesystem.sqlite"       #"filesystem.sqlite"
    # crud = SQLiteCrud(db_name)
    # cwd = "/home/user"
    # pid = 0
    # cwdid = 0
    def __init__(self,db_name=None):
        if not db_name:
            self.db_name = "filesystem.sqlite"
        else:
            self.db_name = db_name
        self.crud = SqliteCrud(self.db_name)
        self.cwd = "/home/user"
        self.cwdid = 6
        self.pid = 0

    # def __getFileId(self,**kwargs):
    #     """ Find a file id using current location + name
    #     """
    #     pass
    
    def mkdir(self,table_name, **kwargs):
        data = kwargs.get("kwargs")
        #data = data
        print(data)
        self.crud.insert_data(table_name,data)

    def rm(self,conn, table_name, **kwargs):
        flags,data = kwargs.get("kwargs")
        if 'rf' in flags:
            #cascadingDelete
            conn.cursor.execute(f"SELECT * FROM {table_name} WHERE name = {data} AND type = 'folder';")
            table_info = conn.cursor.fetchall()
            conn.cursor.execute(f"SELECT * FROM {table_name} WHERE pid = {table_info[0]};")
            child_info = conn.cursor.fetchall()
            for row in child_info:
                self.crud.delete_data(self,table_name,row)
            self.crud.delete_data(self,table_name,table_info)
        else:
            conn.cursor.execute(f"SELECT EXISTS(SELECT * FROM {table_name} WHERE name = {data} AND type = 'file');")
            if(conn.cursor.fetchall()):
                self.crud.delete_data(self,table_name,data)
    
    def rmdir(self,conn,table_name,**kwargs):
            data = kwargs.get("kwargs")
            conn.cursor.execute(f"SELECT * FROM {table_name} WHERE name = '{data}';")
            table_info = conn.cursor.fetchall()
            #check if the directory is empty
            #query to check that no parent ID exists with the same directory ID
            conn.cursor.execute(f"SELECT * FROM {table_name} WHERE pid = {table_info[0][0]};")
            #returns true/false
            if(conn.cursor.fetchall()):
                print("Error: Folder is not empty")
                print(conn.cursor.fetchall())
            else:
                #self.crud.delete_data(self,table_name,data)
                conn.cursor.execute(f"SELECT * FROM {table_name} WHERE id = {table_info[0][0]};")
                print(conn.cursor.fetchall())

    def wc(self,conn, table_name,**kwargs):

        infileName = kwargs.get('params')[-1]
        conn.cursor.execute(f"SELECT EXISTS(SELECT * FROM {table_name} WHERE name = {infileName} AND type = 'file');")
        if(conn.cursor.fetchall()):   
            # creating variable to store the
            # number of words
            #number_of_words = 0
            lineCount = 0
            byteCount = 0

            with open(infileName,'r') as file:
                #return the absolute path of the file
                #path = os.path.abspath(infileName)
                path = self.pwd()
                #counts the bytes in the file
                byteCount = os.path.getsize(path)
                print("Path: ", path)
                print("byteCount: ", byteCount)
                # Reading the content of the file
                # using the read() function and storing
                # them in a new variable
                data = file.read()

                # Splitting the data into separate lines
                # using the splitlines() function
                lineCount = len(data.splitlines())
                print("lineCount = ", lineCount)
                # Splitting the data into separate words
                # using the split() function
                words = len(data.split())
                print("words = ", words)
                # Printing total number of words
                print(lineCount, words, byteCount, infileName)  

    def list(self, conn, table_name, **kwargs):
        """ List the files and folders in current directory
        """
        flags = kwargs.get('flags')
        print(flags)
        if 'l' in flags:
            if 'a' in flags:
                conn.cursor.execute(f"SELECT * FROM {table_name} WHERE pid = {self.cwdid};")
            else:
                conn.cursor.execute(f"SELECT * FROM {table_name} WHERE pid = {self.cwdid} AND NOT name like '.%';")
            table_info = conn.cursor.fetchall()
            #table_data = str(table_info).strip('[]').strip('()').strip('\' \'').split(',')
            updatedTable_info = ([])
            for row in table_info:
                table_data = list(row)
                for item in row:
                    if item == row[5]:
                        table_data[5] = convert_size(float(item))
                updatedTable_info.append(tuple(table_data))       
            
            table = PrettyTable()
            table.field_names = [desc[0] for desc in conn.cursor.description]
            if 'h' in flags:
                table.add_rows(updatedTable_info)
            else:
                table.add_rows(table_info)
            print("\n$ls -", flags," ./")
            print(table)
            print(self.cwd)
            print("current directory ID: ", self.cwdid)
            print("\n")
            return
        elif 'a' in flags:
            conn.cursor.execute(f"SELECT name FROM {table_name} WHERE pid = {self.cwdid} AND NOT name like '.%';")
            table_info = conn.cursor.fetchall()
            table = PrettyTable()
            table.field_names = [desc[0] for desc in conn.cursor.description]
            table.add_rows(table_info)
            print(table)
            print(self.cwd)
            print("current directory ID: ", self.cwdid)
            print("\n")
            return
        else:
            conn.cursor.execute(f"SELECT * FROM {table_name} WHERE pid = {self.cwdid};")
            table_info = conn.cursor.fetchall()
            table_data = []
            for row in table_info:
                table_data.append(row[2])
            print(*table_data)
            #table = PrettyTable()
            #table.field_names = [desc[0] for desc in conn.cursor.description]
            #table.add_rows(table_info)
            #print(table)
            #print(*table_info)
            print(self.cwd)
            print("current directory ID: ", self.cwdid)
            print("\n")
            return

    def chmod(self, conn, table_name, **kwargs):
        """ Change the permissions of a file
            1) will need the file / folder id
            2) select permissions from the table where that id exists
            3) 
        Params:
            id (int) :  id of file or folder
            permission (string) : +x -x 777 644
            if its a triple just overwrite or update table 

        Example:
            +x 
            p = 'rw-r-----'
            p[2] = x
            p[5] = x
            p[8] = x
        """
        fileId,permissions = kwargs.get('params')   
        conn.cursor.execute(f"SELECT * FROM {table_name} WHERE id = {fileId};")
        item_info = conn.cursor.fetchall()
        data = list(item_info)
        if '+x' in permissions:
            p = data[9]
            p[2] = 'x'
            p[5] = 'x'
            p[8] = 'x'
            data[9] = p
        elif '-x' in permissions:
            p = data[9]
            p[2] = 'x'
            p[5] = 'x'
            p[8] = 'x'
            data[9] = p
        elif '777' in permissions:
            p = 'rwxrwxrwx'
            data[9] = p
        elif '455' in permissions:
            p = 'r-xr-xr-x'
            data[9] = p
        elif '655' in permissions:
            p = 'rw-r-xr-x'
            data[9] = p

    def cd(self, conn, table_name,params):
        """
        cd .. = move to parent directory from cwd
        cd ../.. 
        cd /root  (need to find id of that folder, and set cwd )
        cd homework/english (involves a check to make sure folder exist)
        cd -la Folder1{'cmd': 'cd', 'params': ['Folder1'], 'flags': ['la'], 'directives': []}
        """
        path = params['params'][0]
        flags = ''.join(params['flags'])

        print("flags = ", flags)
        print("path = ",path)
        print(table_name)
        #print()

        dirs = path.strip('[]').strip('\' \'').split('/')

        if '..' in path:
            print("\n$cd ", path)
            for dir in dirs:
                print(self.pid)
                data = ([])
                if self.pid == 0:
                    conn.cursor.execute(f"SELECT * FROM {table_name} WHERE pid = {self.pid};")
                    parent_info = conn.cursor.fetchall()
                    for row in parent_info:
                        parent_data = list(row)      
                        data.append(tuple(parent_data)) 
                    self.pid = data[0][1]
                    self.cwdid = data[0][1]
                    table = PrettyTable()
                    table.field_names = [desc[0] for desc in conn.cursor.description]
                    table.add_rows(parent_info)
                    print(table)
                    self.cwd = 'home/user'
                    print("directory = ", self.cwd)
                    print("ParentID = ", self.pid)
                    print("New cwdID = ", self.cwdid)
                    return
                else:
                    conn.cursor.execute(f"SELECT * FROM {table_name} WHERE id = {self.pid};")
                    parent_info = conn.cursor.fetchall()
                    for row in parent_info:
                        parent_data = list(row)       

                        data.append(tuple(parent_data))
                    self.pid = data[0][1]
                    self.cwdid = data[0][0]
                    conn.cursor.execute(f"SELECT * FROM {table_name} WHERE pid = {self.cwdid};")
                    parent_data = conn.cursor.fetchall()
                    table = PrettyTable()
                    table.field_names = [desc[0] for desc in conn.cursor.description]
                    table.add_rows(parent_data)
                    print(table)
                    self.cwd = self.cwd[:-len(data[0][2])]
                    print("directory = ", self.cwd)
                    print("ParentID = ", self.pid)
                    print("New cwdID = ", self.cwdid)
        else:
            #Check if dir is a directory/exists
            for dir in dirs:
                print(dir)

                conn.cursor.execute(f"SELECT EXISTS(SELECT name FROM {table_name} WHERE name = '{dir}');")      
                if conn.cursor.fetchone():
                    conn.cursor.execute(f"SELECT type FROM {table_name} WHERE name = '{dir}';")
                    filedata = str(conn.cursor.fetchone()).strip('()').strip(',').strip("\' \'")
                    fileType = filedata
                    #print(fileType)
                    if not fileType == 'folder':
                        print("Directory ", path, " does not exist")
                        return
                else:
                    print("Directory ", path, "/ does not exist!")
                    return                 
            directory = dirs[-1]
            print("\n$cd ", path,"...")
            conn.cursor.execute(f"SELECT * FROM {table_name} WHERE name = '{directory}';")
            table_info = conn.cursor.fetchall()
            table_data = str(table_info).strip('[]').strip('()').split(',')
            data = []
            for d in table_data:
                data.append(d)
            table = PrettyTable()
            table.field_names = [desc[0] for desc in conn.cursor.description]
            table.add_rows(table_info)
            print(table)
            self.cwd += '/' + path
            self.cwdid = data[0]
            self.pid = data[1]
            print("directory = ", self.cwd)
            print("ParentID = ", self.pid)
            print("New cwdID = ", self.cwdid)
            print("\n")

    def getCWD(self):
        return self.cwd

    def pwd(self):
        path = self.getCWD()
        print(path)  

    def showTable(self,table_name):
        print(self.crud.formatted_print(table_name))

# Example usage:
if __name__ == "__main__":
    """
    THIS USAGE REALLY JUST SHOWS THE SqliteCRUD CLASS BUT WITH A FILESYSTEM THEME.
    WILL FIX AS WE ADD FUNCTIONALITY INTO THE FileSystem CLASS ABOVE
    SORRY FOR ALL CAPS DIDN'T WANT YOU TO MISS    
    """
    f = FileSystem()

    # Define table schema
    table_name = "files_data"
    columns = ["id INTEGER PRIMARY KEY", "pid INTEGER", "name TEXT", "created_date TEXT", "modified_date TEXT", "size REAL","type TEXT","owner TEXT","groop TEXT","permissions TEXT"]
    # Load table
    test_data = [
        (1, 0, 'Folder1', '2023-09-25 10:00:00', '2023-09-25 10:00:00', 0.0, 'folder', 'user1', 'group1', 'rwxr-xr-x'),
        (2, 1, 'File1.txt', '2023-09-25 10:15:00', '2023-09-25 10:15:00', 1024.5, 'file', 'user1', 'group1', 'rw-r--r--'),
        (3, 1, 'File2.txt', '2023-09-25 10:30:00', '2023-09-25 10:30:00', 512.0, 'file', 'user2', 'group2', 'rw-rw-r--'),
        (4, 0, 'Folder2', '2023-09-25 11:00:00', '2023-09-25 11:00:00', 0.0, 'folder', 'user2', 'group2', 'rwxr-xr--'),
        (5, 4, 'File3.txt', '2023-09-25 11:15:00', '2023-09-25 11:15:00', 2048.75, 'file', 'user3', 'group3', 'rw-r--r--'),
        (6, 4, 'File4.txt', '2023-09-25 11:30:00', '2023-09-25 11:30:00', 4096.0, 'file', 'user3', 'group3', 'rw-r--r--'),
        (7, 0, 'Folder3', '2023-09-25 12:00:00', '2023-09-25 12:00:00', 0.0, 'folder', 'user4', 'group4', 'rwxr-x---'),
        (8, 7, 'File5.txt', '2023-09-25 12:15:00', '2023-09-25 12:15:00', 8192.0, 'file', 'user4', 'group4', 'rw-------'),
        (9, 0, 'Folder4', '2023-09-25 13:00:00', '2023-09-25 13:00:00', 0.0, 'folder', 'user5', 'group5', 'rwxr-xr-x'),
        (10, 9, 'File6.txt', '2023-09-25 13:15:00', '2023-09-25 13:15:00', 3072.25, 'file', 'user5', 'group5', 'rwxr-xr--'),
        (11, 1, 'Folder5', '2023-09-25 13:00:00', '2023-09-25 13:00:00', 0.0, 'folder', 'user5', 'group5', 'rwxr-xr-x'),
    ]
    conn = SqliteCrud("zzztop.sqlite")

    conn.drop_table(table_name)

    conn.create_table(table_name, columns)
    print(conn.describe_table(table_name))

    for row in test_data:
        conn.insert_data(table_name, row)

    #print(conn.formatted_print(table_name))
    #print(f.cwdid)
    f.showTable(f,table_name)
    f.pwd(f)
    f.cd(f, table_name,kwargs='Folder1/Folder5')
    f.list(f,table_name, kwargs='lah')
    f.pwd(f)
    f.cd(f, table_name,kwargs='../..')  
    f.list(f,table_name, kwargs='lah')
    f.pwd(f)
    data = (12,0,'Bananas','2023-11-14 10:00:00','2023-11-14 10:00:00',0,'folder','user1','group6','rwxrwxrwx')
    f.mkdir(f,table_name,kwargs=data)
    f.showTable(f,table_name)
    f.list(f,table_name, kwargs='')
    f.rmdir(f,table_name,kwargs='Bananas')
    f.list(f,table_name, kwargs='lah')
    #f.cd(f, table_name,kwargs='Folder1')
    #data = ('rf','Folder5')
    #f.rm(f,table_name,kwargs=data)

