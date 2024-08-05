import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import random
import json
from collections import deque
import time

def subgraph_insertion(selected_node, session_state):

    session_nodes = []
    session_edges = []

    for node in session_state.nodes:
        if node.id != selected_node:
            session_nodes.append(node)

    for edges in session_state.edges:
        if edges.source != selected_node and edges.to != selected_node:
            session_edges.append(edges)
        
    session_state.nodes = session_nodes
    session_state.edges = session_edges

    while len(session_state.nodes) < 10:

        u = session_state.global_queue.popleft()
        added_neighbors = 0

        for v in session_state.problem_graph[u]:
            if v not in session_state.visited_nodes:
                added_neighbors += 1

                new_node = Node(id=v, label=f"Problem {v}")
                session_state.nodes.append(new_node)
                session_state.nodes_obj[v] = new_node

                new_edge = Edge(source=u, target=v)
                session_state.edges.append(new_edge)

                session_state.global_queue.append(v)
                session_state.visited_nodes.add(v)

            if added_neighbors == session_state.k_nearest_neighbors:
                break

        session_state.current_level += 1


motivational_phrases = [
    ("Keep pushing forward!", "💪"),
    ("You can do it!", "🔥"),
    ("Never give up!", "🚀"),
    ("Stay strong!", "🏋️‍♂️"),
    ("Believe in yourself!", "✨"),
    ("Great job!", "👍"),
    ("Keep up the work!", "👏"),
    ("You're doing amazing!", "🌟"),
    ("Stay positive!", "😊"),
    ("Reach for the stars!", "⭐")
]

config = Config(
    width=800,  # Set the width of the graph
    height=600,  # Set the height of the graph
    directed=True,  # Specify if the graph is directed or not
    physics=True,  # Enable physics for automatic node separation
    hierarchical=False,  # Use non-hierarchical layout for better spacing
    # Adjust the physics parameters to control node separation
    node_spacing=500,  # Increase spacing between nodes
    spring_length=500,  # Increase the spring length to spread out nodes
    gravity=-1000  # Adjust gravity to spread out nodes
)

def main():

    selected_node_id = None

    if 'initialized' not in st.session_state:

        st.session_state['initialized'] = True
        st.session_state['k_nearest_neighbors'] = 2
        st.session_state['total_level'] = 3
        st.session_state['source'] = "1353"

        with open("problem_graph_masked.json", 'r') as file:
            st.session_state['problem_graph'] = json.load(file)

        st.session_state['global_queue'] = deque()
        st.session_state['visited_nodes'] = set()
        st.session_state['current_level'] = 1
        st.session_state['global_queue'].append(st.session_state['source'])
        st.session_state['visited_nodes'].add(st.session_state['source'])
        st.session_state['nodes'] = [Node(id=st.session_state['source'], label=f"Problem {st.session_state['source']}")]
        st.session_state['edges'] = []
        st.session_state['nodes_obj'] = {f"{st.session_state.source}" : st.session_state.nodes[0]}

    if 'nodes' in st.session_state:

        selected_node_id = agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=config)

    # Handle node selection and button action
    if selected_node_id:

        # Add a button to delete the node
        if st.sidebar.button("Solved!"):
            # Provide feedback
            rnd = random.randint(0, len(motivational_phrases)-1)
            st.toast(f"{motivational_phrases[rnd][0]}", icon=motivational_phrases[rnd][1])
            time.sleep(1)

            # Perform subgraph insertion
            subgraph_insertion(selected_node_id, st.session_state)

            # Rerun to update the graph
            st.rerun()

if __name__ == "__main__":
    main()
