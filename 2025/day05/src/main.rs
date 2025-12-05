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

fn parse_input(input: &str) -> (Vec<(u64, u64)>, Vec<u64>) {
    let mut parts = input.split("\n\n");

    let block1 = parts.next().unwrap_or("");
    let block2 = parts.next().unwrap_or("");

    // Parse ingredient ID ranges
    let fresh_ingredient_id_ranges = block1
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|line| {
            let (a, b) = line.split_once('-').expect("Invalid format, expected A-B");
            (
                a.trim().parse::<u64>().expect("Invalid integer in A"),
                b.trim().parse::<u64>().expect("Invalid integer in B"),
            )
        })
        .collect::<Vec<_>>();

    // Parse the available ingredient IDs
    let ingredient_ids = block2
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|line| line.trim().parse::<u64>().expect("Invalid integer"))
        .collect::<Vec<_>>();

    (fresh_ingredient_id_ranges, ingredient_ids)
}

fn count_fresh_ingredient(
    fresh_ingredient_id_ranges: Vec<(u64, u64)>,
    ingredient_ids: Vec<u64>,
) -> u32 {
    let mut nb_fresh_ingredients: u32 = 0;

    for ingredient_id in ingredient_ids {
        for (lower_bound, higher_bound) in &fresh_ingredient_id_ranges {
            if (lower_bound..=higher_bound).contains(&&ingredient_id) {
                nb_fresh_ingredients += 1;
                break;
            }
        }
    }

    nb_fresh_ingredients
}

fn count_fresh_ingredient_ids(fresh_ingredient_id_ranges: &mut Vec<(u64, u64)>) -> u64 {
    let mut nb_fresh_ingredient_ids: u64 = 0;

    // Sort ranges by lower bound
    fresh_ingredient_id_ranges.sort_unstable_by_key(|&(a, _)| a);

    let mut current = fresh_ingredient_id_ranges[0];
    for &(start, end) in &fresh_ingredient_id_ranges[1..] {
        if start <= current.1 + 1 {
            // Overlaps or adjacent -> merge
            current.1 = current.1.max(end);
        } else {
            // No overlap: count current, start new
            nb_fresh_ingredient_ids += current.1 - current.0 + 1;
            current = (start, end);
        }
    }

    nb_fresh_ingredient_ids += current.1 - current.0 + 1;

    nb_fresh_ingredient_ids
}

fn part1(input: &str) -> u32 {
    let (fresh_ingredient_id_ranges, ingredient_ids) = parse_input(input);

    let nb_fresh_ingredient = count_fresh_ingredient(fresh_ingredient_id_ranges, ingredient_ids);

    nb_fresh_ingredient
}

fn part2(input: &str) -> u64 {
    let (mut fresh_ingredient_id_ranges, _ingredient_ids) = parse_input(input);

    let nb_fresh_ingredient_ids = count_fresh_ingredient_ids(&mut fresh_ingredient_id_ranges);

    nb_fresh_ingredient_ids
}
