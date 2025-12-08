use itertools::Itertools;
use std::collections::HashMap;
use std::fmt::Debug;
use std::fs;
use std::hash::Hash;
use std::path::PathBuf;

struct UnionFind<T> {
    parent: HashMap<T, T>,
}

impl<T: Copy + Eq + Hash + Debug> UnionFind<T> {
    fn new() -> Self {
        Self {
            parent: HashMap::new(),
        }
    }

    fn find(&mut self, x: T) -> T {
        let p = *self.parent.get(&x).unwrap_or(&x);
        if p != x {
            let root = self.find(p);
            self.parent.insert(x, root);
            root
        } else {
            x
        }
    }

    /// Returns true if a and b were in different sets (union happened)
    fn union(&mut self, a: T, b: T) -> bool {
        let ra = self.find(a);
        let rb = self.find(b);
        if ra != rb {
            self.parent.insert(ra, rb);
            true
        } else {
            false
        }
    }

    fn add(&mut self, x: T) {
        self.parent.entry(x).or_insert(x);
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

fn parse_input(input: &str) -> Vec<(u32, u32, u32)> {
    let mut junction_boxes: Vec<(u32, u32, u32)> = Vec::new();

    for line in input.lines() {
        let coordinate: Vec<u32> = line
            .split(',')
            .map(|coord| coord.parse::<u32>().unwrap())
            .collect();
        let tuple = (coordinate[0], coordinate[1], coordinate[2]);
        junction_boxes.push(tuple);
    }

    junction_boxes
}

fn dist2(a: &(u32, u32, u32), b: &(u32, u32, u32)) -> u64 {
    let dx = a.0 as i64 - b.0 as i64;
    let dy = a.1 as i64 - b.1 as i64;
    let dz = a.2 as i64 - b.2 as i64;
    (dx * dx + dy * dy + dz * dz) as u64
}

fn part1(input: &str) -> u32 {
    let junction_boxes = parse_input(input);

    let mut junctions_pairs: Vec<(&(u32, u32, u32), &(u32, u32, u32))> =
        junction_boxes.iter().tuple_combinations().collect();

    junctions_pairs.sort_by_key(|(a, b)| dist2(a, b));

    let mut uf = UnionFind::new();
    let mut effective_links = 0;
    let max_links = 1000;

    for (a, b) in junctions_pairs.iter().cycle() {
        if effective_links >= max_links {
            break;
        }

        uf.add(*a);
        uf.add(*b);
        uf.union(*a, *b);

        effective_links += 1;
    }

    // Build final groups
    let keys: Vec<_> = uf.parent.keys().copied().collect();
    let mut groups: HashMap<_, Vec<_>> = HashMap::new();
    for tuple in keys {
        let root = uf.find(tuple); // mutable borrow is safe now
        groups.entry(root).or_default().push(tuple);
    }

    let mut circuits: Vec<Vec<(u32, u32, u32)>> = groups
        .into_values()
        .map(|v| v.into_iter().copied().collect())
        .collect();

    circuits.sort_by_key(|c| std::cmp::Reverse(c.len()));

    let nb_count = 3;
    circuits
        .iter()
        .take(nb_count)
        .map(|c| c.len() as u32)
        .product()
}

fn all_connected(uf: &mut UnionFind<(u32, u32, u32)>, nodes: &[(u32, u32, u32)]) -> bool {
    if nodes.is_empty() {
        return true;
    }

    let first = uf.find(nodes[0]);
    nodes.iter().all(|&n| uf.find(n) == first)
}

fn part2(input: &str) -> u64 {
    let junction_boxes = parse_input(input);

    let mut junctions_pairs: Vec<(&(u32, u32, u32), &(u32, u32, u32))> =
        junction_boxes.iter().tuple_combinations().collect();

    junctions_pairs.sort_by_key(|(a, b)| dist2(a, b));

    let mut uf = UnionFind::new();

    for &node in &junction_boxes {
        uf.add(node);
    }

    let mut ultimate_junction = ((0, 0, 0), (0, 0, 0));

    for (a, b) in junctions_pairs.iter().cycle() {
        let changed = uf.union(**a, **b);

        if changed {
            if all_connected(&mut uf, &junction_boxes) {
                ultimate_junction = (**a, **b);
                break;
            }
        }
    }

    ultimate_junction.0.0 as u64 * ultimate_junction.1.0 as u64
}
