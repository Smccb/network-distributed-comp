
with open("britney.mp3", mode="rb") as file:
    contents = file.read()
    
    chunkSize = 1000*500
    
    f = open('1.mp3', 'wb+')
    
    f.write(contents[0:chunkSize])
    
    f.close()
    
    f = open('2.mp3', 'wb+')
    
    f.write(contents[chunkSize:chunkSize*2])
    
    f.close()