use std::collections::HashSet;
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

fn parse_line(line: &str) -> Vec<(i64, i64)> {
    let ranges: Vec<(i64, i64)> = line
        .split(',')
        .map(|range| {
            let (first_id, last_id) = range.split_once('-').unwrap();
            (
                first_id.parse::<i64>().unwrap(),
                last_id.parse::<i64>().unwrap(),
            )
        })
        .collect();

    ranges
}

fn sum_invalid_id(first_id: i64, last_id: i64) -> i64 {
    let mut sum: i64 = 0;

    let min_len = first_id.to_string().len();
    let max_len = last_id.to_string().len();

    for total_len in (min_len..=max_len).filter(|x| x % 2 == 0) {
        let half_len = total_len / 2;
        let start = 10_i64.pow((half_len - 1) as u32);
        let end = 10_i64.pow(half_len as u32) - 1;

        for half in start..=end {
            let full = half * 10_i64.pow(half_len as u32) + half;
            if full > last_id {
                break;
            }
            if full >= first_id {
                sum += full;
            }
        }
    }

    sum
}

fn sum_invalid_id_v2(first_id: i64, last_id: i64) -> i64 {
    let mut result = Vec::new();

    let min_len = first_id.to_string().len();
    let max_len = last_id.to_string().len();

    for len in min_len..=max_len {
        for k in 1..=len / 2 {
            // Odd length
            if len % k != 0 {
                continue;
            }

            let repeats = len / k;
            if repeats < 2 {
                continue;
            }

            let start = 10_i64.pow((k - 1) as u32);
            let end = 10_i64.pow(k as u32) - 1;

            for prefix in start..=end {
                // Build the number
                let mut full = 0i64;
                let pow = 10_i64.pow(k as u32);
                for _ in 0..repeats {
                    full = full * pow + prefix;
                }

                if full > last_id {
                    break;
                }
                if full >= first_id {
                    result.push(full);
                }
            }
        }
    }

    let set: HashSet<_> = result.into_iter().collect(); // removes duplicates
    let sum = set.into_iter().sum();

    sum
}

fn part1(input: &str) -> i64 {
    let ranges: Vec<(i64, i64)> = parse_line(input);

    let mut sum: i64 = 0;

    for (first_id, last_id) in &ranges {
        sum += sum_invalid_id(*first_id, *last_id);
    }

    sum
}

fn part2(input: &str) -> i64 {
    let ranges: Vec<(i64, i64)> = parse_line(input);

    let mut sum: i64 = 0;

    for (first_id, last_id) in &ranges {
        sum += sum_invalid_id_v2(*first_id, *last_id);
    }

    sum
}
