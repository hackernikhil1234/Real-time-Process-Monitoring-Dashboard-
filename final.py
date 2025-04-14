
import psutil
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update_system_info():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%", fg="white", bg="#1f1f1f", font=("Helvetica", 14, "bold"))
    memory_label.config(text=f"Memory Usage: {memory_info.percent}%", fg="white", bg="#1f1f1f", font=("Helvetica", 14, "bold"))
    
    cpu_usage_history.append(cpu_usage)
    memory_usage_history.append(memory_info.percent)
    
    if len(cpu_usage_history) > 10:
        cpu_usage_history.pop(0)
        memory_usage_history.pop(0)
    
    plot_graph()
    root.after(1000, update_system_info)

def update_process_list():
    for row in process_tree.get_children():
        process_tree.delete(row)
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        process_tree.insert("", "end", values=(proc.info['pid'], proc.info['name'], proc.info['cpu_percent'], proc.info['memory_percent']))
    
    root.after(3000, update_process_list)

def kill_process():
    selected_item = process_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a process to terminate.")
        return
    
    pid = process_tree.item(selected_item)['values'][0]
    try:
        p = psutil.Process(pid)
        p.terminate()
        messagebox.showinfo("Success", f"Process {pid} terminated.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    update_process_list()

def plot_graph():
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(cpu_usage_history, marker='o', linestyle='-', color='lime', label='CPU Usage')
    ax.plot(memory_usage_history, marker='s', linestyle='--', color='cyan', label='Memory Usage')
    ax.set_title("CPU & Memory Usage Trend", fontsize=12, fontweight='bold')
    ax.set_xlabel("Time (seconds)", fontsize=10)
    ax.set_ylabel("Usage (%)", fontsize=10)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    
    for widget in frame_graph.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.get_tk_widget().pack()
    canvas.draw()

root = tk.Tk()
root.title("Real-Time Process Monitoring Dashboard")
root.geometry("1000x700")
root.configure(bg="#1f1f1f")

cpu_label = tk.Label(root, font=("Helvetica", 14, "bold"), bg="#1f1f1f")
cpu_label.pack(pady=10)
memory_label = tk.Label(root, font=("Helvetica", 14, "bold"), bg="#1f1f1f")
memory_label.pack(pady=5)

frame_table = tk.Frame(root, bg="#1f1f1f")
frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ("PID", "Name", "CPU %", "Memory %")
process_tree = ttk.Treeview(frame_table, columns=columns, show='headings', style="Custom.Treeview")
for col in columns:
    process_tree.heading(col, text=col)
    process_tree.column(col, width=220)
process_tree.pack(fill=tk.BOTH, expand=True)

btn_kill = tk.Button(root, text="Kill Process", command=kill_process, bg="#ff4444", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5)
btn_kill.pack(pady=10)

frame_graph = tk.Frame(root, bg="#1f1f1f")
frame_graph.pack()
btn_graph = tk.Button(root, text="Show CPU & Memory Graph", command=plot_graph, bg="#4444ff", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5)
btn_graph.pack(pady=10)

style = ttk.Style()
style.configure("Custom.Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b", font=("Helvetica", 11))
style.map("Custom.Treeview", background=[("selected", "#4CAF50")])

cpu_usage_history = []
memory_usage_history = []
update_system_info()
update_process_list()
root.mainloop()

