import os

def write_text_file(ads,file_name):
    stream = open(file_name, "w")
    for ad in ads:
        stream.write(" price: " + str(ad[1]) + " surface: " + str(ad[2]) + os.linesep)
        stream.write(ad[0] + os.linesep)
    stream.close()

def write_csv_file(ads,file_name):
    stream = open(file_name, "w")
    stream.write("surface,price,prix/m2,url" + os.linesep)
    for ad in ads:
        stream.write(str(ad[2]) + "," + str(ad[1]) + "," + str(ad[1]/ad[2]) + "," + ad[0] + os.linesep)
    stream.close() 