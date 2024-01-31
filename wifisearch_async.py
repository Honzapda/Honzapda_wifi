import asyncio

async def check_host_reachable(host):
    try:
        process = await asyncio.create_subprocess_shell(f'ping -n 1 {host}', 
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.DEVNULL)
        stdout, stderr = await process.communicate()
        
        if b"TTL=" in stdout or b"time=" in stdout:
            print(host + " is reachable")
            return 1
        else:
            return 0
    except asyncio.TimeoutError:
        pass
    return 0

async def wifiSearch():
    count = 0
    tasks = [check_host_reachable(f"192.168.0.{i}") for i in range(1, 255)]
    results = await asyncio.gather(*tasks)
    count = sum(results)

    print("Total reachable hosts: " + str(count))

    return count
    
if __name__ == "__main__":
    asyncio.run(wifiSearch())
