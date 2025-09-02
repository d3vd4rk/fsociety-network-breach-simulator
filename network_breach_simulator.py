import os
import sys
import time
import random
import itertools
import ctypes

RESET="\033[0m";BOLD="\033[1m";DIM="\033[2m";ITALIC="\033[3m";UNDER="\033[4m"
BLACK="\033[30m";RED="\033[31m";GREEN="\033[32m";YELLOW="\033[33m";BLUE="\033[34m";MAGENTA="\033[35m";CYAN="\033[36m";WHITE="\033[37m"
BGBLACK="\033[40m";BGGREEN="\033[42m";BGRED="\033[41m";BGCYAN="\033[46m"

def enable_ansi():
    if os.name=="nt":
        h=ctypes.windll.kernel32.GetStdHandle(-11)
        mode=ctypes.c_uint32()
        if ctypes.windll.kernel32.GetConsoleMode(h,ctypes.byref(mode)):
            ctypes.windll.kernel32.SetConsoleMode(h,mode.value|0x0004)

def set_title_and_clear():
    if os.name=="nt":
        os.system("title fsociety breach")
        os.system("cls")
    else:
        sys.stdout.write("\033]0;fsociety breach\007")
        sys.stdout.flush()
        os.system("clear")

def rand_ip():
    return ".".join(str(random.randint(1,254)) for _ in range(4))

