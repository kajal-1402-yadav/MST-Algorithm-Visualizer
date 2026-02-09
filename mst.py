import tkinter as tk
import math
import random


class MSTVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("MST Algorithm Visualizer")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0f172a')
        
        self.nodes = []
        self.edges = []
        self.vertex_map = {}
        self.algorithm = 'kruskal'
        self.steps = []
        self.current_step = 0
        self.is_playing = False
        self.animation_speed = 1000
        
        self.setup_ui()
        
    def setup_ui(self):
        main = tk.Frame(self.root, bg='#0f172a')
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main, text="MST ALGORITHM VISUALIZER", font=('Courier New', 24, 'bold'),
                 bg='#0f172a', fg='#10b981').pack(pady=(0, 5))
        tk.Label(main, text="GREEDY ALGORITHM IMPLEMENTATION // PRIM'S & KRUSKAL'S",
                 font=('Courier New', 10), bg='#0f172a', fg='#64748b').pack(pady=(0, 20))
        
        algo_frame = tk.Frame(main, bg='#1e293b', relief=tk.RIDGE, bd=2)
        algo_frame.pack(fill=tk.X, pady=(0, 15))
        self.kruskal_btn = self.create_button(algo_frame, "KRUSKAL'S ALGORITHM", '#10b981', lambda: self.select_algorithm('kruskal'))
        self.prim_btn = self.create_button(algo_frame, "PRIM'S ALGORITHM", '#334155', lambda: self.select_algorithm('prim'))
        
        content = tk.Frame(main, bg='#0f172a')
        content.pack(fill=tk.BOTH, expand=True)
        
        canvas_frame = tk.Frame(content, bg='#1e293b', relief=tk.RIDGE, bd=2)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        cost_frame = tk.Frame(canvas_frame, bg='#1e293b')
        cost_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(cost_frame, text="MST COST:", font=('Courier New', 10, 'bold'),
                 bg='#1e293b', fg='#64748b').pack(side=tk.LEFT)
        self.cost_label = tk.Label(cost_frame, text="0", font=('Courier New', 20, 'bold'),
                                    bg='#1e293b', fg='#10b981')
        self.cost_label.pack(side=tk.RIGHT)
        
        self.canvas = tk.Canvas(canvas_frame, width=600, height=500, bg='#1e293b', highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        
        right = tk.Frame(content, bg='#0f172a')
        right.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.setup_graph_controls(right)
        self.setup_controls(right)
        self.setup_legend(right)
        
    def create_button(self, parent, text, bg, command):
        btn = tk.Button(parent, text=text, font=('Courier New', 11, 'bold'), bg=bg,
                       fg='#0f172a' if bg == '#10b981' else '#e2e8f0', relief=tk.FLAT,
                       padx=20, pady=12, command=command)
        btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        return btn
        
    def setup_graph_controls(self, parent):
        frame = tk.Frame(parent, bg='#1e293b', relief=tk.RIDGE, bd=2)
        frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(frame, text="GRAPH CONTROLS", font=('Courier New', 9, 'bold'),
                 bg='#1e293b', fg='#10b981').pack(pady=(10, 5))
        
        tk.Label(frame, text="Vertices (e.g., A B C):", font=('Courier New', 9),
                 bg='#1e293b', fg='#e2e8f0').pack(anchor=tk.W, padx=10, pady=(5, 2))
        self.vertices_entry = tk.Entry(frame, font=('Courier New', 9), width=25)
        self.vertices_entry.pack(padx=10, pady=2, fill=tk.X)
        tk.Button(frame, text="SET VERTICES", font=('Courier New', 9, 'bold'),
                  bg='#10b981', fg='#0f172a', relief=tk.FLAT, padx=10, pady=5,
                  command=self.set_vertices).pack(pady=5)
        
        tk.Label(frame, text="Edge (e.g., A-B-4):", font=('Courier New', 9),
                 bg='#1e293b', fg='#e2e8f0').pack(anchor=tk.W, padx=10, pady=(10, 2))
        self.edges_entry = tk.Entry(frame, font=('Courier New', 9), width=25)
        self.edges_entry.pack(padx=10, pady=2, fill=tk.X)
        tk.Button(frame, text="SET EDGE", font=('Courier New', 9, 'bold'),
                  bg='#10b981', fg='#0f172a', relief=tk.FLAT, padx=10, pady=5,
                  command=self.set_edge).pack(pady=5)
        
        tk.Button(frame, text="RANDOM GRAPH", font=('Courier New', 10, 'bold'),
                  bg='#334155', fg='#e2e8f0', relief=tk.FLAT, padx=15, pady=8,
                  command=self.generate_random_graph).pack(pady=10)
        
    def setup_controls(self, parent):
        frame = tk.Frame(parent, bg='#0f172a')
        frame.pack(fill=tk.X, pady=(0, 10))
        self.play_btn = tk.Button(frame, text="▶ PLAY", font=('Courier New', 11, 'bold'),
                                  bg='#10b981', fg='#0f172a', relief=tk.FLAT, padx=20, pady=10,
                                  command=self.toggle_play)
        self.play_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(frame, text="↺ RESET", font=('Courier New', 11, 'bold'),
                  bg='#334155', fg='#e2e8f0', relief=tk.FLAT, padx=20, pady=10,
                  command=self.reset).pack(side=tk.LEFT, padx=5)
        
        step_frame = tk.Frame(parent, bg='#0f172a')
        step_frame.pack(fill=tk.X, pady=(0, 10))
        self.prev_btn = tk.Button(step_frame, text="← PREV", font=('Courier New', 10, 'bold'),
                                  bg='#334155', fg='#e2e8f0', relief=tk.FLAT, padx=15, pady=8,
                                  command=self.prev_step)
        self.prev_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.next_btn = tk.Button(step_frame, text="NEXT →", font=('Courier New', 10, 'bold'),
                                  bg='#334155', fg='#e2e8f0', relief=tk.FLAT, padx=15, pady=8,
                                  command=self.next_step)
        self.next_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
    def setup_legend(self, parent):
        frame = tk.Frame(parent, bg='#1e293b', relief=tk.RIDGE, bd=2)
        frame.pack(fill=tk.X)
        tk.Label(frame, text="LEGEND", font=('Courier New', 9, 'bold'),
                 bg='#1e293b', fg='#64748b').pack(pady=(10, 5))
        for label, color in [("MST Edge", '#10b981'), ("Examining", '#fbbf24')]:
            item = tk.Frame(frame, bg='#1e293b')
            item.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(item, text="■", font=('Courier New', 14), bg='#1e293b', fg=color).pack(side=tk.LEFT)
            tk.Label(item, text=label, font=('Courier New', 9), bg='#1e293b', fg='#e2e8f0').pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text="", bg='#1e293b').pack(pady=5)
        
    def set_vertices(self):
        vertex_list = self.vertices_entry.get().strip().split()
        if not vertex_list:
            return
        self.vertex_map = {v: i for i, v in enumerate(vertex_list)}
        center_x, center_y, radius = 300, 250, 150
        self.nodes = []
        for i, v in enumerate(vertex_list):
            angle = 2 * math.pi * i / len(vertex_list)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            node = {
                'id': i,
                'x': x,
                'y': y,
                'label': v
            }
            self.nodes.append(node)
        self.edges = []
        self.draw_graph_only()

    def set_edge(self):
        if not self.vertex_map:
            return
        parts = self.edges_entry.get().strip().split('-')
        if len(parts) < 3:
            return
        try:
            from_v, to_v, weight = parts[0].strip(), parts[1].strip(), int(parts[2].strip())
            if from_v in self.vertex_map and to_v in self.vertex_map:
                from_id, to_id = self.vertex_map[from_v], self.vertex_map[to_v]
                if not any(
                    (e['from'] == from_id and e['to'] == to_id) or
                    (e['from'] == to_id and e['to'] == from_id)
                    for e in self.edges
                ):
                    self.edges.append({'from': from_id, 'to': to_id, 'weight': weight})
                    self.edges_entry.delete(0, tk.END)
                    self.draw_graph_only()
        except (ValueError, KeyError):
            pass

    def draw_graph_only(self):
        self.canvas.delete('all')
        for edge in self.edges:
            from_node, to_node = self.nodes[edge['from']], self.nodes[edge['to']]
            self.canvas.create_line(from_node['x'], from_node['y'], to_node['x'], to_node['y'],
                                     fill='#475569', width=2)
            mid_x, mid_y = (from_node['x'] + to_node['x']) / 2, (from_node['y'] + to_node['y']) / 2
            self.canvas.create_oval(mid_x - 15, mid_y - 15, mid_x + 15, mid_y + 15,
                                     fill='#1e293b', outline='#475569', width=2)
            self.canvas.create_text(mid_x, mid_y, text=str(edge['weight']),
                                     font=('Courier New', 12, 'bold'), fill='#e2e8f0')
        for node in self.nodes:
            self.canvas.create_oval(node['x'] - 25, node['y'] - 25, node['x'] + 25, node['y'] + 25,
                                     fill='#334155', outline='#64748b', width=3)
            self.canvas.create_text(node['x'], node['y'], text=node['label'],
                                     font=('Courier New', 16, 'bold'), fill='#e2e8f0')

    def generate_random_graph(self, vertices=None, edges=None):
        vertices = vertices or random.randint(4, 8)
        edges = edges or random.randint(vertices, vertices * 2)
        vertex_labels = [chr(65 + i) for i in range(vertices)]
        self.vertex_map = {v: i for i, v in enumerate(vertex_labels)}
        self.vertices_entry.delete(0, tk.END)
        self.vertices_entry.insert(0, ' '.join(vertex_labels))
        
        center_x, center_y, radius = 300, 250, 150
        self.nodes = [{'id': i, 'x': center_x + radius * math.cos(2 * math.pi * i / vertices),
                       'y': center_y + radius * math.sin(2 * math.pi * i / vertices), 'label': v}
                      for i, v in enumerate(vertex_labels)]
        
        max_edges = (vertices * (vertices - 1)) // 2
        edge_set = set()
        while len(edge_set) < min(edges, max_edges):
            from_node, to_node = random.randint(0, vertices - 1), random.randint(0, vertices - 1)
            if from_node != to_node:
                edge_set.add(tuple(sorted([from_node, to_node])))
        
        self.edges = [{'from': f, 'to': t, 'weight': random.randint(1, 10)} for f, t in edge_set]
        self.run_algorithm()

    def select_algorithm(self, algorithm):
        self.algorithm = algorithm
        self.is_playing = False
        if algorithm == 'kruskal':
            self.kruskal_btn.configure(bg='#10b981', fg='#0f172a')
            self.prim_btn.configure(bg='#334155', fg='#e2e8f0')
        else:
            self.prim_btn.configure(bg='#3b82f6', fg='#0f172a')
            self.kruskal_btn.configure(bg='#334155', fg='#e2e8f0')
        self.run_algorithm()
        
    def run_algorithm(self):
        if not self.nodes:
            return
        self.steps = []
        
        self.current_step = 0
        if self.algorithm == 'kruskal':
            self.kruskals_algorithm()
        else:
            self.prims_algorithm()
        self.update_display()
    
    def has_path_dfs(self, u, v, graph, visited):
        if u == v:
            return True

        visited.add(u)

        for neighbor in graph[u]:
            if neighbor not in visited:
                if self.has_path_dfs(neighbor, v, graph, visited):
                    return True

        return False

    def kruskals_algorithm(self):
        graph = {i: [] for i in range(len(self.nodes))}
        mst_edges, total_cost = [], 0

        self.steps.append({'mst_edges': [], 'examining': None, 'total_cost': 0})

        for edge in sorted(self.edges, key=lambda e: e['weight']):
            u = edge['from']
            v = edge['to']

            # DFS-based cycle check
            if not self.has_path_dfs(u, v, graph, set()):
                self.steps.append({'mst_edges': mst_edges.copy(), 'examining': edge, 'total_cost': total_cost})

                mst_edges.append(edge)
                total_cost += edge['weight']

                graph[u].append(v)
                graph[v].append(u)

                self.steps.append({'mst_edges': mst_edges.copy(), 'examining': None, 'total_cost': total_cost})

        self.steps.append({'mst_edges': mst_edges.copy(), 'examining': None, 'total_cost': total_cost, 'complete': True})

        
    def prims_algorithm(self):
        visited, mst_edges, total_cost = {0}, [], 0
        self.steps.append({'mst_edges': [], 'visited': visited.copy(), 'examining': None, 'total_cost': 0})
        
        while len(visited) < len(self.nodes):
            min_edge = min([e for e in self.edges if (e['from'] in visited) != (e['to'] in visited)],
                          key=lambda e: e['weight'], default=None)
            if not min_edge:
                break
            self.steps.append({'mst_edges': mst_edges.copy(), 'visited': visited.copy(), 'examining': min_edge, 'total_cost': total_cost})
            visited.update([min_edge['from'], min_edge['to']])
            mst_edges.append(min_edge)
            total_cost += min_edge['weight']
            self.steps.append({'mst_edges': mst_edges.copy(), 'visited': visited.copy(), 'examining': None, 'total_cost': total_cost})
        
        self.steps.append({'mst_edges': mst_edges.copy(), 'visited': visited.copy(), 'examining': None, 'total_cost': total_cost, 'complete': True})
        
    def update_display(self):
        if not self.steps or not self.nodes:
            return

        current_step_data = self.steps[self.current_step]

        self.canvas.delete('all')

        is_complete = current_step_data.get('complete', False)
        mst_edges = current_step_data.get('mst_edges', [])
        examining_edge = current_step_data.get('examining')

        mst_edge_set = set()
        for edge in mst_edges:
            mst_edge_set.add((edge['from'], edge['to']))
            mst_edge_set.add((edge['to'], edge['from']))

        examining_key = None
        if examining_edge:
            examining_key = (examining_edge['from'], examining_edge['to'])

        for edge in self.edges:
            from_node = self.nodes[edge['from']]
            to_node = self.nodes[edge['to']]

            edge_key = (edge['from'], edge['to'])
            reverse_key = (edge['to'], edge['from'])

            is_mst_edge = edge_key in mst_edge_set or reverse_key in mst_edge_set
            is_examining = examining_key and (edge_key == examining_key or reverse_key == examining_key)

            if is_complete and not is_mst_edge:
                continue

            if is_mst_edge:
                color = '#10b981'      
                width = 4
            elif is_examining:
                color = '#fbbf24'      
                width = 4
            else:
                color = '#475569'      
                width = 2

            self.canvas.create_line(
                from_node['x'], from_node['y'],
                to_node['x'], to_node['y'],
                fill=color,
                width=width
            )

            mid_x = (from_node['x'] + to_node['x']) / 2
            mid_y = (from_node['y'] + to_node['y']) / 2

            self.canvas.create_oval(
                mid_x - 15, mid_y - 15,
                mid_x + 15, mid_y + 15,
                fill='#1e293b',
                outline=color,
                width=2
            )

            self.canvas.create_text(
                mid_x, mid_y,
                text=str(edge['weight']),
                font=('Courier New', 12, 'bold'),
                fill='#e2e8f0'
            )

        if self.algorithm == 'prim':
            visited_nodes = current_step_data.get('visited', set())
        else:
            visited_nodes = set()
            for edge in mst_edges:
                visited_nodes.add(edge['from'])
                visited_nodes.add(edge['to'])

        for node in self.nodes:
            node_is_visited = node['id'] in visited_nodes

            if node_is_visited:
                fill_color = '#10b981'
                outline_color = '#10b981'
                text_color = '#0f172a'
            else:
                fill_color = '#334155'
                outline_color = '#64748b'
                text_color = '#e2e8f0'

            self.canvas.create_oval(
                node['x'] - 25, node['y'] - 25,
                node['x'] + 25, node['y'] + 25,
                fill=fill_color,
                outline=outline_color,
                width=3
            )

            self.canvas.create_text(
                node['x'], node['y'],
                text=node['label'],
                font=('Courier New', 16, 'bold'),
                fill=text_color
            )


        self.cost_label.configure(
            text=str(current_step_data['total_cost'])
        )

        self.prev_btn.configure(
            state=tk.NORMAL if self.current_step > 0 else tk.DISABLED
        )
        self.next_btn.configure(
            state=tk.NORMAL if self.current_step < len(self.steps) - 1 else tk.DISABLED
        )

        
    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_btn.configure(text="⏸ PAUSE", bg='#ef4444')
            self.play_animation()
        else:
            self.play_btn.configure(text="▶ PLAY", bg='#10b981')
            
    def play_animation(self):
        if not self.is_playing:
            return
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_display()
            self.root.after(self.animation_speed, self.play_animation)
        else:
            self.is_playing = False
            self.play_btn.configure(text="▶ PLAY", bg='#10b981')
            
    def reset(self):
        self.is_playing = False
        self.current_step = 0
        self.play_btn.configure(text="▶ PLAY", bg='#10b981')
        self.update_display()
        
    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()
            
    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_display()


def main():
    root = tk.Tk()
    app = MSTVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
