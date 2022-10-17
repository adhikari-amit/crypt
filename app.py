from flask import Flask,request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import smtplib

from RSA_Algo4 import e , d, n
from re import ASCII
import time
import timeit
import os
import sys

from gcd_idea import *
t=open("log.txt","r")
temp_l=[]
temp=""
for i in t.read():
    if(i=="-"):
        temp_l.append(int(temp))
        temp=""
    else:
        temp+=i
t.close()

n=temp_l[0]
e=temp_l[1]
d=temp_l[2]

t=open("log.txt","w")
t.write(str(n)+"-")
t.write(str(e)+"-")
t.write(str(d)+"-")
t.close()

UPLOAD_FOLDER = "static/Files/Uploads"
ENCRYPT_UPLOAD_FOLDER = "static/Files/Encrypted"
DECRYPT_UPLOAD_FOLDER = "static/Files/Decrypted"

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPT_UPLOAD_FOLDER']=ENCRYPT_UPLOAD_FOLDER
app.config['DECRYPT_UPLOAD_FOLDER']=DECRYPT_UPLOAD_FOLDER


class Encrypt:
    def __init__(self):
        self.name_of_the_input_file="test.txt"
        self.inter_file_name=""
        self.Input_data_in_binry_coded_ascii_format=[]
        self.Encript_Message_ascii_format=[]
        self.Encript_Message_binary_bunched_format=[]
        self.start_enc_time=""
        self.end_enc_time=""
    def convert_file(self,filelocation):
        self.name_of_the_input_file =filelocation
        name_of_the_input_file_with_ext = self.name_of_the_input_file
        plsize=os.path.getsize(self.name_of_the_input_file)
        print("Input File Size",plsize,"bytes")
        if(self.name_of_the_input_file[-3:]!="txt"):
            try:
                Inter_Input_file = open("text.txt","w")
                t_data = open(self.name_of_the_input_file,"rb")
            except Exception as e:
                print(" error occoured when opened "+"text.txt or "+self.name_of_the_input_file)

            temp=[]
            for i in t_data:
                temp.append(i.hex())

            for i in temp:
                Inter_Input_file.write(i)
            Inter_Input_file.close()
            t_data.close()
            self.name_of_the_input_file = "text.txt"

    def encrypt_step_1(self):     
        try:
            Input_file = open(self.name_of_the_input_file,"r",encoding="utf8")
        except Exception as e:
            print(e+" error occoured when opened "+self.name_of_the_input_file)

        self.inter_file_name = "File1.txt"
        try:
            intermediate_binary_file = open(self.inter_file_name,"wb")
        except Exception as e:
                print(e+" error occoured when opened "+self.inter_file_name)

        Input_file.seek(0)
        bin_ascii_data=[]
        for i in Input_file.read():
            i_to_bin = bin(ord(i))[2:]
            i_to_bin = i_to_bin.zfill(8)
            bin_ascii_data.append(i_to_bin)
            intermediate_binary_file.write(bytes(i_to_bin, 'utf-8'))
        print("")
        Input_file.close()
        intermediate_binary_file.close()

    def encrypt_step_7(self):
        try:
            intermediate_binary_file = open(self.inter_file_name,"rb")
        except Exception as e:
            print(e+" error occoured when second time opened "+self.inter_file_name)

        t_data_holder=[]
        bunch_size = 4
        for i in intermediate_binary_file.read():
            if(len(t_data_holder)==bunch_size):
                ttt=""
                
                for i_temp in t_data_holder:
                    ttt+=chr(i_temp)
                
                t___=int(ttt,2)
                self.Input_data_in_binry_coded_ascii_format.append(t___)
                t_data_holder=[i]
            else:
                t_data_holder.append(i)

        if(len(t_data_holder)==4):
            ttt=""
            for i_temp in t_data_holder:
                    ttt+=chr(i_temp)
            t___=int(ttt,2)
            self.Input_data_in_binry_coded_ascii_format.append(t___)
            t_data_holder=[]

        if(len(t_data_holder)!=0):
            ttt = "0"*(bunch_size-len(t_data_holder))
            for i_temp in t_data_holder:
                    ttt=ttt+chr(i_temp)
            t___=int(ttt,2)
            self.Input_data_in_binry_coded_ascii_format.append(t___)
        intermediate_binary_file.close()

    def encrypt_step_8(self):

        self.start_enc_time = timeit.default_timer()
        
        for i in self.Input_data_in_binry_coded_ascii_format:
            C = (int(i)**e)%n
            self.Encript_Message_ascii_format.append(C)

        Encript_Message_binary_format=[]
        for i in self.Encript_Message_ascii_format:
            temp_=bin(i)[2:]

            Encript_Message_binary_format.append(temp_)

        self.temp_=""
        self.second_bunch_len=21
        for j in Encript_Message_binary_format:
            ttt = j.zfill(self.second_bunch_len)
            self.temp_+=ttt

    def encrypt_step_9(self):
                
        t_data_holder=""
        
        for j in self.temp_:
            if(len(t_data_holder)==self.second_bunch_len):
                
                t___=t_data_holder
                self.Encript_Message_binary_bunched_format.append(t___)
                t_data_holder=j
            else:
                t_data_holder+=j
        
        if(len(t_data_holder)==self.second_bunch_len):
            t___=t_data_holder
            self.Encript_Message_binary_bunched_format.append(t___)
            t_data_holder=[]

        if(len(t_data_holder)!=0):
            ttt = "0"*(self.second_bunch_len-len(t_data_holder))
            t___ = t_data_holder+ttt
            self.Encript_Message_binary_bunched_format.append(t___)

    def encrypt_step_10(self):

        cypher_file_name = "file3.txt"
        try:
            cypher_file = open(cypher_file_name,"w")
        except Exception as e:
            print(" error occoured when opening "+cypher_file_name)
        for i in self.Encript_Message_binary_bunched_format:
            ttt=""
            for k in i:
                ttt+=k
                if(len(ttt)==7):
                    l =int(ttt,2)
                    ttt__ = chr(l)
                    cypher_file.write(ttt__)
                    ttt=""
        cypher_file.close()
        self.end_enc_time = timeit.default_timer()
        print("\nTime took to encrypt the message2 = "+str(self.end_enc_time-self.start_enc_time)+"\n")
       

