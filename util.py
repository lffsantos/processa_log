__author__ = 'lucas'

def read_file(file):

    with open(file, 'r') as line:
        for l in line:
            print(l[l.index("userid=")+7:].replace("\"",""))
            generate_token(l[l.index("userid=")+7:].replace("\"",""))


def generate_token(userid, number_host):
    return str(userid)/number_host


def write_log(file_path):
    file = open(file_path,"w")
    file.write("oi\n")
    file.close()

# file_path = "1"
# write_log(file_path)
# # read_file("logs/log.txt")
