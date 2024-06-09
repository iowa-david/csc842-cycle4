import psutil
import sqlite3
import asyncio
import datetime
import time

_PERCENT_THRESH = 3
_WAIT = 1 #seconds to wait between runs

async def checkCPU():
    sampleCPU = []
    for x in range(10):
        sampleCPU.append(psutil.cpu_percent(interval=1, percpu=False))

    return sum(sampleCPU) / len(sampleCPU)
    
async def checkMemory():
    return psutil.virtual_memory().percent
    
async def getProcessInfo():
    process_infos = []
    for proc in psutil.process_iter():
        proc_info = dict()
        with proc.oneshot():
            proc_info["pid"] = proc.pid
            proc_info["ppid"] = proc.ppid()
            proc_info["name"] = proc.name()
            proc_info["cpu_percent"] = proc.cpu_percent()
            proc_info["memory_percent"] = proc.memory_percent()
            mem_info = proc.memory_info()
            proc_info["mem_rss"] = mem_info.rss

            proc_info["num_threads"] = proc.num_threads()
            #proc_info["nice_priority"] = proc.nice()
        #only track if memory or cpu greater than identified threshold
        if(proc_info["memory_percent"] > _PERCENT_THRESH or proc_info["cpu_percent"] > _PERCENT_THRESH):    
            process_infos.append(proc_info)
    
    return process_infos


def createDB(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE overview(correlation_id, timestamp, cpu, memory)")
    cur.execute("CREATE TABLE detail(correlation_id, timestamp, pid, name, cpu, memory, num_threads)")

def addOverview(con, correlation_id, timestamp, cpu, memory):
    cur = con.cursor()

    insert = """INSERT INTO overview
                      (correlation_id, timestamp, cpu, memory) 
                      VALUES (?, ?, ?, ?);"""

    data = (correlation_id, timestamp, cpu, memory)
    cur.execute(insert, data)
    con.commit()

def addDetail(con, correlation_id, timestamp, process_list):
    cur = con.cursor()

    insert = """INSERT INTO detail
                      (correlation_id,  pid, name, cpu, memory, num_threads) 
                      VALUES (?, ?, ?, ?, ?, ?);"""

    records = []

    for x in process_list:
        data = (correlation_id, x["pid"], x["name"], x["cpu_percent"], x["memory_percent"], x["num_threads"])
        records.append(data)
                                                        
    cur.executemany(insert, records)
    
    con.commit()

def getAllOverview(con):
    cur = con.cursor()
    statement = """select * from overview"""
  
    cur.execute(statement) 
  
    output = cur.fetchall() 
    for row in output: 
        print(row) 

def getAllDetail(con):
    cur = con.cursor()
    statement = """select * from detail"""
  
    cur.execute(statement) 
  
    output = cur.fetchall() 
    for row in output: 
        print(row) 
 
    
async def main():
    correlation_id = 1
    con = sqlite3.connect(":memory:")
    createDB(con)

    for x in range(5):
        timestamp = datetime.datetime.now()
        cpu, memory, process_list = await asyncio.gather(
            checkCPU(),
            checkMemory(),
            getProcessInfo()
        )
        addOverview(con, correlation_id, timestamp, cpu, memory)
        addDetail(con, correlation_id, timestamp, process_list)
        #print(cpu)
        #print(memory)
        #print(process)
        correlation_id+=1
        time.sleep(_WAIT)

    getAllOverview(con)
    getAllDetail(con)
    
asyncio.run(main())
