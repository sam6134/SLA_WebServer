def monitor(t,init_servers,init_fs):
    if(t<2.5):
        if(init_fs<1):
            return init_servers, init_fs+0.1
        elif(init_servers>1):
            return init_servers-1,init_fs
        else:
            return init_servers,init_fs
    elif(init_servers<4):
        return init_servers+1,init_fs
    else:
        return init_servers,init_fs-0.1
