import os

def write_text_file(ads,file_name):
    stream = open(file_name, "w")
    for ad in ads:
        stream.write(" price: " + str(ad[1]) + " surface: " + str(ad[2]) + os.linesep)
        stream.write(ad[0] + os.linesep)
    stream.close()

def write_csv_file(ads,file_name):
    stream = open(file_name, "w")
    for ad in ads:
        stream.write(ad[0] + "," + ad[1] + "," + ad[2] + "," + ad[3]+ os.linesep)
    stream.close() 