class Decrypt:
    def __init__(self):
        self.Encript_Message_ascii_format__temp=[]
        self.Input_data_in_binary_decoded_ascii_format=[]
        self.start_dec_time=""
        self.end_dec_time=""
    def decrypt_step_1(self,encryptedfilename):

        cypher_file_name = encryptedfilename
        try:
            cypher_file = open(cypher_file_name,"r")
        except Exception as e:
            print(" error occoured when opening "+cypher_file_name)
        self.start_dec_time=timeit.default_timer()
        print("start time: ",self.start_dec_time)
        temp=[]
        temp2=""
        for i in cypher_file.read():
            
            t=ord(i)
            t=bin(t)[2:]
            temp2+=str(t).zfill(7)
            if(len(temp2)==21):
                temp.append(temp2)
                temp2=""

        self.Encript_Message_ascii_format__temp=[]
        for i in temp:
            ttt = i.lstrip("0")
            if(len(ttt)==0):
                ttt="0"
            ttt = int(ttt,2)
            self.Encript_Message_ascii_format__temp.append(ttt)
        cypher_file.close()
       

    def decrypt_step_2(self):
      
        self.Input_data_in_binary_decoded_ascii_format=[]
       
        for i in self.Encript_Message_ascii_format__temp:
            ttt=i
            m = (ttt**d) % n
            self.Input_data_in_binary_decoded_ascii_format.append(m)
       

    def decrypt_step_3(self):
       
        temp_string=""
        for i in self.Input_data_in_binary_decoded_ascii_format:
            ttt = bin(i)[2:]
            ttt = ttt.zfill(4)
            temp_string+=ttt
          
        self.the_read_message=[]
        t_data=""
        for i in temp_string:
            if(len(t_data)==8):
                ttt=chr(int(t_data,2))
                self.the_read_message.append(ttt)
                
                t_data=i
            else:
                t_data+=i

        if(len(t_data)==8):
            ttt=chr(int(t_data,2))
            self.the_read_message.append(ttt)
          

    def decrypt_step_4(self,OutputFileName):
        last_output_file=str(os.path.join(app.config['DECRYPT_UPLOAD_FOLDER'], 'file5.txt'))
        try:
            dec_file = open(last_output_file,"w")
        except Exception as e:
            print(e+" error occoured when opened "+last_output_file)

        for i in self.the_read_message:
            dec_file.write(i)
        dec_file.close()

        Output_file_name=OutputFileName

        if(Output_file_name[-3:]!="txt"):
            Output = open(Output_file_name,"wb")
            aa = open( last_output_file,"r")
            T=[]
            for i in aa:
                T.append(bytes.fromhex(i))
            aa.close()

            for j in T:
                Output.write(j)
            Output.close()
        else:
            os.rename( last_output_file, Output_file_name)
        self.end_dec_time = timeit.default_timer()
        print("end time: ",self.end_dec_time)
        print("\nTime took to decrypt the message = "+str(self.end_dec_time-self.start_dec_time)+"\n")
        

