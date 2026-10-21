#输入文件名，将域控上的DNS文件导出并以域名为文件名，并对输入的文件名进行文字处理。
file_name = input("请输入文件名：")

output_file = file_name + "输出文件.txt"

#A记录文件处理过程，字符增删。

back_file_name = "." + file_name  #文件名加前缀“.”

two_file_name = file_name +".txt"   #文件名加后缀.txt 后面

domain = file_name[3:]     #字符分割从第三个字符开始

cname_domain = file_name[-5:]  #取cname记录中的域名

A_domain = "." + file_name[:-6]   #根据实际情况进行调整参数：如这里测试时使用的文件名是yc.sh.tb   

A = "create dns zone global dns-records a "  #创建A记录
CNAME = "create dns zone global dns-records cname "   #创建CNAME记录



#打开文件取字符并进行字符拼接

with open(two_file_name , 'r') as input_file, open(output_file, 'w') as output_file:
    
    for line in input_file:
        # Split the line by tab characters ('\t').
        parts = line.split('\t')
        
        first_part = f"{parts[0]}"     #取第一个制表符之前的字符
        
        second_part = f"{parts[2]}"     #取第三个制表符和第二个制表符之间的字符
        
        second_part_back = second_part[:-1]  #针对cname记录中的域名提取字符并去掉最后一个字符，通常是个.
        
        # Check if the line contains "主机(A)".
        if "主机(A)" in line:
            # 如果主机行中包含“主机（A）”则根据制表符进行取数据，取第一个制表符之前的和第二个制表符
            extracted_text = A + f"{parts[0]}" + "." + file_name + ' generate_ptr_record "enable" domain ' + f"{parts[0]}"  + " zone " + file_name  + ' state "enable" type "a" ' + "a_records [{ ttl 60 address " + f"{parts[2]}" + " }]"
        else:
        
        
            if "别名(CNAME)" in line:
            #如果主机行中包含“别名（CNAME）”则根据制表符进行取数据，取第一个制表符之前的和第二个制表符
                
                extracted_text = CNAME + '"' + f"{parts[0]}" + '"' + " ttl 60 cname_records "  + '"' + f"{parts[0]}" + '" ' + "domain " + '"' + second_part_back[:-6]  + '"' + " zone " + '"' + cname_domain + '"' + ' state "enable" type "cname"'
            # If not, skip this line.
            else:
                
             
                
                continue
        
        #else:
            # If not, skip this line.
            #continue
        
        # Write the extracted text to the output file with a tab separator.
        output_file.write(extracted_text + '\n')

# 2. Close both input and output files.
input_file.close()
output_file.close()
