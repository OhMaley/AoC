use std::fs;
use std::path::PathBuf;

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

fn parse_input(input: &str) -> (Vec<Vec<u64>>, Vec<char>) {
    let mut lines = input
        .lines()
        .map(|l| l.trim_end())
        .filter(|l| !l.trim().is_empty())
        .collect::<Vec<_>>();

    let op_line = lines.pop().unwrap();

    let ops = op_line
        .split_whitespace()
        .map(|tok| tok.chars().next().unwrap())
        .collect::<Vec<_>>();

    let matrix = lines
        .into_iter()
        .map(|line| {
            line.split_whitespace()
                .map(|s| s.parse::<u64>().expect("invalid number"))
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    (matrix, ops)
}

fn parse_input_2(input: &str) -> (Vec<Vec<String>>, Vec<char>) {
    let mut lines = input.lines().collect::<Vec<_>>();

    let op_line = lines.pop().unwrap();

    let chars_with_pos: Vec<(usize, char)> = op_line
        .char_indices()
        .filter(|&(_, c)| !c.is_whitespace())
        .collect();

    let (positions, ops): (Vec<usize>, Vec<char>) = chars_with_pos.into_iter().unzip();

    let mut positions = positions.clone();
    positions.push(lines[0].len() + 1);

    let matrix = lines
        .into_iter()
        .map(|line| {
            let mut row = Vec::new();
            for w in positions.windows(2) {
                let start = w[0];
                let end = w[1] - 1;
                row.push(line[start..end].to_string());
            }
            row
        })
        .collect::<Vec<_>>();

    (matrix, ops)
}

fn math_worksheet_solver(matrix: Vec<Vec<u64>>, ops: Vec<char>) -> u64 {
    let total: u64 = (0..matrix[0].len())
        .map(|j| {
            let col = matrix.iter().map(|row| row[j]);
            match ops[j] {
                '*' => col.product::<u64>(),
                '+' => col.sum::<u64>(),
                _ => panic!("Invalid operator"),
            }
        })
        .sum();

    total
}

fn math_worksheet_solver_2(matrix: Vec<Vec<String>>, ops: Vec<char>) -> u64 {
    let total: u64 = (0..matrix[0].len())
        .map(|j| {
            let max_len = matrix.iter().map(|row| row[j].len()).max().unwrap();
            let numbers: Vec<u64> = (0..max_len)
                .map(|char_pos| {
                    let s: String = matrix
                        .iter()
                        .filter_map(|row| row[j].chars().nth(char_pos))
                        .collect();
                    s.trim().parse::<u64>().unwrap()
                })
                .collect();
            match ops[j] {
                '*' => numbers.iter().product::<u64>(),
                '+' => numbers.iter().sum::<u64>(),
                _ => panic!("Invalid operator"),
            }
        })
        .sum();

    total
}

fn part1(input: &str) -> u64 {
    let (matrix, ops) = parse_input(input);
    let result = math_worksheet_solver(matrix, ops);

    result
}

fn part2(input: &str) -> u64 {
    let (matrix, ops) = parse_input_2(input);
    let result = math_worksheet_solver_2(matrix, ops);

    result
}
