import dpkt,socket
def sorted_keys_2(x):#key 정렬시 첫번째 요소를 기준으로 정렬하는 함수. 
    return x[0]
def sorted_keys_1(x):#key 정렬시 두번째 요소를 기준으로 정렬하는 함수. 
    return x[1]
while True:
    select=0;print("1. 추출시작 2. 종료");select=input()
    if select=='1':
        with open('videoplusimg.pcap', 'rb') as f:
            pcap = dpkt.pcap.Reader(f)
            dic = {};copy_dic ={};count=1;count2=1;print("One moment, please.")
            for timestamp, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                    continue
                if ip.p != dpkt.ip.IP_PROTO_TCP:
                    continue
                tcp = ip.data
                if len(str(tcp.data.hex())) < 10:
                    continue
                streamIndex = socket.inet_ntoa(ip.src) + ':' + str(tcp.sport) + ':'
                streamIndex += socket.inet_ntoa(ip.dst) + ':' + str(tcp.dport) + ':' + str(tcp.ack)
                streamIndexValue=[tcp.seq,str(tcp.data.hex())]
                if streamIndex in dic:
                    dic[streamIndex] += [streamIndexValue]
                    copy_dic[streamIndex] += [streamIndexValue]
                else:
                    dic[streamIndex] = [streamIndexValue]
                    copy_dic[streamIndex] = [streamIndexValue]
            
        for i in dic.keys(): #패킷내 이미지 추출부분
            tmp=sorted(dic[i],key=sorted_keys_2)
            result="".join(map(sorted_keys_1,tmp))
            header,footer=-1,-1
            for z in range(0,len(result),2): #header(find)
                if result[z:z+7]=="ffd8ffe":
                    header=z
                elif result[z:z+4]=="ffd9":
                    footer=z
            result=result[header:footer+4]
            
            if header>-1:
                str=f"result_{count}.jpg"
                file=open(str,"wb")
                w = result;w =bytes.fromhex(w)
                file.write(w);file.close()
                print(str,"Process success");count+=1

        for j in copy_dic.keys(): #패킷내 동영상 추출부분 
            temp2=sorted(copy_dic[j],key=sorted_keys_2)
            result2="".join(map(sorted_keys_1,temp2))
            viheader=-1
            for z2 in range(0,len(result2),5):
                if result2[z2:z2+10]=="0000001866":
                    viheader=z2
            result2=result2[viheader:]
            if viheader>-1:
                video=f"result_{count2}.mp4";file2=open(video,"wb")
                w2=result2;w2=bytes.fromhex(w2)
                file2.write(w2);file2.close()
                print(video,"Process success");count2+=1
    else:
        break