def pick_ports():
    base=[21,22,23,25,53,80,110,139,143,389,443,445,587,993,995,1433,1521,2049,2375,3306,3389,4444,5000,5432,5900,6379,8080,8443,9000]
    sample=random.sample(base,k=random.randint(6,12))
    open_ports=set(random.sample(sample,k=max(1,len(sample)//3)))
    return [(p,"OPEN" if p in open_ports else "CLOSED") for p in sorted(sample)]

def service_for_port(p):
    m={21:"ftp",22:"ssh",23:"telnet",25:"smtp",53:"dns",80:"http",110:"pop3",139:"netbios",143:"imap",389:"ldap",443:"https",445:"smb",587:"smtp-sub",993:"imaps",995:"pop3s",1433:"mssql",1521:"oracle",2049:"nfs",2375:"docker",3306:"mysql",3389:"rdp",4444:"metasvc",5000:"svc",5432:"postgres",5900:"vnc",6379:"redis",8080:"http-alt",8443:"https-alt",9000:"svc"}
    return m.get(p,"svc")

def rand_user_for_port(p):
    users={21:["anonymous","ftp","backup"],22:["root","admin","user","devops"],23:["root","admin"],25:["postfix","admin"],3306:["root","mysql"],3389:["Administrator","admin","user"],5432:["postgres","admin"],5900:["user","operator"],445:["guest","admin"],6379:["default","redis"],80:["admin","web"],8080:["admin","tomcat"],443:["admin","ops"]}
    return random.choice(users.get(p,["admin","user","root"]))

def print_fast(x):
    sys.stdout.write(x+"\n");sys.stdout.flush()

def progress_bar(pct,w=26):
    f=int(w*pct/100);return "["+GREEN+"#"*f+RESET+DIM+"-"*(w-f)+RESET+"] "+f"{pct:3d}%"

def hydra_bruteforce(ip,p):
    user=rand_user_for_port(p);svc=service_for_port(p);spin=itertools.cycle(["|","/","-","\\"]);pct=0
    step=[1,2,3,4,5]
    while pct<100:
        pct=min(100,pct+random.choice(step))
        bar=progress_bar(pct)
        line=f"{CYAN}hydra{RESET} {WHITE}{ip}:{p}{RESET} {DIM}{svc}{RESET} user={YELLOW}{user}{RESET} {bar} {next(spin)}"
        print_fast(line)
        time.sleep(random.uniform(0.012,0.035))
    creds=random.choice([f"{user}:admin",f"{user}:toor",f"{user}:password",f"{user}:P@ssw0rd",f"{user}:letmein",f"{user}:changeme"])
    print_fast(f"{GREEN}login found{RESET} {WHITE}{ip}:{p}{RESET} {DIM}{svc}{RESET} -> {YELLOW}{creds}{RESET}")
    return creds

def scan_host(ip):
    print_fast(f"{DIM}Scanning {RESET}{WHITE}{ip}{RESET} {DIM}...{RESET}")
    ports=pick_ports();time.sleep(random.uniform(0.01,0.03))
    for p,state in ports:
        svc=service_for_port(p)
        color=GREEN if state=="OPEN" else RED
        print_fast(f"PORT {WHITE}{p}{RESET}/tcp {color}{state:<6}{RESET} {DIM}{svc}{RESET}")
        time.sleep(random.uniform(0.003,0.010))
    hits=[]
    open_candidates=[p for p,s in ports if s=="OPEN" and p in {21,22,23,80,443,445,3306,3389,5432,5900,6379,8080}]
    if open_candidates and random.random()<0.85:
        pick=random.sample(open_candidates,k=min(len(open_candidates),random.randint(1,3)))
        for p in pick:
            creds=hydra_bruteforce(ip,p)
            hits.append((p,creds))
    return hits

def header():
    lines=[
        f"{GREEN}{BOLD}█████╗{WHITE} █   █{GREEN}    █████╗   █   █║{RESET}",
        f"{GREEN}{BOLD}█    █║{WHITE}█   █{GREEN}    █    █║  █  █║{RESET}",
        f"{GREEN}{BOLD}█    █║{WHITE}█████║   {GREEN}█████║   ███║{RESET}",
        f"{GREEN}{BOLD}█    █║{WHITE}    █║  {GREEN} █   █║   █  █║{RESET}",
        f"{GREEN}{BOLD}█████║{WHITE}     █║ {GREEN}  █   █║   █  █║{RESET}",
        f"{GREEN}{BOLD}╚═══╝{WHITE}      ═╝ {GREEN}  █    ╝   █   ╝{RESET}",
        f"{DIM}d a r k n e t   i n f i l t r a t i o n   s u i t e{RESET}",
    ]
    for s in lines:
        print_fast(s);time.sleep(0.015)

def banner():
    print_fast(f"{DIM}{BGBLACK}{WHITE}──────────────────────────────────────────────{RESET}")
    print_fast(f"{GREEN}fsociety breach engine v1.0{RESET}")
    print_fast(f"{DIM}target discovery: adaptive subnet spray{RESET}")
    print_fast(f"{DIM}mode: nmap/hydra simulation{RESET}")
    print_fast(f"{DIM}{BGBLACK}{WHITE}──────────────────────────────────────────────{RESET}")


def run_sim():
    random.seed()
    header()
    banner()
    total_hosts=random.randint(10,18)
    owned=[]
    for _ in range(total_hosts):
        ip=rand_ip()
        hits=scan_host(ip)
        for p,creds in hits:
            owned.append((ip,p,creds))
        time.sleep(random.uniform(0.01,0.03))
    print_fast("")
    print_fast(f"{WHITE}{BOLD}summary{RESET}")
    print_fast(f"hosts scanned: {YELLOW}{total_hosts}{RESET}")
    print_fast(f"credentials found: {YELLOW}{len(owned)}{RESET}")
    for ip,p,creds in owned[-5:]:
        print_fast(f"{GREEN}owned{RESET} {WHITE}{ip}:{p}{RESET} -> {YELLOW}{creds}{RESET}")
    print_fast("")
    time.sleep(0.35)
    print_fast(f"{BOLD}{BGGREEN}{BLACK} Access granted – fsociety owns you. {RESET}")


def menu():
    while True:
        set_title_and_clear();enable_ansi()
        print_fast(f"{GREEN}{BOLD}=============================={RESET}")
        print_fast(f"{GREEN}{BOLD} fsociety breach{RESET}")
        print_fast(f"{GREEN}{BOLD}=============================={RESET}")
        print_fast(f"{WHITE}[1] START{RESET}")
        print_fast(f"{WHITE}[2] QUIT{RESET}")
        choice=input(f"{GREEN}> {RESET}").strip()
        if choice=="1":
            set_title_and_clear();enable_ansi()
            print_fast(f"{GREEN}{BOLD}fsociety breach avviato{RESET}")
            print_fast("")
            run_sim()
            print_fast("")
            input(f"{DIM}premi invio per tornare al menu...{RESET}")
        elif choice=="2":
            return
        else:
            time.sleep(0.4)

if __name__=="__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print()