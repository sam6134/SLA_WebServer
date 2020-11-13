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

t_ref = 2.5
P1 = 0.67
def controller(t,init_servers,init_fs):
    u_t = (t-t_ref)
    v_t = init_servers
    k_t = init_fs
    v_t1 = int(0.7*v_t + 0.5*(u_t))
    if(v_t1>4):
        v_t1 = 4
    if(v_t == 4):
        k_t1 = 0.9*k_t - 0.5*(u_t*P1)
    return v_t1, k_t1


