import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Context Switching Simulator", layout="wide")
st.title("🧠 Context Switching Simulator")

# ---------------- INPUT ----------------
n = st.number_input("Number of Processes", 1, 10, 3)

at, bt, pr = [], [], []

st.subheader("Process Details")
cols = st.columns(3)
for i in range(n):
    with cols[0]:
        at.append(st.number_input(f"AT P{i+1}", 0, 50, key=f"at{i}"))
    with cols[1]:
        bt.append(st.number_input(f"BT P{i+1}", 1, 50, key=f"bt{i}"))

algo = st.selectbox("Algorithm", ["FCFS","SJF","Priority","Round Robin"])

mode = "Non-Preemptive"
if algo in ["SJF","Priority"]:
    mode = st.selectbox("Mode", ["Non-Preemptive","Preemptive"])

if algo == "Round Robin":
    tq = st.number_input("Time Quantum", 1, 20, 2)

cs = st.number_input("Context Switch Time", 0, 10, 0)

# ---------------- RUN ----------------
if st.button("Run Simulation"):

    if algo=="FCFS" and mode!="Non-Preemptive":
        st.error("FCFS supports only Non-Preemptive")
        st.stop()

    if algo=="Round Robin" and mode!="Preemptive":
        st.error("Round Robin supports only Preemptive")
        st.stop()

    wt=[0]*n
    tat=[0]*n
    gantt=[]
    time=0

    # -------- FCFS --------
    if algo=="FCFS":
        order=sorted(range(n), key=lambda i:at[i])
        for i in order:
            if time<at[i]:
                time=at[i]
            wt[i]=time-at[i]
            gantt.append((f"P{i+1}", bt[i]))
            time+=bt[i]
            gantt.append(("CS", cs))
            time+=cs
            tat[i]=wt[i]+bt[i]
        nature="Non-Preemptive"

    # -------- SJF --------
    elif algo=="SJF":
        if mode=="Non-Preemptive":
            done=[False]*n
            while not all(done):
                idx=-1
                mn=9999
                for i in range(n):
                    if not done[i] and at[i]<=time and bt[i]<mn:
                        mn=bt[i]; idx=i
                if idx==-1:
                    time+=1; continue
                wt[idx]=time-at[idx]
                gantt.append((f"P{idx+1}", bt[idx]))
                time+=bt[idx]
                gantt.append(("CS", cs))
                time+=cs
                tat[idx]=wt[idx]+bt[idx]
                done[idx]=True
            nature="Non-Preemptive"

        else:
            rt=bt[:]
            complete=0
            while complete<n:
                idx=-1; mn=9999
                for i in range(n):
                    if at[i]<=time and rt[i]>0 and rt[i]<mn:
                        mn=rt[i]; idx=i
                if idx==-1:
                    time+=1; continue
                gantt.append((f"P{idx+1}",1))
                rt[idx]-=1
                time+=1
                if rt[idx]==0:
                    complete+=1
                    wt[idx]=time-bt[idx]-at[idx]
                    tat[idx]=wt[idx]+bt[idx]
            nature="Preemptive"

    # -------- PRIORITY --------
    elif algo=="Priority":
        pr=[]
        for i in range(n):
            pr.append(st.number_input(f"Priority P{i+1}",1,10,key=f"p{i}"))

        if mode=="Non-Preemptive":
            done=[False]*n
            while not all(done):
                idx=-1; best=9999
                for i in range(n):
                    if not done[i] and at[i]<=time and pr[i]<best:
                        best=pr[i]; idx=i
                if idx==-1:
                    time+=1; continue
                wt[idx]=time-at[idx]
                gantt.append((f"P{idx+1}", bt[idx]))
                time+=bt[idx]
                gantt.append(("CS", cs))
                time+=cs
                tat[idx]=wt[idx]+bt[idx]
                done[idx]=True
            nature="Non-Preemptive"

        else:
            rt=bt[:]
            complete=0
            while complete<n:
                idx=-1; best=9999
                for i in range(n):
                    if at[i]<=time and rt[i]>0 and pr[i]<best:
                        best=pr[i]; idx=i
                if idx==-1:
                    time+=1; continue
                gantt.append((f"P{idx+1}",1))
                rt[idx]-=1
                time+=1
                if rt[idx]==0:
                    complete+=1
                    wt[idx]=time-bt[idx]-at[idx]
                    tat[idx]=wt[idx]+bt[idx]
            nature="Preemptive"

    # -------- RR --------
    elif algo=="Round Robin":
        rt=bt[:]
        remain=n
        while remain>0:
            for i in range(n):
                if rt[i]>0 and at[i]<=time:
                    if rt[i]>tq:
                        gantt.append((f"P{i+1}",tq))
                        time+=tq
                        rt[i]-=tq
                    else:
                        gantt.append((f"P{i+1}",rt[i]))
                        time+=rt[i]
                        wt[i]=time-bt[i]-at[i]
                        rt[i]=0
                        remain-=1
                    gantt.append(("CS",cs))
                    time+=cs
        for i in range(n):
            tat[i]=wt[i]+bt[i]
        nature="Preemptive"

    # -------- OUTPUT --------
    st.subheader(f"{algo} ({nature})")

    for i in range(n):
        st.write(f"P{i+1} → WT={wt[i]}  TAT={tat[i]}")

    st.write("Average WT:", sum(wt)/n)
    st.write("Average TAT:", sum(tat)/n)

    # -------- GANTT --------
    fig, ax = plt.subplots(figsize=(10,2))
    start=0
    for name,dur in gantt:
        ax.barh(0,dur,left=start)
        ax.text(start+dur/2,0,name,ha='center')
        start+=dur
    ax.set_yticks([])
    st.pyplot(fig)