@app.route('/', methods =["GET", "POST"])
@app.route('/encrypt', methods =["GET", "POST"])
def encrypt():
    error=None
    if request.method == "POST":
            try:
                # Uploading the Input File
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                # Collecting the Email addresses
                email=[]
                email00 = request.form["email00"]
                email01 = request.form["email01"]
                email02 = request.form["email02"]
                email03 = request.form["email03"]
                email.append(email00)
                email.append(email01)
                email.append(email02)
                email.append(email03)
                
                # Encryption process
                obj = Encrypt()
                obj.convert_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                obj.encrypt_step_1()
                obj.encrypt_step_7()
                obj.encrypt_step_8()
                obj.encrypt_step_9()
                obj.encrypt_step_10()
                allotp = genotps(4)
                allotps = [i*e for i in allotp] 
                
                # SMTP mail send to given email addresses
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("amit.adhikari@tnu.in", "amit@tnu")
                otpcount=0
                for i in email:
                    SUBJECT = "Decryption Key"
                    message = 'Subject: {}\n\n{}'.format(SUBJECT, str(allotps[otpcount]))
                    s.sendmail("amit.adhikari@tnu.in",i, message)
                    otpcount=otpcount+1
                s.quit()
                return redirect(url_for('decrypt'))
            except:
                error="UnIntended Error Occured."
                return render_template("encryptionform.html",error=error)    
    return render_template("encryptionform.html",error=error)


@app.route('/decrypt', methods =["GET", "POST"])
def decrypt():
    error="Otp Send Successfully"
    if request.method == "POST":
        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['ENCRYPT_UPLOAD_FOLDER'], filename))

            otp00 = request.form["otp00"]
            otp01 = request.form["otp01"]
            otp02 = request.form["otp02"]
            otp03 = request.form["otp03"]
            OutputFileName=request.form['outputfile']

            arr=[]
            arr.append(int(otp00))
            arr.append(int(otp01))
            arr.append(int(otp02))
            arr.append(int(otp03))

            check = checkotp(4,e,arr)
            if(check):
                o = Decrypt()
                o.decrypt_step_1(str(os.path.join(app.config['ENCRYPT_UPLOAD_FOLDER'], filename)))
                o.decrypt_step_2()
                o.decrypt_step_3()
                o.decrypt_step_4(str(os.path.join(app.config['DECRYPT_UPLOAD_FOLDER'], OutputFileName)))
                error="Key matched successfully."
                return render_template("success.html",error=error,OutputFileName=OutputFileName)
            else:
                error="Key Didn't matched."
                return render_template("decryptionform.html",error=error)
        except:       
            error="Error in the Encrypted File."
            return render_template("decryptionform.html",error=error)

    return render_template("decryptionform.html",error=error)

if __name__=='__main__':
   app.run()    