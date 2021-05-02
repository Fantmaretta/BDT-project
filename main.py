#print("ciao mondooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
# ciao


print("ciao")
f= open("guru99.txt","w+")
for i in range(10):
     f.write("This is line %d\r\n" % (i+1))
     print("ciao ciao ciao")
f.close()

'''f = open("guru99.txt", "w+")

def prova(file):
     file.write("ciao")



schedule.every(5).seconds.do(prova, f)'''
#schedule.every().hour.do(self.fetch_prediction, url_pred)
#schedule.every().day.do(self.fetch_prediction, url_pred)

'''while True:
    schedule.run_pending()
    time.sleep(1)'''

