use std::collections::{HashMap, HashSet};
use std::fs;
use std::path::PathBuf;

#[derive(Debug, Clone)]
struct Graph {
    nodes: HashMap<String, Vec<String>>,
}

impl Graph {
    fn new() -> Self {
        Graph {
            nodes: HashMap::new(),
        }
    }

    fn add_node_and_neighbors(&mut self, name: String, neighbors: Vec<String>) {
        self.nodes.entry(name.clone()).or_insert(neighbors);
    }
}

fn main() {
    let input = read_input("input.txt");
    println!("Solution for part 1: {}", part1(&input));
    println!("Solution for part 2: {}", part2(&input));
}

fn read_input(filename: &str) -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push(filename);

    fs::read_to_string(path)
        .expect("Could not read the input file")
        .trim()
        .to_string()
}

fn count_nb_different_paths(graph: &Graph) -> u64 {
    let start = "you";
    let end = "out";
    let mut visited = HashSet::new();
    let count = dfs(&graph, start, end, &mut visited);

    count
}

fn count_nb_different_paths_2(graph: &Graph) -> u64 {
    let start = "svr";
    let end = "out";
    let must_visit_1 = "dac";
    let must_visit_2 = "fft";

    // svr -> dac -> fft -> out
    let nb_paths_part_1 = dfs(&graph, start, must_visit_1, &mut HashSet::new());
    let nb_paths_part_2 = dfs(&graph, must_visit_1, must_visit_2, &mut HashSet::new());
    let nb_paths_part_3 = dfs(&graph, must_visit_2, end, &mut HashSet::new());

    let total_1 = nb_paths_part_1 * nb_paths_part_2 * nb_paths_part_3;

    // svr -> fft -> dac -> out
    let nb_paths_part_1 = dfs(&graph, start, must_visit_2, &mut HashSet::new());
    let nb_paths_part_2 = dfs(&graph, must_visit_2, must_visit_1, &mut HashSet::new());
    let nb_paths_part_3 = dfs(&graph, must_visit_1, end, &mut HashSet::new());

    let total_2 = nb_paths_part_1 * nb_paths_part_2 * nb_paths_part_3;

    total_1 + total_2
}

fn dfs(graph: &Graph, current: &str, end: &str, visited: &mut HashSet<String>) -> u64 {
    if current == end {
        return 1;
    }

    visited.insert(current.to_string());

    let neighbors = match graph.nodes.get(current) {
        Some(n) => n,
        None => {
            visited.remove(current);
            return 0;
        }
    };

    let mut total = 0;
    for neighbor in neighbors {
        if !visited.contains(neighbor) {
            total += dfs(graph, neighbor, end, visited);
        }
    }

    visited.remove(current);

    total
}

fn parse_input(input: &str) -> Graph {
    let mut graph = Graph::new();

    for line in input.lines() {
        let parts: Vec<&str> = line.split(':').collect();
        let name = parts[0].trim().to_string();
        let neighbors: Vec<String> = parts[1].split_whitespace().map(|s| s.to_string()).collect();
        graph.add_node_and_neighbors(name, neighbors);
    }

    graph
}

fn part1(input: &str) -> u64 {
    let graph = parse_input(input);

    let nb_different_paths = count_nb_different_paths(&graph);

    nb_different_paths
}

fn part2(input: &str) -> u64 {
    let graph = parse_input(input);

    let nb_different_paths = count_nb_different_paths_2(&graph);

    nb_different_paths
}
