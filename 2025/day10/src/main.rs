use regex::Regex;
use std::collections::{HashSet, VecDeque};
use std::fs;
use std::path::PathBuf;

#[derive(Debug)]
struct Machine {
    light_diagram: Vec<bool>,
    button_schematics: Vec<Vec<u32>>,
    joltage_requirements: Vec<u32>,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Node {
    lights: Vec<bool>,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Node2 {
    joltage: Vec<u32>,
}

fn main() {
    let input = read_input("input.txt");
    println!("Solution for part 1: {}", part1(&input));
    println!("Solution for part 1: {}", part2(&input));
}

fn read_input(filename: &str) -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push(filename);

    fs::read_to_string(path)
        .expect("Could not read the input file")
        .trim()
        .to_string()
}

fn parse_input(input: &str) -> Vec<Machine> {
    let machines: Vec<Machine> = input
        .lines()
        .map(|line| line.trim())
        .map(|line| {
            let re_main = Regex::new(
                r"^\s*\[(?P<light_diagram>[^\]]+)\]\s*(?P<button_schematics>.*?)\s*\{(?P<joltage_requirements>[^\}]+)\}\s*$"
            ).expect("Regex parse error");
            let captures = re_main.captures(line).expect("Regex capture failed");

            let light_diagram = captures["light_diagram"].to_string();
            let button_schematics = captures["button_schematics"].to_string();
            let joltage_requirements = captures["joltage_requirements"].to_string();

            (light_diagram, button_schematics, joltage_requirements)
        }).map(|(light_diagram, button_schematics, joltage_requirements)| {
            let light_diagram: Vec<bool> = light_diagram.chars().map(|c| c == '#').collect();

            let re = Regex::new(r"\(([^)]+)\)").unwrap();
            let button_schematics: Vec<Vec<u32>> = re.captures_iter(&button_schematics)
                .map(|capture| {
                    capture[1].split(',').map(|n| n.parse::<u32>().expect("parse error")).collect()
                })
                .collect::<Vec<Vec<u32>>>();

            let joltage_requirements: Vec<u32> = joltage_requirements.split(',').map(|s| s.parse::<u32>().expect("invalid number")).collect();

            Machine { light_diagram, button_schematics, joltage_requirements }
        })
        .collect();

    return machines;
}

fn get_fewest_button_presses(machine: &Machine) -> u32 {
    // Goal is to run a BFS from the initial lights state and stops as soon as the required lights state is reached

    let start = Node {
        lights: vec![false; machine.light_diagram.len()],
    };
    let target = Node {
        lights: machine.light_diagram.clone(),
    };

    bfs(start, target, &machine.button_schematics)
}

fn get_fewest_button_presses_2(machine: &Machine) -> u32 {
    let start = Node2 {
        joltage: vec![0; machine.joltage_requirements.len()],
    };
    let target = Node2 {
        joltage: machine.joltage_requirements.clone(),
    };

    bfs_2(
        start,
        target,
        &machine.button_schematics
    )
}

fn generate_neighbors(node: &Node, button_schematics: &Vec<Vec<u32>>) -> Vec<Node> {
    let mut neighbors = vec![];
    for action in button_schematics {
        let mut lights = node.lights.clone();
        for &i in action {
            if let Some(b) = lights.get_mut(i as usize) {
                *b = !*b;
            }
        }
        neighbors.push(Node { lights: lights });
    }
    neighbors
}

fn bfs(start: Node, target: Node, button_schematics: &Vec<Vec<u32>>) -> u32 {
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();

    visited.insert(start.clone());
    queue.push_back((start, 0 as u32));

    while let Some((current, dist)) = queue.pop_front() {
        if current == target {
            return dist;
        }

        for neighbor in generate_neighbors(&current, button_schematics) {
            if visited.insert(neighbor.clone()) {
                queue.push_back((neighbor, dist + 1));
            }
        }
    }

    9999
}

fn bfs_2(
    start: Node2,
    target: Node2,
    button_schematics: &Vec<Vec<u32>>
) -> u32 {
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();

    visited.insert(start.joltage.clone());
    queue.push_back((start.joltage, 0 as u32));

    println!("------------------------------------");

    while let Some((current, dist)) = queue.pop_front() {
        if current == target.joltage {
            return dist;
        }

        for action in button_schematics {
            let max_apply = action
                .iter()
                .map(|&i| target.joltage[i as usize] - current[i as usize])
                .min()
                .unwrap_or(0);

            if max_apply == 0 {
                continue; // cannot apply command at all
            }

            for k in 1..=max_apply {
                let mut next = current.clone();
                for &i in action {
                    next[i as usize] += k;
                }

                if visited.insert(next.clone()) {
                    queue.push_back((next, dist + k));
                }
            }
        }
    }

    99999
}

fn part1(input: &str) -> u32 {
    let machines = parse_input(input);
    machines
        .iter()
        .map(|machine| get_fewest_button_presses(machine))
        .sum()
}

fn part2(input: &str) -> u32 {
    let machines = parse_input(input);
    machines
        .iter()
        .map(|machine| get_fewest_button_presses_2(machine))
        .sum()
}
