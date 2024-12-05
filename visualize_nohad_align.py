import pyhepmc as hep
from graphviz import Digraph

# Input HepMC file
input_file = "filtered.hepmc"

# Open the input file
reader = hep.open(input_file, "r")


def visualize_event(event, output_file):
    graph = Digraph(comment=f"Event {event.event_number}")

    partons = {1, 2, 3, 4, 5, -1, -2, -3, -4, -5, 21}
    accepts = {82, 2212}

    # graph option
    #graph.attr(dpi="350", rankdir="LR")  # Default is often 300; lower it to reduce file size.
    graph.attr(dpi="350")  # Default is often 300; lower it to reduce file size.
    #graph.engine = "patchwork"
   
    with graph.subgraph(name="protons") as proton_subgraph:
        proton_subgraph.attr(rank="same")  # Ensure protons are at the same height

        with graph.subgraph(name="final_states") as final_subgraph:
            final_subgraph.attr(rank="same")
            #final_particles = set()

            # Track edges to avoid duplicates
            drawn_edges = set()
            used_vertices = set()
    
            # Add particles (edges between vertices)
            for particle in event.particles:
    
                if ( abs(particle.pid) > 40 and particle.pid not in accepts ):
                    continue
                particles_in = [p for p in particle.production_vertex.particles_in]
                if len(particles_in) > 0 and all(abs(ptc.pid) > 40 and ptc.pid not in accepts for ptc in particles_in):
                    continue

                if particle.pid == 2212 and particle.production_vertex.id == 0:
                    start_vertex = f"p{particle.id}"
                    proton_subgraph.node(start_vertex, label=f"proton", shape="circle", color="black", style="bold")
                    used_vertices.add(f"V{particle.production_vertex.id}")
                elif any( f"V{p.production_vertex.id}" in used_vertices for p in particles_in ):
                    start_vertex = f"V{particle.production_vertex.id}" if particle.production_vertex else "Unknown"
                    used_vertices.add(f"V{particle.production_vertex.id}")
                else:
                    continue
    
                # Identify the qq -> jj process
                highlight=False
                if ( particle.end_vertex and len(particle.end_vertex.particles_in) == 2 and len(particle.end_vertex.particles_out) == 2 ):
                    # Check if incoming particles are quarks/gluons and outgoing are jets/quarks
                    incoming_pids = [p.pid for p in particle.end_vertex.particles_in]
                    outgoing_pids = [p.pid for p in particle.end_vertex.particles_out]
                    if ( all(pid in partons for pid in incoming_pids) and all(pid in partons for pid in outgoing_pids) ):
                        highlight = True
                if ( particle.production_vertex and len(particle.production_vertex.particles_in) == 2 and len(particle.production_vertex.particles_out) == 2 ):
                    # Check if incoming particles are quarks/gluons and outgoing are jets/quarks
                    incoming_pids = [p.pid for p in particle.production_vertex.particles_in]
                    outgoing_pids = [p.pid for p in particle.production_vertex.particles_out]
                    if ( all(pid in partons for pid in incoming_pids) and all(pid in partons for pid in outgoing_pids) ):
                        highlight = True
    
                if particle.end_vertex:
                    end_vertex = f"V{particle.end_vertex.id}"
                    pids_out = [p.pid for p in particle.end_vertex.particles_out]
                    if len(pids_out) == 0 or all(abs(pid) > 40 and pid not in accepts for pid in pids_out):
                        final_subgraph.node(end_vertex, label="Had", fontsize="8", shape="circle", width="0.1", height="0.1")
                    else:
                        used_vertices.add(f"V{particle.end_vertex.id}")
                else:
                    end_vertex = f"{particle.id}_{particle.pid}"
                    final_subgraph.node(end_vertex, label="Had", fontsize="8", shape="circle", width="0.1", height="0.1")
    
                if (start_vertex, end_vertex, particle.pid) not in drawn_edges:
                    if highlight:
                        graph.edge(start_vertex, end_vertex, label=f"{particle.pid}", fontcolor="blue", fontsize="20", penwidth="3", color="blue")
                    elif particle.pid == 32:
                        graph.edge(start_vertex, end_vertex, label=f"{particle.pid}", fontcolor="red", fontsize="24", fontname="Helvetica-Bold", penwidth="4", color="red")
                    else:
                        graph.edge(start_vertex, end_vertex, label=f"{particle.pid}")
                    drawn_edges.add((start_vertex, end_vertex, particle.pid))

    # Add vertices (interaction points)
    for vertex in used_vertices:
        if vertex != "V0":
            graph.node(vertex, label=f"", shape="circle", width="0.1", height="0.1")

    # Save the graph to a file
    graph.render(output_file, format="pdf", cleanup=True)
    print(f"Visualization saved as {output_file}.pdf")

# Visualize the first event with Z' bosons
for event in reader:
    print(f"Visualizing Event ID: {event.event_number}")
    visualize_event(event, f"event_{event.event_number}")
    break

# Close the reader
reader.close()

# only stable particles
#stable_particles = [p for p in event.particles if p.status == 1]  # Status = 1 means stable particles
#print(f"Number of stable particles: {len(stable_particles)}")

# only specific pdgids
#filtered_particles = [p for p in event.particles if abs(p.pid) in {21, 1, 2, 3, 4, 5, 6}]

# only hard pt particles
# pt_threshold = 10.0  # GeV
# high_pt_particles = [p for p in event.particles if math.sqrt(p.momentum.px**2 + p.momentum.py**2) > pt_threshold]

