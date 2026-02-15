import streamlit as st

st.title("Context Switching Simulator")

n = st.number_input("Number of processes", 1, 10, 3)

at = []
bt = []
pr = []

st.subheader("Process Details")

for i in range(n):
    col1, col2, col3 = st.columns(3)
    with col1:
        at.append(st.number_input(f"AT P{i+1}", 0, 50, key=f"at{i}"))
    with col2:
        bt.append(st.number_input(f"BT P{i+1}", 1, 50, key=f"bt{i}"))

algo = st.selectbox("Algorithm", ["FCFS","SJF","Priority","Round Robin"])

mode = "Non-Preemptive"
if algo in ["SJF","Priority"]:
    mode = st.selectbox("Mode", ["Non-Preemptive","Preemptive"])

if algo == "Round Robin":
    tq = st.number_input("Time Quantum", 1, 20, 2)

cs = st.number_input("Context Switch Time", 0, 10, 0)

if st.button("Run Simulation"):

    wt = [0]*n
    tat = [0]*n
    time = 0

    if algo == "FCFS":
        order = sorted(range(n), key=lambda i: at[i])
        for i in order:
            if time < at[i]:
                time = at[i]
            wt[i] = time - at[i]
            time += bt[i] + cs
            tat[i] = wt[i] + bt[i]
        nature="Non-Preemptive"

    elif algo=="Round Robin":
        rt=bt[:]
        remain=n
        while remain>0:
            for i in range(n):
                if rt[i]>0 and at[i]<=time:
                    if rt[i]>tq:
                        time+=tq
                        rt[i]-=tq
                    else:
                        time+=rt[i]
                        wt[i]=time-bt[i]-at[i]
                        rt[i]=0
                        remain-=1
                    time+=cs
        for i in range(n):
            tat[i]=wt[i]+bt[i]
        nature="Preemptive"

    st.write(f"Algorithm: {algo} ({nature})")
    for i in range(n):
        st.write(f"P{i+1}  WT={wt[i]}  TAT={tat[i]}")

    st.write("Average WT:", sum(wt)/n)
    st.write("Average TAT:", sum(tat)/n)
